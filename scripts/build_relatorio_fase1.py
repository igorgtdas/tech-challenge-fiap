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
    "Sumário Executivo", "3. Principais achados",
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
    pct = lambda m, r, d=1: b.br_pct(V(o3, m, r), d)  # noqa: E731
    dias = lambda m, r: b.br_num(V(o3, m, r), 1)  # noqa: E731

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
        f"Analisamos {b.br_int(I['I01']['valor'])} pedidos da Olist ({I['I02']['texto']}) e encontramos um eixo claro: a entrega. "
        f"Com atraso, {pct('M01', 'atrasados')} dos clientes dão nota 1 ou 2; no prazo, {pct('M01', 'no prazo')}. O atraso dá sinais antes de acontecer, "
        "porque se forma no transporte e na postagem fora do prazo pelo vendedor. Ele se concentra em rotas longas, no Norte e no Nordeste e em poucos "
        "meses de pico. Os comentários negativos falam principalmente de entrega e de produto. Recomendamos três agentes, com aprovação humana nas ações "
        "que afetam o cliente: um que previne o atraso, um que lê e encaminha as avaliações e um copiloto para os gestores."
    ))
    afazer(doc, "OLIST-7", "Diogo", "Fechar o sumário (até 1 página) depois de prontos os agentes, os KPIs e o roadmap; incluir 3–5 números de destaque do OLIST-4.")

    # ------------------------------------------------------------------ 1
    titulo(doc, "1. Contexto, pergunta e escopo")
    b.body(doc, (
        "A Olist conecta pequenos e médios lojistas aos grandes marketplaces brasileiros. Ela quer melhorar a experiência do cliente, a logística, "
        "a retenção, a gestão de avaliações, a eficiência operacional, a automação, o apoio à decisão e a escalabilidade (FIAP, 2026). "
        "A pergunta desta fase é: como a Olist poderia utilizar IA Generativa e Agentes de IA para melhorar sua operação e seus indicadores de negócio?"
    ))
    b.body(doc, (
        "O objetivo é identificar com dados onde estão os problemas, priorizar as oportunidades e propor agentes, arquitetura, prompts, indicadores e riscos. "
        "Esta fase é de diagnóstico e desenho: nada é implementado (sem banco de dados, API ou protótipo), e o monitoramento dos agentes aparece só como conceito."
    ))

    # ------------------------------------------------------------------ 2
    titulo(doc, "2. Dados e método")
    b.body(doc, (
        f"Usamos o dataset público da Olist no Kaggle (OLIST, 2018): {meta['tabelas']} tabelas e {b.br_int(meta['pedidos'])} pedidos de "
        f"{b.br_int(meta['clientes'])} clientes. As análises foram feitas em Python, e cada número tem uma fórmula do Excel equivalente, que chegou ao "
        f"mesmo valor. Fizemos {len(o3['achados'])} análises, cobrindo as 8 dimensões do dataset. Como os dados são observacionais, os achados são "
        "associações, não relações de causa. Antes de calcular qualquer número, aplicamos oito regras de qualidade (Tabela 1). O dicionário de dados está no Apêndice A."
    ))
    regras_curtas = {
        "R1": "Pedido é contado pelo order_id, não pelas linhas de itens",
        "R2": "Cliente é a pessoa (customer_unique_id), não o cadastro do pedido",
        "R3": "Uma avaliação por pedido: a mais recente",
        "R4": "Atraso só para pedidos entregues, com as datas preenchidas",
        "R5": "Vazio continua vazio: nunca vira zero",
        "R6": "Datas incoerentes ficam fora dos prazos",
        "R7": "Geolocalização reduzida a 1 ponto por CEP",
        "R8": "Valor do pedido = soma dos pagamentos",
    }
    b.caption(doc, "Tabela 1. Regras de qualidade aplicadas.")
    b.table(doc, ["Regra", "O que garante", "Registros afetados"],
            [[r["id"], regras_curtas[r["id"]], b.br_int(r["afetados"])] for r in o2["regras"]], [1.4, 11.0, 3.6], size=8)
    b.source(doc)

    # ------------------------------------------------------------------ 3
    titulo(doc, "3. Principais achados")
    afazer(doc, "OLIST-4", "Diogo", "Texto e números desta seção estão prontos. Falta trocar ou complementar as figuras pelos gráficos finais no padrão visual do relatório.")
    b.body(doc, "A Tabela 2 reúne os achados mais relevantes, em ordem de importância para a escolha dos agentes. Em seguida, cada tema é resumido.")
    b.caption(doc, "Tabela 2. Achados mais relevantes e desafios do enunciado.")
    b.table(doc, ["#", "Achado", "Evidência nos dados", "Desafios"],
            [[k["rank"], k["titulo"], k["resumo"], k["desafios"]] for k in o3["chave"]], [0.7, 3.6, 7.6, 4.1], size=8)
    b.source(doc)

    titulo(doc, "3.1 A entrega concentra a insatisfação", 2)
    b.body(doc, (
        f"Com atraso, {pct('M01', 'atrasados')} dos clientes dão nota 1 ou 2; no prazo, {pct('M01', 'no prazo')} (Figura 1). Os atrasados são "
        f"{pct('M02', 'atrasados no total')} dos pedidos entregues, mas concentram {pct('M02', 'de atrasados')} das notas negativas. O atraso se forma no transporte: "
        f"{dias('M07', 'transporte · atrasados')} dias nos atrasados, contra {dias('M07', 'transporte · no prazo')} nos demais, com um prazo prometido parecido "
        f"para os dois grupos. Também dá sinal cedo: quando o vendedor posta depois do prazo-limite ({pct('M07', '% postou fora do limite')} dos pedidos), "
        f"o atraso sobe de {pct('M07', 'atraso se postou no limite')} para {pct('M07', 'atraso se postou fora')}. "
        f"Entre os vendedores com 50 ou mais entregas, {pct('M08', '% (50+ entregas) com 2× a média', 0)} atrasam o dobro da média ou mais."
    ))
    b.figure(doc, 1, "Percentual de notas 1 ou 2 por faixa de atraso.", fig("o3_n1_atraso_nota"), 12.0)

    titulo(doc, "3.2 Onde e quando o atraso acontece", 2)
    b.body(doc, (
        f"O atraso é de {pct('M06', 'Nordeste')} no Nordeste e {pct('M06', 'Norte')} no Norte, contra {pct('M06', 'Sudeste')} no Sudeste. Quando vendedor e "
        f"cliente estão em estados diferentes, {pct('M12', 'atraso · outra UF')}; no mesmo estado, {pct('M12', 'atraso · mesma UF')}. No tempo, há picos: "
        f"{pct('M11', 'nov/2017')} na Black Friday de 2017 e {pct('M11', 'mar/2018')} em março de 2018, contra cerca de 4% nos meses normais (Figura 2). "
        "Nesses meses, a nota média também cai."
    ))
    b.figure(doc, 2, "Pedidos entregues e taxa de atraso por mês.", fig("o3_d5_sazonalidade"), 13.0)

    titulo(doc, "3.3 O que o cliente escreve", 2)
    b.body(doc, (
        f"Há {b.br_int(o3['comentarios_negativos'])} comentários em avaliações com nota 1 ou 2. Pela classificação por palavras-chave, "
        f"{pct('M03', 'entrega (qualquer)', 0)} falam de entrega e {pct('M03', 'produto (qualquer)', 0)} de produto errado, incompleto ou com defeito. "
        "É um volume de texto em português que hoje não tem leitura em escala, um caso típico para IA generativa."
    ))

    titulo(doc, "3.4 Outros sinais", 2)
    b.body(doc, (
        f"Pedidos acima de 10 kg atrasam {pct('M09', 'atraso · mais de 10 kg')}, contra {pct('M09', 'atraso · até 0,5 kg')} nos de até 0,5 kg. "
        f"O peso do frete no valor quase não muda a nota (diferença de {b.br_num(V(o3, 'M10', 'diferença q1 − q5'))} ponto). "
        f"Cancelamentos são raros ({pct('M04', 'cancelados + indisponíveis')}), mas {pct('M04', '% que já estava aprovado', 0)} deles acontecem depois do pagamento aprovado. "
        f"A recompra é baixa ({pct('M05', 'recompra geral')}) e quase igual com nota boa ({pct('M05', '1ª compra nota 4-5')}) ou ruim "
        f"({pct('M05', '1ª compra nota 1-2')}) na primeira compra, o que indica que retenção pede ação ativa."
    ))

    # ------------------------------------------------------------------ 4
    titulo(doc, "4. Limitações")
    b.body(doc, (
        "Os dados vão de 2016 a 2018 e não trazem custos, transportadora, motivo de cancelamento nem registros de atendimento. As avaliações dependem de o "
        "cliente responder, e os temas dos comentários foram classificados de forma aproximada. Por isso, os achados são hipóteses fortes, e o efeito de cada "
        "agente só se mede em piloto."
    ))
    n_tab = 2

    # ------------------------------------------------------------------ 5
    titulo(doc, "5. Oportunidades e priorização")
    b.body(doc, f"Proposta inicial de oportunidades, derivada dos achados-chave (Tabela {n_tab + 1}):")
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
        f"terceiro apoia quem decide (Tabela {n_tab + 1})."
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
    b.body(doc, f"Linhas de base medidas no dataset, que servirão de ponto de partida para os KPIs dos agentes (Tabela {n_tab + 1}):")
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

    doc.save(OUT)
    print("Word:", OUT)
    return OUT


def V(o3, metrica, rotulo):
    """Valor de uma métrica do OLIST-3 pelo rótulo da fórmula no Excel (ex.: V(o3, "M01", "no prazo"))."""
    return next(x for x in o3["metricas"] if x["id"] == metrica)["valores"][rotulo]


if __name__ == "__main__":
    build()
