"""Gera o rascunho do Relatório Executivo da Fase 1 (Word, template FIAP), com todas as seções.

Uso (na raiz do projeto, com o .venv ativo e depois de rodar os notebooks 01 e 02):
    python scripts/build_relatorio_fase1.py

- Seções prontas: título preto, texto escrito com os números de reports/indicadores.json e reports/achados_olist3.json.
- Seções que ainda não estão prontas: título em vermelho e uma caixa vermelha dizendo o que falta,
  a que card se refere e quem é o responsável. Quando a seção ficar pronta, tire o título de PENDENTES.
"""
import json

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

import build_docx as b
from olist import config

OUT = b.ABNT / "Relatorio_Executivo_Fase1_rascunho.docx"
RED = "C00000"
RED_FILL = "FDECEA"
GRAY = "7F7F7F"

# Seções que ainda não estão prontas: o título sai em vermelho. Uma seção-mãe fica vermelha se alguma parte dela estiver pendente.
PENDENTES = {
    "Sumário Executivo", "3. O que os dados mostram",
    "5. Oportunidades e priorização", "6. Mapa de agentes",
    "7. Fichas dos agentes: responsabilidades, limites e autonomia", "7.1 Sentinela de Entregas", "7.2 Voz do Cliente", "7.3 Copiloto Operacional",
    "8. Arquitetura conceitual", "8.1 Diagrama", "8.2 Fluxo das informações", "8.3 Governança, monitoramento e integrações futuras",
    "9. Prompts estruturados", "9.1 Prompt · Sentinela de Entregas", "9.2 Prompt · Voz do Cliente", "9.3 Prompt · Copiloto Operacional",
    "10. Impacto esperado e indicadores", "10.1 O que podemos e o que não podemos afirmar",
    "11. Riscos, governança e autonomia", "12. Roadmap nas cinco fases", "13. Conclusão e recomendação", "Vídeo executivo",
}


def titulo(doc, text, level=1):
    """Título de seção (nível 1 em negrito; nível 2 em negrito itálico); vermelho se a seção ainda não está pronta."""
    p = b._para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, before=14 if level == 1 else 8, after=6, keep=True)
    b._font(p.add_run(text), 12 if level == 1 else 11, bold=True, italic=level == 2, color=RED if text in PENDENTES else None)
    return p


def afazer(doc, card, quem, texto):
    """Caixa vermelha de pendência: a que card se refere, quem é o responsável e o que falta."""
    p = b._para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, line=1.15, before=4, after=8)
    p.paragraph_format.left_indent = b.Cm(0.2)
    p.paragraph_format.right_indent = b.Cm(0.2)
    pPr = p._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    for side in ("top", "left", "bottom", "right"):
        e = OxmlElement(f"w:{side}")
        e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "12"); e.set(qn("w:space"), "4"); e.set(qn("w:color"), RED)
        bdr.append(e)
    pPr.append(bdr)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), RED_FILL)
    pPr.append(shd)
    b._font(p.add_run(f"A FAZER · Card {card} · {quem}"), 10, bold=True, color=RED)
    p.add_run().add_break()
    b._font(p.add_run(texto), 10, color=RED)
    return p


def build():
    o2 = json.loads(config.JSON_PATH.read_text(encoding="utf-8"))
    o3 = json.loads((config.REPORTS / "achados_olist3.json").read_text(encoding="utf-8"))
    I = {i["id"]: i for i in o2["indicadores"]}
    A = {a["id"]: a for a in o3["achados"]}
    K = {k["rank"]: k for k in o3["chave"]}
    meta = o2["meta"]
    fig = lambda n: config.FIGURES / f"{n}.png"  # noqa: E731

    doc = Document(str(b.make_template()))
    body_el = doc.element.body
    for el in list(body_el):
        if el.tag != qn("w:sectPr"):
            body_el.remove(el)
    cp = doc.core_properties
    cp.author, cp.title = "Diogo, Igor e Lorran", "Relatório Executivo – Fase 1 – Olist (rascunho)"
    cp.comments, cp.last_modified_by = "Tech Challenge Agentic AI – Fase 1 – FIAP · OLIST-7", "Igor"

    # ------------------------------------------------------------------ capa
    p = b._para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, line=1.5, after=6)
    b._font(p.add_run("Olist Intelligent Marketplace: como IA Generativa e Agentes de IA podem melhorar a operação e os indicadores da Olist"), 14, bold=True)
    b.rich(b._para(doc, align=WD_ALIGN_PARAGRAPH.CENTER), "Diogo; Igor; Lorran", base_bold=True)
    b.rich(b._para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, line=1.0), "Relatório Executivo · Tech Challenge Agentic AI – Fase 1 · FIAP · 2026", size=10)
    p = b._para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, line=1.0, before=6, after=10)
    b._font(p.add_run("RASCUNHO EM CONSTRUÇÃO: títulos em vermelho marcam as seções que ainda não estão prontas; as caixas vermelhas dizem o que falta e a que card se refere."), 9, italic=True, color=GRAY)

    # ------------------------------------------------------------------ sumário executivo
    titulo(doc, "Sumário Executivo")
    b.body(doc, (
        f"A Olist quer usar IA Generativa e Agentes de IA para melhorar sua operação e seus indicadores. Analisamos {b.br_int(I['I01']['valor'])} pedidos "
        f"feitos de {I['I02']['texto']} e encontramos um eixo claro: a entrega. Com atraso, {b.br_pct(V(o3, 'M01', 'atrasados'), 0)} dos clientes "
        f"dão nota 1 ou 2; no prazo, só {b.br_pct(V(o3, 'M01', 'no prazo'), 0)}. O atraso dá sinais antes de acontecer, porque se forma no transporte e na postagem "
        "fora do prazo pelo vendedor. Ele também se concentra em rotas longas, no Norte e no Nordeste e em poucos meses de pico. Os comentários negativos, "
        "com milhares de textos, falam principalmente de entrega e de produto."
    ))
    b.body(doc, (
        "Recomendamos começar por três agentes, com uma pessoa aprovando as ações que afetam o cliente:"
    ))
    b.bullet(doc, "**um agente que previne o atraso;**")
    b.bullet(doc, "**um agente que lê e encaminha as avaliações;**")
    b.bullet(doc, "**um copiloto que apoia as decisões dos gestores.**")
    afazer(doc, "OLIST-7", "Diogo", "Fechar o sumário (até 1 página) depois de prontos os agentes, os KPIs e o roadmap; incluir 3–5 números de destaque do OLIST-4.")

    # ------------------------------------------------------------------ 1
    titulo(doc, "1. Contexto, pergunta e escopo")
    titulo(doc, "1.1 A Olist e seus desafios", 2)
    b.body(doc, (
        "A Olist conecta pequenos e médios lojistas aos grandes marketplaces brasileiros. O enunciado do desafio lista oito frentes em que a empresa "
        "quer melhorar:"
    ))
    b.bullet(doc, "experiência do cliente;")
    b.bullet(doc, "eficiência logística;")
    b.bullet(doc, "retenção e fidelização;")
    b.bullet(doc, "gestão de avaliações;")
    b.bullet(doc, "eficiência operacional;")
    b.bullet(doc, "automação de processos;")
    b.bullet(doc, "apoio à tomada de decisão;")
    b.bullet(doc, "escalabilidade.")
    b.body(doc, "Este relatório é o primeiro passo de uma estratégia de IA agêntica que será construída ao longo das cinco fases do curso (FIAP, 2026).")
    titulo(doc, "1.2 A pergunta desta fase", 2)
    b.body(doc, "Como a Olist poderia utilizar IA Generativa e Agentes de IA para melhorar sua operação e seus indicadores de negócio?")
    titulo(doc, "1.3 Objetivos", 2)
    for t in ["Identificar, com dados, onde estão os principais problemas e oportunidades da Olist.",
              "Priorizar as oportunidades em que agentes de IA têm mais impacto.",
              "Propor um mapa de pelo menos três agentes, a arquitetura conceitual e os prompts de cada um.",
              "Definir os indicadores que vão medir o resultado e os riscos que precisam de controle."]:
        b.bullet(doc, t)
    titulo(doc, "1.4 Escopo", 2)
    b.body(doc, (
        "Esta fase é de diagnóstico e desenho. Nada é implementado: não há modelagem de banco de dados, integração por API nem protótipo. "
        "O monitoramento dos agentes aparece só como conceito na arquitetura. Os dados são públicos e vão de 2016 a 2018, então os achados são "
        "hipóteses fortes a validar em piloto, e não relações de causa."
    ))

    # ------------------------------------------------------------------ 2
    titulo(doc, "2. Dados e método")
    titulo(doc, "2.1 Fonte e período", 2)
    b.body(doc, (
        f"Usamos o Brazilian E-Commerce Public Dataset by Olist (OLIST, 2018), indicado pelo enunciado. São {meta['tabelas']} tabelas: oito citadas no "
        f"enunciado e uma de apoio. Elas cobrem {b.br_int(meta['pedidos'])} pedidos de {meta['clientes']:,} clientes".replace(",", ".") +
        f", com compras de {I['I02']['texto']}. As análises foram feitas em Python, em notebooks reproduzíveis. "
        "Cada número tem uma fórmula do Excel equivalente, que chegou ao mesmo valor."
    ))
    titulo(doc, "2.2 Tabelas e o que cada linha representa", 2)
    b.caption(doc, "Tabela 1. Tabelas do dataset, registros e granularidade.")
    b.table(doc, ["Tabela", "Registros", "1 linha representa"],
            [[r["tabela"], b.br_int(r["registros"]), r["granularidade"]] for r in o2["inventario"]], [3.4, 2.2, 10.4], size=8)
    b.source(doc, "Fonte: Elaboração própria a partir do dataset Olist (Kaggle).")
    b.body(doc, "O dicionário completo de tabelas e colunas está no Apêndice A.")
    titulo(doc, "2.3 Regras de qualidade", 2)
    b.body(doc, "Antes de calcular qualquer número, definimos oito regras que evitam erros de contagem comuns neste dataset (Tabela 2).")
    b.caption(doc, "Tabela 2. Regras de qualidade aplicadas.")
    b.table(doc, ["Regra", "Em linguagem simples", "Registros afetados"],
            [[r["id"], r["regra"], b.br_int(r["afetados"])] for r in o2["regras"]], [1.4, 11.6, 3.0], size=8)
    b.source(doc)
    titulo(doc, "2.4 Como lemos os achados", 2)
    b.body(doc, "Cada achado foi escrito em quatro partes:")
    b.bullet(doc, "**fato:** o que os números mostram;")
    b.bullet(doc, "**leitura:** o que o fato sugere;")
    b.bullet(doc, "**cautela:** o limite da conclusão;")
    b.bullet(doc, "**e daí?:** o que muda para a Olist.")
    b.body(doc, (
        f"Foram {len(o3['achados'])} análises, cobrindo as 8 dimensões do dataset. Como os dados são observacionais, o texto usa \"associado a\" e "
        "\"compatível com\", nunca \"causa\"."
    ))

    # ------------------------------------------------------------------ 3
    titulo(doc, "3. O que os dados mostram")
    afazer(doc, "OLIST-4", "Diogo", "Texto e números desta seção estão prontos. Falta trocar ou complementar as figuras pelos gráficos finais no padrão visual do relatório.")
    secoes = [
        ("3.1 Atraso e satisfação andam juntos", ["N1", "N2"], ("o3_n1_atraso_nota", "Percentual de notas 1 ou 2 por faixa de atraso.")),
        ("3.2 O que dizem os comentários negativos", ["N3"], ("o3_n3_temas_comentarios", "Temas dos comentários de avaliações com nota 1 ou 2.")),
        ("3.3 Em que etapa o atraso nasce", ["D1", "D2"], ("o3_d1_etapas_ciclo", "Tempo médio por etapa do ciclo do pedido.")),
        ("3.4 Onde e quando o atraso acontece", ["N6", "D6", "D5"], ("o3_d5_sazonalidade", "Pedidos entregues e taxa de atraso por mês.")),
        ("3.5 Produto, frete e forma de pagamento", ["D3", "D4"], None),
    ]
    n_fig, n_tab = 0, 2
    for tit, ids, f in secoes:
        titulo(doc, tit, 2)
        for i in ids:
            a = A[i]
            b.rich(b._para(doc, indent=True), f"**{a['titulo']}.** {a['fato']} {a['leitura']}")
            b.rich(b._para(doc, indent=True), f"*Cautela:* {a['cautela']} **E daí?** {a['e_dai']}".replace("*Cautela:*", "**Cautela:**"))
        if f:
            n_fig += 1
            b.figure(doc, n_fig, f[1], fig(f[0]), 14.0)
    titulo(doc, "3.6 Achados-chave", 2)
    b.body(doc, "A Tabela 3 resume os seis achados que orientam as oportunidades e os agentes, em ordem de relevância.")
    n_tab += 1
    b.caption(doc, f"Tabela {n_tab}. Achados-chave e desafios do enunciado.")
    b.table(doc, ["#", "Achado", "Evidência", "Desafios"],
            [[k["rank"], k["titulo"], k["resumo"], k["desafios"]] for k in o3["chave"]], [0.7, 3.6, 7.6, 4.1], size=8)
    b.source(doc)

    # ------------------------------------------------------------------ 4
    titulo(doc, "4. Análises complementares e limitações")
    titulo(doc, "4.1 Cancelamentos e recompra", 2)
    for i in ["N4", "N5"]:
        a = A[i]
        b.rich(b._para(doc, indent=True), f"**{a['titulo']}.** {a['fato']} {a['leitura']} **Cautela:** {a['cautela']}")
    titulo(doc, "4.2 Limitações dos dados", 2)
    for t in ["Os dados vão de 2016 a 2018; a operação atual pode ser diferente.",
              "Não há custos internos, transportadora, motivo de cancelamento nem registros de atendimento.",
              "Avaliações dependem de o cliente responder; comentários existem em só parte delas.",
              "Os temas dos comentários foram classificados por palavras-chave, de forma aproximada.",
              "Todos os achados são associações; o efeito real de cada agente só se mede em piloto."]:
        b.bullet(doc, t)

    # ------------------------------------------------------------------ 5
    titulo(doc, "5. Oportunidades e priorização")
    b.body(doc, "Proposta inicial de oportunidades, derivada dos achados-chave (Tabela 4):")
    n_tab += 1
    b.caption(doc, f"Tabela {n_tab}. Oportunidades candidatas e achado que as sustenta.")
    b.table(doc, ["#", "Oportunidade", "Achado que sustenta"],
            [[k["rank"], k["oportunidade"], k["titulo"]] for k in o3["chave"]], [0.7, 9.0, 6.3], size=8)
    b.source(doc)
    afazer(doc, "OLIST-5", "Lorran", "Matriz de priorização com critérios e pesos próprios (somando 100%), notas justificadas, 3–4 oportunidades escolhidas, descartadas com motivo e formato visual (heatmap ou quadrante).")

    # ------------------------------------------------------------------ 6
    titulo(doc, "6. Mapa de agentes")
    b.body(doc, (
        "Proposta inicial de três agentes, que cobrem o ciclo da entrega: o primeiro age antes do problema, o segundo depois da reclamação e o "
        "terceiro apoia quem decide (Tabela 5)."
    ))
    agentes = [
        ("Sentinela de Entregas", "Prevenir o atraso e avisar o cliente antes que ele aconteça",
         "Atraso associado a 62% de notas 1–2; postagem fora do prazo eleva o atraso de 5% para 21%",
         "Clientes, vendedores, time de operações", "Menos atrasos e menos notas negativas"),
        ("Voz do Cliente", "Ler, classificar, priorizar e encaminhar avaliações e reclamações",
         "10.838 comentários negativos sem leitura em escala; 45% sobre entrega, 32% sobre produto",
         "Atendimento (SAC), time de lojistas", "Resposta mais rápida e problemas recorrentes visíveis"),
        ("Copiloto Operacional", "Apoiar gestores com respostas, alertas e recomendações sobre atraso, vendedores e prazos",
         "Atraso concentrado em rotas longas, Norte e Nordeste, meses de pico e alguns vendedores",
         "Gestores de operações, logística e lojistas", "Decisões mais rápidas e prazos prometidos mais realistas"),
    ]
    n_tab += 1
    b.caption(doc, f"Tabela {n_tab}. Mapa de agentes: nome, objetivo, problema, usuários e benefício.")
    b.table(doc, ["Agente", "Objetivo", "Problema resolvido", "Usuários", "Benefício esperado"], [list(x) for x in agentes],
            [2.6, 3.6, 4.0, 2.9, 2.9], size=8)
    b.source(doc)
    afazer(doc, "OLIST-8", "Lorran", "Validar os agentes no Checkpoint 1, conferir que nome e escopo não repetem a referência e inserir o diagrama visual do mapa com os fluxos entre os agentes.")

    # ------------------------------------------------------------------ 7
    titulo(doc, "7. Fichas dos agentes: responsabilidades, limites e autonomia")
    fichas = [
        ("7.1 Sentinela de Entregas",
         "Monitora pedidos em andamento e age em sinais de risco: postagem após o prazo-limite, pedido parado no transporte além do normal para a rota, "
         "pedido de alto risco (outro estado, mais de 10 kg, Norte ou Nordeste, mês de pico). Cobra o vendedor, avisa o cliente com nova previsão e escala para a logística.",
         "Envia avisos padrão sozinho; compensação, cancelamento ou reembolso só com aprovação humana."),
        ("7.2 Voz do Cliente",
         "Classifica cada avaliação negativa por tema e urgência, rascunha a resposta, encaminha para a área certa e consolida os temas por vendedor e categoria.",
         "Classifica e sugere; no início, toda resposta ao cliente passa por aprovação humana."),
        ("7.3 Copiloto Operacional",
         "Responde perguntas dos gestores em linguagem natural, aponta vendedores com atraso acima do esperado, sugere prazo prometido por rota e peso e alerta antes das datas de pico.",
         "Só recomenda; toda decisão é humana."),
    ]
    for tit, faz, aut in fichas:
        titulo(doc, tit, 2)
        b.rich(b._para(doc, indent=True), f"**O que faz:** {faz}")
        b.rich(b._para(doc, indent=True), f"**Autonomia:** {aut}")
        afazer(doc, "OLIST-8", "Lorran", "Completar entradas e saídas (lista de campos), ferramentas futuras, o que o agente nunca faz, quando aciona humano e por que precisa de agente e não de regra simples.")

    # ------------------------------------------------------------------ 8
    titulo(doc, "8. Arquitetura conceitual")
    titulo(doc, "8.1 Diagrama", 2)
    afazer(doc, "OLIST-10", "Igor", "Diagrama em uma página com fontes de dados (tabelas usadas por agente), os três agentes, usuários, entradas e saídas rotuladas nas setas e interações entre agentes.")
    titulo(doc, "8.2 Fluxo das informações", 2)
    b.body(doc, (
        "Exemplo de fluxo entre os agentes: o Sentinela sinaliza um pedido em risco. O Voz do Cliente já recebe esse contexto quando o cliente reclama. "
        "Os temas por vendedor alimentam o Copiloto, que recalibra prazos e limites de risco usados pelo Sentinela."
    ))
    afazer(doc, "OLIST-10", "Igor", "Narrar de 6 a 8 passos de um pedido atrasado atravessando os agentes.")
    titulo(doc, "8.3 Governança, monitoramento e integrações futuras", 2)
    afazer(doc, "OLIST-10", "Igor", "Camada de governança com o ponto de aprovação humana; monitoramento dos agentes como conceito (ex.: LangSmith: execuções, custo, qualidade, escalonamentos); lista de integrações futuras.")

    # ------------------------------------------------------------------ 9
    titulo(doc, "9. Prompts estruturados")
    b.body(doc, "Cada agente tem ao menos um prompt com quatro blocos:")
    b.bullet(doc, "(a) objetivo;")
    b.bullet(doc, "(b) contexto fornecido;")
    b.bullet(doc, "(c) instrução principal, com papel, tarefa e formato de resposta;")
    b.bullet(doc, "(d) resultado esperado.")
    for i, (nome, *_r) in enumerate(agentes, start=1):
        titulo(doc, f"9.{i} Prompt · {nome}", 2)
        afazer(doc, "OLIST-9", "Lorran", "Prompt com os 4 blocos, regras para não inventar dados e escalar para humano, e um exemplo de entrada com registro real do dataset.")

    # ------------------------------------------------------------------ 10
    titulo(doc, "10. Impacto esperado e indicadores")
    b.body(doc, "Linhas de base medidas no dataset, que servirão de ponto de partida para os KPIs dos agentes (Tabela 6):")
    base = [
        ("Taxa de atraso", I["I05"]["texto"], "Sentinela, Copiloto"),
        ("% de notas 1–2 entre atrasados", b.br_pct(V(o3, "M01", "atrasados")), "Sentinela"),
        ("% de pedidos postados após o prazo-limite", b.br_pct(V(o3, "M07", "% postou fora do limite")), "Sentinela"),
        ("% de avaliações negativas", I["I08"]["texto"], "Voz do Cliente"),
        ("Nota média", I["I07"]["texto"], "Voz do Cliente"),
        ("Atraso na região Nordeste", b.br_pct(V(o3, "M06", "Nordeste")), "Copiloto"),
        ("Taxa de recompra", I["I12"]["texto"], "segunda onda (retenção)"),
    ]
    n_tab += 1
    b.caption(doc, f"Tabela {n_tab}. Linhas de base dos indicadores.")
    b.table(doc, ["Indicador", "Linha de base", "Agente"], [list(x) for x in base], [8.0, 3.5, 4.5])
    b.source(doc, "Fonte: Elaboração própria a partir do dataset Olist (Kaggle).")
    titulo(doc, "10.1 O que podemos e o que não podemos afirmar", 2)
    afazer(doc, "OLIST-6", "Diogo", "Cadeia problema → mudança no processo → indicador → resultado por agente; ≥ 2 KPIs por agente com fórmula e baseline; quadro \"pode afirmar / precisa de mais dados / só prova em operação\"; indicadores de saúde dos agentes.")

    # ------------------------------------------------------------------ 11
    titulo(doc, "11. Riscos, governança e autonomia")
    afazer(doc, "OLIST-8", "Lorran", "Tabela padronizada com ≥ 3 riscos por agente e mitigação (resposta inventada, viés, privacidade, autonomia excessiva, custo, adoção) e matriz de autonomia: faz sozinho / recomenda / exige aprovação humana.")

    # ------------------------------------------------------------------ 12
    titulo(doc, "12. Roadmap nas cinco fases")
    afazer(doc, "OLIST-6", "Diogo", "O que fazemos em cada fase (1 a 5), o que preservamos da Fase 1 e os critérios para avançar de uma fase para a outra.")

    # ------------------------------------------------------------------ 13
    titulo(doc, "13. Conclusão e recomendação")
    b.body(doc, (
        "Os dados apontam a entrega como o ponto de maior impacto na experiência do cliente da Olist. A recomendação é começar pelos agentes que agem "
        "antes do atraso e que dão escala à leitura das avaliações, sempre com aprovação humana nas ações que afetam o cliente."
    ))
    afazer(doc, "OLIST-6", "Diogo", "Fechar a conclusão com a recomendação de decisão para a diretoria, alinhada à matriz, aos KPIs e ao roadmap.")

    # ------------------------------------------------------------------ vídeo e referências
    titulo(doc, "Vídeo executivo")
    afazer(doc, "OLIST-4", "Diogo", "Inserir o link do vídeo (até 5 minutos), testado em janela anônima.")

    titulo(doc, "Referências")
    for ref in [
        "CHAPMAN, P. et al. CRISP-DM 1.0: step-by-step data mining guide. [S.l.]: SPSS, 2000.",
        "FIAP. Tech Challenge Agentic AI – Fase 1: Olist Intelligent Marketplace. São Paulo: FIAP, 2026. Enunciado da atividade.",
        "OLIST. Brazilian E-Commerce Public Dataset by Olist. Kaggle, 2018. Disponível em: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce. Acesso em: 26 out. 2026.",
        "TUKEY, J. W. Exploratory data analysis. Reading: Addison-Wesley, 1977.",
    ]:
        p = b._para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, line=1.0, after=12)
        b._font(p.add_run(ref), 11)

    # ------------------------------------------------------------------ apêndices
    p = b._para(doc); p.add_run().add_break(WD_BREAK.PAGE)
    titulo(doc, "Apêndice A – Dicionário de dados")
    overview, tabs = b.parse_dictionary()
    b.caption(doc, "Tabela A.1. Tabelas do dataset: o que é e para que serve.")
    b.table(doc, ["Tabela", "O que é", "Para que serve"],
            [[b.plain(b.re.sub(r"\s*\(.*?\)", "", r[0])).replace("**", ""), b.plain(r[1]), b.plain(r[4])] for r in overview], [3.2, 6.0, 6.8], size=8)
    b.source(doc)
    titulo(doc, "Apêndice B – Indicadores-base")
    b.caption(doc, "Tabela B.1. Indicadores-base: fórmula, origem e valor.")
    b.table(doc, ["ID", "Indicador", "Fórmula", "Origem", "Valor"],
            [[i["id"], i["nome"], i["formula"], i["tabelas"], i["texto"]] for i in o2["indicadores"]], [1.0, 3.6, 6.4, 2.8, 2.2], size=8)
    b.source(doc)

    doc.save(OUT)
    print("Word:", OUT)
    return OUT


def V(o3, metrica, rotulo):
    """Valor de uma métrica do OLIST-3 pelo rótulo da fórmula no Excel (ex.: V(o3, "M01", "no prazo"))."""
    return next(x for x in o3["metricas"] if x["id"] == metrica)["valores"][rotulo]


if __name__ == "__main__":
    build()
