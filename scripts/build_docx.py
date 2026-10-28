"""Gera o relatório ABNT do OLIST-2 (Word) a partir dos resultados do notebook.

Uso (na raiz do projeto, com o .venv ativo):
    python scripts/build_docx.py

1. Cria docs/abnt/template_fiap.docx a partir do modelo do TCC (docs/PTCC_Nalanda_revisado_v7.docx):
   mesmo layout (A4, margens, Arial, rodapé com página), com logo e texto de cabeçalho da FIAP.
2. Preenche docs/abnt/OLIST-2_relatorio.docx com o texto, as tabelas e as figuras.
   Todos os números vêm de reports/indicadores.json — nenhum é digitado à mão.
"""
import json
import re
import shutil
import sys
import zipfile
from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from olist import config  # noqa: E402

SOURCE_TEMPLATE = ROOT / "docs" / "PTCC_Nalanda_revisado_v7.docx"
ABNT = ROOT / "docs" / "abnt"
TEMPLATE = ABNT / "template_fiap.docx"
LOGO = ABNT / "assets" / "fiap_logo.png"
OUT = ABNT / "OLIST-2_relatorio.docx"

HEADER_OLD = "Trabalho de Conclusão de Curso apresentado para obtenção do título de especialista em Data Science e Analytics – 2026"
HEADER_NEW = "Tech Challenge · Pós-graduação em Agentic AI · Fase 1 – FIAP – 2026"
LOGO_HEIGHT_EMU = 298450  # mesma altura do logo original no cabeçalho


# ---------------------------------------------------------------- 1. template FIAP

def make_template():
    """Copia o modelo, troca o logo do cabeçalho (word/media/image3.png) e o texto do cabeçalho."""
    from PIL import Image  # vem com o matplotlib

    w, h = Image.open(LOGO).size
    cx = int(LOGO_HEIGHT_EMU * w / h)
    ABNT.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(SOURCE_TEMPLATE) as src, zipfile.ZipFile(TEMPLATE, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            data = src.read(item.filename)
            if item.filename == "word/media/image3.png":
                data = LOGO.read_bytes()
            elif item.filename == "word/header1.xml":
                xml = data.decode("utf-8")
                assert HEADER_OLD in xml, "texto do cabeçalho do modelo mudou"
                xml = xml.replace(HEADER_OLD, HEADER_NEW)
                xml = xml.replace('<wp:extent cx="723900" cy="298450"/>', f'<wp:extent cx="{cx}" cy="{LOGO_HEIGHT_EMU}"/>', 1)
                xml = re.sub(r'(<wp:positionH relativeFrom="column"><wp:posOffset>)5035550(</wp:posOffset>)',
                             lambda m: f"{m.group(1)}{5759450 - cx}{m.group(2)}", xml, count=1)
                data = xml.encode("utf-8")
            dst.writestr(item, data)
    return TEMPLATE


# ---------------------------------------------------------------- 2. helpers de formatação (mesmo padrão do modelo)

def _font(run, size=11, bold=False, italic=False, color=None, superscript=False):
    run.font.name = "Arial"
    run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "Arial")
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.superscript = superscript
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    return run


def _para(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=False, line=1.5, before=0, after=0, keep=False):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = align
    pf.line_spacing = line
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    if indent:
        pf.first_line_indent = Cm(1.25)
    if keep:
        pf.keep_with_next = True
    return p


def rich(p, text, size=11, base_bold=False):
    """Escreve texto com **negrito** e ^sobrescrito^ simples."""
    for part in re.split(r"(\*\*[^*]+\*\*|\^[^^]+\^)", text):
        if not part:
            continue
        if part.startswith("**"):
            _font(p.add_run(part[2:-2]), size, bold=True)
        elif part.startswith("^"):
            _font(p.add_run(part[1:-1]), size, bold=base_bold, superscript=True)
        else:
            _font(p.add_run(part), size, bold=base_bold)
    return p


def body(doc, text):
    return rich(_para(doc, indent=True), text)


def heading(doc, text, level=1):
    p = _para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, before=12 if level == 1 else 6, after=6, keep=True)
    _font(p.add_run(text), 11, bold=True, italic=level == 2)
    return p


def blank(doc):
    return _para(doc, line=1.0)


def bullet(doc, text):
    p = _para(doc, indent=False)
    p.paragraph_format.left_indent = Cm(1.25)
    p.paragraph_format.first_line_indent = Cm(-0.5)
    return rich(p, "– " + text)


def caption(doc, text):
    p = _para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, line=1.0, before=6, after=3, keep=True)
    _font(p.add_run(text), 10)
    return p


def source(doc, text="Fonte: Elaboração própria."):
    p = _para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, line=1.0, before=3, after=9)
    _font(p.add_run(text), 9)
    return p


def _borders(cell, top=None, bottom=None):
    tcPr = cell._tc.get_or_add_tcPr()
    b = OxmlElement("w:tcBorders")
    for side, val in (("top", top), ("bottom", bottom), ("left", "nil"), ("right", "nil")):
        e = OxmlElement(f"w:{side}")
        if val in (None, "nil"):
            e.set(qn("w:val"), "nil")
        else:
            e.set(qn("w:val"), "single"); e.set(qn("w:sz"), val); e.set(qn("w:color"), "000000")
        b.append(e)
    tcPr.append(b)


def table(doc, header, rows, widths_cm, size=9):
    """Tabela no padrão ABNT/IBGE: traço acima e abaixo do cabeçalho e no fim, sem linhas verticais."""
    t = doc.add_table(rows=1 + len(rows), cols=len(header))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for r, values in enumerate([header] + rows):
        for c, v in enumerate(values):
            cell = t.cell(r, c)
            cell.width = Cm(widths_cm[c])
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.line_spacing = 1.0
            _font(p.add_run(str(v)), size, bold=r == 0)
            last = r == len(rows)
            _borders(cell, top="8" if r in (0, 1) else None, bottom="8" if last else None)
    tr = t.rows[0]._tr
    trPr = tr.get_or_add_trPr()
    h = OxmlElement("w:tblHeader"); h.set(qn("w:val"), "true"); trPr.append(h)
    return t


def figure(doc, number, title, png, width_cm=15.5):
    caption(doc, f"Figura {number}. {title}")
    p = _para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, line=1.0, keep=True)
    p.add_run().add_picture(str(png), width=Cm(width_cm))
    source(doc, "Fonte: Elaboração própria a partir do dataset Olist (Kaggle).")


def br_int(n):
    return f"{int(n):,}".replace(",", ".")


def br_pct(x, d=1):
    return f"{x * 100:.{d}f}%".replace(".", ",")


def br_num(x, d=2):
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ---------------------------------------------------------------- 3. relatório

def build():
    data = json.loads(config.JSON_PATH.read_text(encoding="utf-8"))
    meta, inds, regras, inv = data["meta"], {i["id"]: i for i in data["indicadores"]}, data["regras"], data["inventario"]
    V = lambda k: inds[k]["valor"]          # noqa: E731
    T = lambda k: inds[k]["texto"]          # noqa: E731
    fig = lambda name: config.FIGURES / f"{name}.png"  # noqa: E731
    ini = date.fromisoformat(meta["inicio"]).strftime("%d/%m/%Y")
    fim = date.fromisoformat(meta["fim"]).strftime("%d/%m/%Y")
    pior_uf = re.search(r"\((\w{2})\)", inds["I15"]["definicao"]).group(1)

    doc = Document(str(make_template()))
    bd = doc.element.body
    for el in list(bd):
        if el.tag != qn("w:sectPr"):
            bd.remove(el)
    cp = doc.core_properties
    cp.author, cp.title = "Diogo, Igor e Lorran", "OLIST-2 · Preparação do dataset e indicadores-base"
    cp.comments, cp.last_modified_by = "Tech Challenge Agentic AI – Fase 1 – FIAP", "Igor"

    # Título e autores
    titulo = "Preparação e validação do dataset Olist: inventário, regras de qualidade e indicadores-base para a estratégia de IA agêntica"
    p = _para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, line=1.5, after=6)
    _font(p.add_run(titulo), 12, bold=True)
    blank(doc)
    rich(_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER), "Diogo^1^; Igor^1*^; Lorran^1^", base_bold=True)
    blank(doc)
    p = _para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, line=1.0)
    rich(p, "^1^ FIAP. Pós-graduação em Agentic AI. Tech Challenge – Fase 1. São Paulo, SP, Brasil", size=9)
    p = _para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, line=1.0)
    rich(p, "*autor correspondente: igorgtdas1@gmail.com · card OLIST-2", size=9)
    blank(doc)

    # Sumário executivo
    heading(doc, "Sumário Executivo")
    body(doc, (
        f"Este documento registra a primeira etapa analítica do Tech Challenge da Fase 1: preparar e validar o dataset público da Olist "
        f"antes de qualquer proposta de agente de IA. Foram inventariadas as {meta['tabelas']} tabelas do dataset ({br_int(V('I01'))} pedidos, "
        f"de {ini} a {fim}), mapeadas a granularidade e as chaves de cada uma e definidas oito regras de qualidade que evitam erros de contagem, "
        f"como tratar itens como pedidos ou cadastros como clientes. Com a base consolidada em uma linha por pedido, foram calculados 15 indicadores-base. "
        f"Os principais são: {T('I03')} dos pedidos entregues com datas válidas, prazo médio de entrega de {br_num(V('I04'), 1)} dias, taxa de atraso de {T('I05')}, "
        f"nota média de {br_num(V('I07'))} em 5 e {T('I08')} de avaliações negativas. Pedidos atrasados recebem, em média, {br_num(V('I09'))} pontos "
        f"a menos de nota que os entregues no prazo. Apenas {T('I12')} dos clientes compraram mais de uma vez, e {T('I10')} das avaliações trazem comentário em texto, "
        f"matéria-prima para agentes de leitura de reviews. Todos os números foram calculados em Python e reproduzidos com fórmulas do Excel, "
        f"que chegaram aos mesmos valores. Isso deixa a base pronta para as análises de profundidade (OLIST-3) e para a matriz de oportunidades (OLIST-5)."
    ))
    rich(_para(doc), "**Palavras-chave:** análise exploratória de dados; qualidade de dados; e-commerce; indicadores logísticos; inteligência artificial agêntica.")
    blank(doc)

    # Abstract
    p = _para(doc, align=WD_ALIGN_PARAGRAPH.CENTER)
    _font(p.add_run("Preparing and validating the Olist dataset: inventory, data quality rules and baseline indicators for an agentic AI strategy"), 11, bold=True)
    p = _para(doc, align=WD_ALIGN_PARAGRAPH.CENTER)
    _font(p.add_run("Abstract"), 11, bold=True)
    heading(doc, "Executive Summary")
    body(doc, (
        f"This document records the first analytical step of the Phase 1 Tech Challenge: preparing and validating the public Olist dataset before proposing any AI agent. "
        f"All {meta['tabelas']} tables were inventoried ({br_int(V('I01'))} orders, from {meta['inicio']} to {meta['fim']}), their grain and keys were mapped, "
        f"and eight data quality rules were defined to prevent counting errors, such as treating items as orders or customer records as customers. "
        f"From an order-level base, 15 baseline indicators were computed, including a late delivery rate of {br_pct(V('I05')).replace(',', '.')}, "
        f"an average delivery time of {V('I04'):.1f} days and an average review score of {V('I07'):.2f} out of 5. Late orders score "
        f"{V('I09'):.2f} points lower on average, and only {br_pct(V('I12')).replace(',', '.')} of customers bought more than once. "
        f"Every figure was computed in Python and reproduced with Excel formulas, with identical results."
    ))
    rich(_para(doc), "**Keywords:** exploratory data analysis; data quality; e-commerce; logistics indicators; agentic artificial intelligence.")
    blank(doc)

    # Introdução
    heading(doc, "Introdução")
    body(doc, (
        "A Olist conecta pequenos e médios lojistas aos grandes marketplaces brasileiros e deseja iniciar sua jornada com Inteligência Artificial Generativa e "
        "Agentes de IA. O enunciado do Tech Challenge lista os desafios da empresa: experiência do cliente, eficiência logística, retenção, avaliações, "
        "eficiência operacional, automação, apoio à decisão e escalabilidade. A pergunta da Fase 1 é como a Olist poderia usar essas tecnologias para melhorar "
        "sua operação e seus indicadores de negócio (FIAP, 2026)."
    ))
    body(doc, (
        "Antes de propor qualquer agente, é preciso saber o que os dados realmente dizem. Um agente que prioriza pedidos atrasados, por exemplo, "
        "só faz sentido se a taxa de atraso estiver bem medida. Na base pública da Olist, há armadilhas que mudam os números sem que ninguém perceba: "
        "um pedido aparece várias vezes na tabela de itens, o mesmo cliente recebe um código novo a cada compra e algumas avaliações se repetem. "
        "Uma análise que ignore esses detalhes produz indicadores errados, e uma estratégia construída sobre eles fica frágil."
    ))
    body(doc, (
        "Este trabalho corresponde ao card OLIST-2 do plano do grupo. Ele tem quatro objetivos: (i) inventariar as tabelas, com o número de registros, "
        "a granularidade e as chaves de cada uma; (ii) definir regras de qualidade em linguagem simples; (iii) calcular ao menos dez indicadores-base, "
        "cada um com definição, fórmula e tabela de origem; e (iv) entregar uma planilha que permita reproduzir cada número sem programação."
    ))

    # Metodologia
    heading(doc, "Metodologia")
    body(doc, (
        "A pesquisa é aplicada, de abordagem quantitativa e caráter exploratório e descritivo. A análise exploratória de dados (TUKEY, 1977) serve para conhecer "
        "a estrutura da base, identificar inconsistências e resumir o comportamento das variáveis antes de qualquer modelagem. O processo segue as etapas de "
        "entendimento e preparação dos dados do CRISP-DM (CHAPMAN et al., 2000)."
    ))
    body(doc, (
        f"A fonte é o Brazilian E-Commerce Public Dataset by Olist (OLIST, 2018), disponível no Kaggle e indicado pelo enunciado. Ele reúne {meta['tabelas']} arquivos CSV, "
        "oito citados no enunciado e uma tabela de apoio com a tradução das categorias, descritos na Tabela 1."
    ))
    caption(doc, "Tabela 1. Inventário das tabelas do dataset: registros, chave e granularidade.")
    table(doc, ["Tabela", "Registros", "Chave", "1 linha representa"],
          [[r["tabela"], br_int(r["registros"]), r["chave"] + ("" if r["chave_e_unica"] == "sim" else " (repete)"), r["granularidade"]] for r in inv],
          [3.2, 2.0, 4.6, 6.2])
    source(doc, "Fonte: Elaboração própria a partir do dataset Olist (Kaggle).")
    body(doc, (
        "O trabalho foi feito em Python 3.13, com as bibliotecas pandas e NumPy para os cálculos (MCKINNEY, 2010; HARRIS et al., 2020), Matplotlib para os gráficos "
        "(HUNTER, 2007) e XlsxWriter para a planilha. Todo o processo está em um único notebook Jupyter, organizado em etapas com explicações em texto. "
        "O código reutilizável fica em um pacote do repositório do projeto, e os arquivos originais nunca são alterados. A Tabela 2 resume o passo a passo."
    ))
    caption(doc, "Tabela 2. Etapas do notebook de preparação e o que cada uma entrega.")
    etapas = [
        ("0", "Preparação", "Carrega bibliotecas, caminhos e o estilo padrão dos gráficos"),
        ("1", "Carga e inventário", "Registros, colunas e chave de cada tabela (Tabela 1, Figura 1)"),
        ("2", "Granularidade e chaves", "Linhas por entidade, mapa de chaves e integridade referencial (Figuras 2 a 4)"),
        ("3", "Nulos", "Colunas com valores vazios e o motivo de cada vazio (Figura 5)"),
        ("4", "Período e status", "Datas cobertas, meses de borda e situação dos pedidos (Figuras 6 e 7)"),
        ("5", "Regras de qualidade", "Oito regras, cada uma medida e checada (Tabela 3)"),
        ("6", "Base de pedidos", f"Base com 1 linha por pedido ({br_int(meta['pedidos'])} linhas) e as regras aplicadas"),
        ("7", "Indicadores", "15 indicadores com definição, fórmula e origem (Tabela 4, Figuras 8 a 10)"),
        ("8", "Exportação", "Planilha Excel com fórmulas vivas, arquivo de dados e figuras"),
        ("9", "Checklist", "Conferência dos critérios de aceite do card"),
    ]
    table(doc, ["Etapa", "Nome", "O que entrega"], [list(e) for e in etapas], [1.4, 3.8, 10.8])
    source(doc)
    body(doc, (
        "A planilha gerada pelo notebook tem uma aba por indicador. Em cada aba, uma fórmula do Excel recalcula o número a partir da base de pedidos e aparece ao lado "
        "do valor obtido em Python, com uma coluna de conferência. Assim, qualquer integrante do grupo consegue auditar os resultados sem programar."
    ))

    # Resultados
    heading(doc, "Resultados e Discussão")
    heading(doc, "Inventário, granularidade e chaves", 2)
    geo = next(r for r in inv if r["tabela"] == "geolocation")
    body(doc, (
        f"A tabela de geolocalização concentra {br_int(geo['registros'])} linhas, mais que todas as outras somadas (Figura 1). "
        "Essa diferença de escala também é de natureza: ela registra pontos de coordenada, e não entidades do negócio."
    ))
    figure(doc, 1, "Registros por tabela do dataset (escala logarítmica).", fig("g01_registros_por_tabela"), 14.5)
    gran = {g["tabela"]: g for g in meta["granularidade"]}
    body(doc, (
        f"A Figura 2 mostra quantas linhas cada tabela tem para cada entidade que descreve. Itens têm {br_num(gran['order_items']['linhas_por_entidade'])} linhas por pedido, "
        f"pagamentos {br_num(gran['payments']['linhas_por_entidade'])} e avaliações {br_num(gran['order_reviews']['linhas_por_entidade'])}. "
        f"A geolocalização tem {br_num(gran['geolocation']['linhas_por_entidade'], 1)} linhas por prefixo de CEP. "
        "Essas tabelas precisam ser resumidas para uma linha por pedido ou por CEP antes de qualquer cruzamento. Caso contrário, o mesmo pedido é contado várias vezes."
    ))
    figure(doc, 2, "Linhas por entidade distinta em cada tabela.", fig("g02_linhas_por_entidade"), 14.5)
    body(doc, (
        "O mapa de chaves (Figura 3) mostra que a tabela de pedidos é o centro do modelo: itens, pagamentos e avaliações se ligam a ela pelo código do pedido, "
        "e ela se liga ao cliente. Produtos e vendedores entram pelos itens. A geolocalização se liga aos clientes e aos vendedores por prefixo de CEP, "
        "que não é único, por isso a ligação é indireta."
    ))
    figure(doc, 3, "Mapa de chaves e cardinalidade entre as tabelas.", fig("g03_mapa_de_chaves"), 15.5)
    menor = min(meta["integridade"], key=lambda r: r["pct_encontrado"])
    body(doc, (
        f"A integridade referencial é alta (Figura 4). Todas as chaves de pedido, produto e vendedor encontram par. As maiores lacunas são os pedidos sem item ou sem avaliação, "
        f"com cerca de {br_pct(1 - menor['pct_encontrado'])} dos pedidos, e alguns CEPs sem coordenada. Esses casos não são corrigidos: eles ficam declarados como limitação."
    ))
    figure(doc, 4, "Percentual de valores que encontram par na tabela relacionada.", fig("g04_integridade_referencial"), 15.5)

    heading(doc, "Valores ausentes, período e status", 2)
    body(doc, (
        "A maior parte dos vazios é esperada (Figura 5). O comentário da avaliação é opcional, e pedidos não entregues não têm data de entrega. "
        "Por isso, a regra adotada é nunca trocar vazio por zero: um pedido sem avaliação não tem nota zero, e um pedido cancelado não teve prazo zero."
    ))
    figure(doc, 5, "Percentual de valores vazios por coluna.", fig("g05_nulos_por_coluna"), 15.5)
    body(doc, (
        f"As compras vão de {ini} a {fim}. Os meses {', '.join(meta['meses_de_borda'])} têm menos de 10% da mediana mensal de pedidos (Figura 6). "
        "Eles são meses de borda, quando a coleta começou ou terminou, e ficam fora de comparações mês a mês. "
        f"Quase todos os pedidos foram entregues: os cancelados e indisponíveis somam {T('I11')} (Figura 7)."
    ))
    figure(doc, 6, "Pedidos por mês de compra.", fig("g06_pedidos_por_mes"), 15.5)
    figure(doc, 7, "Pedidos por status.", fig("g07_pedidos_por_status"), 14.0)

    heading(doc, "Regras de qualidade", 2)
    body(doc, (
        "A Tabela 3 apresenta as oito regras de qualidade. O plano do grupo pedia ao menos seis. Seis delas (R1 a R6) corrigem armadilhas que mudam os "
        "indicadores-base. As outras duas (R7 e R8) protegem cruzamentos que serão usados nas próximas etapas, com geolocalização e valor do pedido. "
        "Todas foram medidas e checadas no notebook."
    ))
    caption(doc, "Tabela 3. Regras de qualidade, problema que evitam e registros afetados.")
    table(doc, ["Regra", "Em linguagem simples", "Por que existe", "Afetados"],
          [[r["id"], r["regra"], r["motivo"], br_int(r["afetados"])] for r in regras], [1.2, 6.0, 6.6, 2.2], size=8)
    source(doc)

    heading(doc, "Indicadores-base", 2)
    body(doc, (
        "A Tabela 4 reúne os 15 indicadores calculados sobre a base de pedidos. Cada um tem fórmula, tabela de origem e as regras de qualidade aplicadas. "
        "As definições completas e as fórmulas do Excel estão na planilha que acompanha este documento."
    ))
    caption(doc, "Tabela 4. Indicadores-base: fórmula, origem, regras e valor.")
    table(doc, ["ID", "Indicador", "Fórmula", "Origem", "Regras", "Valor"],
          [[i["id"], i["nome"], i["formula"], i["tabelas"], i["regras"], i["texto"]] for i in data["indicadores"]],
          [1.0, 3.4, 5.6, 2.6, 1.4, 2.0], size=8)
    source(doc)
    body(doc, (
        f"A logística aparece como o primeiro ponto de atenção. A taxa de atraso é de {T('I05')} dos pedidos entregues, e, quando há atraso, ele passa em média "
        f"{br_num(V('I06'), 1)} dias da data prometida. A distribuição das notas é concentrada em 5, mas {T('I08')} das avaliações são negativas (Figura 8)."
    ))
    figure(doc, 8, "Distribuição das notas de avaliação.", fig("g08_distribuicao_notas"), 13.0)
    diff = V("I09")
    body(doc, (
        f"A nota cai de forma consistente com o tamanho do atraso (Figura 9). A diferença média entre pedidos no prazo e atrasados é de {br_num(diff)} pontos. "
        "Isso indica associação, não causa: outros fatores, como o tipo de produto ou a região, podem variar junto com o atraso. O card OLIST-3 aprofunda essa leitura."
    ))
    figure(doc, 9, "Nota média por faixa de atraso.", fig("g09_nota_por_faixa_de_atraso"), 14.0)
    body(doc, (
        f"O atraso não se distribui igualmente pelo país (Figura 10). Entre os estados com pelo menos 500 entregas, {pior_uf} tem a maior taxa ({T('I15')}). "
        f"Estados do Sul e do Sudeste ficam abaixo da média nacional. Também se destacam a baixa recompra ({T('I12')} dos clientes) e o volume de comentários "
        f"em texto ({T('I10')} das avaliações), temas para as oportunidades de retenção e de leitura de avaliações."
    ))
    figure(doc, 10, "Taxa de atraso por UF do cliente.", fig("g10_atraso_por_uf"), 14.5)
    body(doc, (
        "Cada indicador da Tabela 4 foi recalculado com fórmulas do Excel sobre a aba base_pedidos, e todos chegaram ao mesmo valor do Python. "
        "Falta um colega do grupo repetir essa conferência para ao menos três indicadores, como pede o critério de aceite do card."
    ))

    # Considerações finais
    heading(doc, "Considerações Finais")
    body(doc, (
        "A etapa de preparação deixou a base pronta e documentada. Todas as tabelas estão inventariadas, oito regras de qualidade estão justificadas e aplicadas, "
        "e quinze indicadores-base são reproduzíveis em Python e em Excel. Os números mostram três temas para a estratégia de IA: a pontualidade da entrega "
        "e seu efeito na satisfação, a baixa recompra e o grande volume de avaliações em texto."
    ))
    body(doc, (
        "Os dados cobrem apenas 2016 a 2018 e não trazem custos internos nem registros de atendimento. As relações observadas são associações. "
        "As próximas etapas são aprofundar as análises por categoria, vendedor e frete (OLIST-3) e usar os indicadores como evidência na matriz de "
        "oportunidades (OLIST-5) e nos KPIs dos agentes (OLIST-6)."
    ))

    # Cronograma
    heading(doc, "Cronograma de Atividades")
    caption(doc, "Tabela 5. Cronograma do card OLIST-2 dentro da sprint da Fase 1.")
    table(doc, ["Atividade", "Data", "Situação"], [
        ["Inventário, granularidade e chaves", "26/10", "concluído"],
        ["Regras de qualidade e base de pedidos", "26/10–27/10", "concluído"],
        ["Indicadores-base e planilha", "27/10", "concluído"],
        ["Conferência por um colega (CA4)", "até o Checkpoint 2 (30/10)", "pendente"],
        ["Entrega do relatório executivo da Fase 1", "03/11", "a fazer"],
    ], [8.0, 4.6, 3.4])
    source(doc)

    # Referências
    heading(doc, "Referências")
    refs = [
        "CHAPMAN, P. et al. CRISP-DM 1.0: step-by-step data mining guide. [S.l.]: SPSS, 2000.",
        "FIAP. Tech Challenge Agentic AI – Fase 1: Olist Intelligent Marketplace. São Paulo: FIAP, 2026. Enunciado da atividade.",
        "HARRIS, C. R. et al. Array programming with NumPy. Nature, v. 585, p. 357-362, 2020. DOI: 10.1038/s41586-020-2649-2.",
        "HUNTER, J. D. Matplotlib: a 2D graphics environment. Computing in Science & Engineering, v. 9, n. 3, p. 90-95, 2007.",
        "MCKINNEY, W. Data structures for statistical computing in Python. In: PYTHON IN SCIENCE CONFERENCE, 9., 2010, Austin. Proceedings [...]. Austin: SciPy, 2010. p. 56-61.",
        "OLIST. Brazilian E-Commerce Public Dataset by Olist. Kaggle, 2018. Disponível em: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce. Acesso em: 26 out. 2026.",
        "TUKEY, J. W. Exploratory data analysis. Reading: Addison-Wesley, 1977.",
    ]
    for ref in refs:
        p = _para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, line=1.0, after=12)
        _font(p.add_run(ref), 11)

    doc.save(OUT)
    print("Word:", OUT)
    return OUT


if __name__ == "__main__":
    build()
