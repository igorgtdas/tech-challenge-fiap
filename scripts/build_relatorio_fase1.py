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
    "4. Oportunidades e priorização", "5. Mapa de agentes",
    "6. Fichas dos agentes: responsabilidades, limites e autonomia", "6.1 [nome agente 1]", "6.2 [nome agente 2]", "6.3 [nome agente 3]",
    "7. Arquitetura conceitual", "7.1 Diagrama", "7.2 Fluxo das informações", "7.3 Governança, monitoramento e integrações futuras",
    "8. Prompts estruturados", "8.2 Prompt · [nome agente 1]", "8.3 Prompt · [nome agente 2]", "8.4 Prompt · [nome agente 3]",
    "9. Impacto esperado e indicadores", "9.1 O que podemos e o que não podemos afirmar",
    "10. Riscos, governança e autonomia", "11. Próximas fases", "12. Conclusão e recomendação", "Vídeo executivo",
}


def titulo(doc, text, level=1):
    """Título de seção (nível 1 em negrito; nível 2 em negrito itálico); vermelho se a seção ainda não está pronta."""
    p = b._para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, before=14 if level == 1 else 8, after=6, keep=True)
    b._font(p.add_run(text), 12 if level == 1 else 11, bold=True, italic=level == 2, color=RED if text in PENDENTES else None)
    return p


def afazer(doc, card, quem, texto, rotulo="A FAZER"):
    """Caixa vermelha de pendência: a que card se refere, quem é o responsável e o que falta (texto ou lista de linhas)."""
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
    b._font(p.add_run(f"{rotulo} · Card {card} · {quem}"), 10, bold=True, color=RED)
    for linha in ([texto] if isinstance(texto, str) else texto):
        p.add_run().add_break()
        b._font(p.add_run(linha), 10, color=RED)
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
        "meses de pico. Os comentários negativos falam principalmente de entrega e de produto. Recomendamos três agentes (a definir no mapa de agentes), "
        "com aprovação humana nas ações que afetam o cliente."
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

    n_tab = 2

    # ------------------------------------------------------------------ 4
    titulo(doc, "4. Oportunidades e priorização")
    b.body(doc, f"Proposta inicial de oportunidades, derivada dos achados-chave (Tabela {n_tab + 1}):")
    n_tab += 1
    b.caption(doc, f"Tabela {n_tab}. Oportunidades candidatas e achado que as sustenta.")
    b.table(doc, ["#", "Oportunidade", "Achado que sustenta"],
            [[k["rank"], k["oportunidade"], k["titulo"]] for k in o3["chave"]], [0.7, 9.0, 6.3], size=8)
    b.source(doc)
    afazer(doc, "OLIST-5", "Lorran", "Matriz de priorização com critérios e pesos próprios (somando 100%), notas justificadas, 3–4 oportunidades escolhidas, descartadas com motivo e formato visual (heatmap ou quadrante).")

    # ------------------------------------------------------------------ 5
    titulo(doc, "5. Mapa de agentes")
    b.body(doc, (
        "Esta seção é do card OLIST-8 (Lorran): a escolha e o desenho dos agentes são dele. Abaixo está a estrutura a preencher, com os campos "
        f"que o enunciado pede para cada agente (Tabela {n_tab + 1})."
    ))
    n_tab += 1
    b.caption(doc, f"Tabela {n_tab}. Mapa de agentes: nome, objetivo, problema, usuários e benefício.")
    b.table(doc, ["Agente", "Objetivo", "Problema resolvido", "Usuários", "Benefício esperado"],
            [[f"[nome agente {i}]", "", "", "", ""] for i in (1, 2, 3)], [2.8, 3.4, 3.8, 3.0, 3.0], size=8)
    b.source(doc)
    afazer(doc, "OLIST-8", "Lorran", [
        "Sugestão a partir dos achados (a decisão é do Lorran):",
        f"• Sentinela de Entregas: previne o atraso e avisa o cliente antes. Com atraso, {pct('M01', 'atrasados', 0)} de notas 1–2 contra {pct('M01', 'no prazo', 0)}; "
        f"postagem fora do prazo eleva o atraso de {pct('M07', 'atraso se postou no limite', 0)} para {pct('M07', 'atraso se postou fora', 0)}.",
        f"• Voz do Cliente: lê, classifica e encaminha avaliações. São {b.br_int(o3['comentarios_negativos'])} comentários negativos; "
        f"{pct('M03', 'entrega (qualquer)', 0)} falam de entrega e {pct('M03', 'produto (qualquer)', 0)} de produto.",
        f"• Copiloto Operacional: apoia os gestores com alertas e recomendações. O atraso é de {pct('M06', 'Nordeste')} no Nordeste e tem picos de "
        f"{pct('M11', 'nov/2017', 0)} a {pct('M11', 'mar/2018', 0)}.",
        "Falta: escolher os agentes, conferir que nome e escopo não repetem a referência e inserir o diagrama do mapa com os fluxos entre eles.",
    ], rotulo="SUGESTÃO E A FAZER")

    # ------------------------------------------------------------------ 6
    titulo(doc, "6. Fichas dos agentes: responsabilidades, limites e autonomia")
    afazer(doc, "OLIST-8", "Lorran", "Preencher uma ficha por agente. As entradas e saídas devem ser descritas como lista de campos, para reaproveitar na Fase 3.")
    campos = ["O que faz", "Entradas (campos)", "Saídas (campos)", "Ferramentas futuras", "O que nunca faz", "Quando aciona um humano",
              "Nível de autonomia", "Por que agente, e não regra simples"]
    for i in (1, 2, 3):
        titulo(doc, f"6.{i} [nome agente {i}]", 2)
        n_tab += 1
        b.caption(doc, f"Tabela {n_tab}. Ficha do [nome agente {i}].")
        b.table(doc, ["Campo", "Descrição"], [[c, ""] for c in campos], [5.0, 11.0], size=8)

    # ------------------------------------------------------------------ 7
    titulo(doc, "7. Arquitetura conceitual")
    titulo(doc, "7.1 Diagrama", 2)
    afazer(doc, "OLIST-10", "Igor", "Diagrama em uma página com fontes de dados (tabelas usadas por agente), os três agentes, usuários, entradas e saídas rotuladas nas setas e interações entre agentes.")
    titulo(doc, "7.2 Fluxo das informações", 2)
    b.body(doc, (
        "Exemplo de fluxo: o [nome agente 1] sinaliza um pedido em risco. O [nome agente 2] já recebe esse contexto quando o cliente reclama. "
        "Os temas consolidados alimentam o [nome agente 3], que recalibra os prazos e os limites de risco usados pelo [nome agente 1]."
    ))
    afazer(doc, "OLIST-10", "Igor", "Narrar de 6 a 8 passos de um pedido atrasado atravessando os agentes.")
    titulo(doc, "7.3 Governança, monitoramento e integrações futuras", 2)
    afazer(doc, "OLIST-10", "Igor", "Camada de governança com o ponto de aprovação humana; monitoramento dos agentes como conceito (ex.: LangSmith: execuções, custo, qualidade, escalonamentos); lista de integrações futuras.")

    # ------------------------------------------------------------------ 8
    titulo(doc, "8. Prompts estruturados")
    b.body(doc, (
        "Cada agente tem ao menos um prompt com os quatro blocos pedidos pelo enunciado: objetivo, contexto fornecido, instrução principal e resultado "
        "esperado. A seção 8.1 traz um modelo canônico para servir de base; as seções seguintes são para os prompts de cada agente."
    ))
    titulo(doc, "8.1 Modelo canônico de prompt", 2)
    modelo = [
        ("(a) Objetivo do prompt",
         "Fazer o [nome agente] [tarefa de negócio, ex.: identificar pedidos com risco de atraso e preparar o aviso ao cliente], para melhorar "
         "[KPI do agente, ex.: taxa de atraso e % de notas 1–2]."),
        ("(b) Contexto fornecido",
         "Dados do pedido vindos do dataset: [campos, ex.: order_id, data da compra, prazo prometido, data de postagem, prazo-limite do vendedor, "
         "UF do cliente e do vendedor, peso, status]. Regras do negócio: [ex.: prazo-limite de postagem; quem pode autorizar compensação]."),
        ("(c) Instrução principal",
         "Você é o [nome agente] da Olist. Sua tarefa é [tarefa]. Use apenas os dados fornecidos e não invente informações. Se faltar um dado "
         "necessário, responda \"dados insuficientes\" e encaminhe o caso para um humano. Nunca [limite, ex.: prometa reembolso ou cancele pedidos]. "
         "Responda no formato definido em (d)."),
        ("(d) Resultado esperado",
         "Saída em campos: [ex.: order_id; nível de risco (baixo, médio ou alto); motivo em uma frase; ação recomendada; mensagem ao cliente "
         "(até 3 linhas); precisa de humano (sim ou não)]."),
    ]
    n_tab += 1
    b.caption(doc, f"Tabela {n_tab}. Modelo canônico de prompt, nos quatro blocos do enunciado.")
    b.table(doc, ["Bloco", "Conteúdo"], [list(x) for x in modelo], [3.6, 12.4], size=8)
    b.source(doc)
    blocos = ["(a) Objetivo do prompt", "(b) Contexto fornecido", "(c) Instrução principal", "(d) Resultado esperado", "Exemplo de entrada (registro real do dataset)"]
    for i in (1, 2, 3):
        titulo(doc, f"8.{i + 1} Prompt · [nome agente {i}]", 2)
        n_tab += 1
        b.caption(doc, f"Tabela {n_tab}. Prompt do [nome agente {i}].")
        b.table(doc, ["Bloco", "Conteúdo"], [[c, ""] for c in blocos], [5.0, 11.0], size=8)
    afazer(doc, "OLIST-9", "Lorran", "Preencher um prompt por agente a partir do modelo 8.1, com um exemplo de entrada usando um registro real do dataset.")

    # ------------------------------------------------------------------ 9
    titulo(doc, "9. Impacto esperado e indicadores")
    b.body(doc, f"Linhas de base medidas no dataset, que servirão de ponto de partida para os KPIs dos agentes (Tabela {n_tab + 1}):")
    base = [
        ("Taxa de atraso", I["I05"]["texto"]),
        ("% de notas 1–2 entre atrasados", pct("M01", "atrasados")),
        ("% de pedidos postados após o prazo-limite", pct("M07", "% postou fora do limite")),
        ("% de avaliações negativas", I["I08"]["texto"]),
        ("Nota média", I["I07"]["texto"]),
        ("Atraso na região Nordeste", pct("M06", "Nordeste")),
        ("Taxa de recompra", I["I12"]["texto"]),
    ]
    n_tab += 1
    b.caption(doc, f"Tabela {n_tab}. Linhas de base dos indicadores.")
    b.table(doc, ["Indicador", "Linha de base", "Agente"], [[x, v, "[nome agente]"] for x, v in base], [8.0, 3.5, 4.5])
    b.source(doc, "Fonte: Elaboração própria a partir do dataset Olist (Kaggle).")
    titulo(doc, "9.1 O que podemos e o que não podemos afirmar", 2)
    afazer(doc, "OLIST-6", "Diogo", "Cadeia problema → mudança no processo → indicador → resultado por agente; ≥ 2 KPIs por agente com fórmula e baseline; quadro \"pode afirmar / precisa de mais dados / só prova em operação\"; indicadores de saúde dos agentes.")

    # ------------------------------------------------------------------ 10
    titulo(doc, "10. Riscos, governança e autonomia")
    afazer(doc, "OLIST-8", "Lorran", "Tabela padronizada com ≥ 3 riscos por agente e mitigação (resposta inventada, viés, privacidade, autonomia excessiva, custo, adoção) e matriz de autonomia: faz sozinho / recomenda / exige aprovação humana.")

    # ------------------------------------------------------------------ 11
    titulo(doc, "11. Próximas fases")
    b.body(doc, (
        "O enunciado prevê que o projeto evolua ao longo da Postech e seja reaproveitado nas fases seguintes (FIAP, 2026), e a evolução do projeto "
        f"é um dos critérios de avaliação. A Tabela {n_tab + 1} indica o que deste relatório segue para cada fase."
    ))
    fases = [
        ("Fase 2", "Estruturar casos de uso e desenho dos agentes"),
        ("Fase 3", "Construir protótipos e validar soluções"),
        ("Fase 4", "Orquestrar múltiplos agentes e automações"),
        ("Fase 5", "Estruturar governança, liderança e escala corporativa"),
    ]
    n_tab += 1
    b.caption(doc, f"Tabela {n_tab}. Próximas fases e o que este relatório leva para cada uma.")
    b.table(doc, ["Fase", "Foco no enunciado", "O que este relatório leva"], [[f, foco, ""] for f, foco in fases], [2.0, 7.0, 7.0], size=8)
    b.source(doc, "Fonte: Elaboração própria a partir do enunciado (FIAP, 2026).")
    afazer(doc, "OLIST-6", "Diogo", "Preencher a última coluna: o que segue de cada parte deste relatório (achados, agentes, KPIs, arquitetura) para cada fase.")

    # ------------------------------------------------------------------ 12
    titulo(doc, "12. Conclusão e recomendação")
    b.body(doc, (
        "Os dados apontam a entrega como o ponto de maior impacto na experiência do cliente da Olist. A recomendação é começar pelos agentes que agem "
        "antes do atraso e que dão escala à leitura das avaliações, sempre com aprovação humana nas ações que afetam o cliente."
    ))
    afazer(doc, "OLIST-6", "Diogo", "Fechar a conclusão com a recomendação de decisão para a diretoria, alinhada à matriz, aos KPIs e às próximas fases.")

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
