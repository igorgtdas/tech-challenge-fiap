# Plano de Execução — Tech Challenge FIAP Fase 1 (Olist)

**Equipe:** Igor (OLIST-2, 3, 10) · Lorran (OLIST-5, 8, 9) · Diogo (OLIST-4, 6, 7)  **Sprint:** 26/10 a 02/11/2026  **Entrega:** 03/11/2026

## Contexto

O grupo precisa entregar o Tech Challenge Agentic AI – Fase 1 (Olist), que vale 90% da nota da fase. O relatório de outra equipe (`Tech_Challenge_FIAP_Fase_1_Olist_Relatorio_Executivo.pdf`) serve de **referência de lógica e estrutura**, mas o nosso texto, as nossas escolhas e o nosso visual precisam ser próprios para não configurar plágio. Este documento é o backlog do Jira em Markdown: método, cronograma, épico e cards. O enunciado pede 5 entregáveis, todos reunidos em **um único relatório executivo**.

O cronograma em Gantt também está publicado como página interativa (link enviado no chat).

---

# PARTE 1 — Como ler o desafio (método)

## 1.1 Método em 5 passos ("Leitura em camadas")

1. **Separar o que é pergunta, entrega e nota.** Ler o enunciado três vezes, cada uma com um foco:
   - *Passada 1 — Pergunta:* "Como a Olist poderia usar IA Generativa e Agentes de IA para melhorar operação e indicadores?" Tudo deve responder a isso.
   - *Passada 2 — Entregáveis:* lista fechada de 5 itens (seção 1.2).
   - *Passada 3 — Critérios de avaliação:* 10 critérios (seção 1.3). É aqui que está a nota.
2. **Sublinhar os verbos obrigatórios.** "Sempre expliquem: problema, benefício, impacto esperado, usuários, riscos" → esses 5 itens precisam aparecer **para cada agente**. "Pelo menos 3 agentes", "pelo menos 1 prompt por agente", "até 5 min de vídeo", "10–20 páginas (sugestão)".
3. **Ler as restrições (o que NÃO fazer).** Foco não é técnico; sem programação avançada; mapa, arquitetura e prompts ficam **dentro** do relatório; vídeo entra como **link** no relatório; linguagem de diretoria.
4. **Montar uma matriz rastreável:** requisito do enunciado → onde aparece no relatório → critério de nota atendido → responsável → critério de aceite (seção 2). Se um requisito não tem dono, ele some.
5. **Definir uma espinha narrativa única** e fazer todas as seções obedecerem a ela:
   `problema → evidência no dataset → agente → impacto esperado → indicador → risco/controle`
   Isso garante coerência (critério "Visão estratégica") e evita um relatório que é só um monte de tabelas.

## 1.2 Entregáveis extraídos do enunciado

| # | Entregável | Obrigatório | Onde vive |
|---|---|---|---|
| 1 | Relatório executivo (problemas/oportunidades, análises no dataset, sugestões de IA, impacto) — 10–20 pág. | Sim | Documento principal |
| 2 | Mapa de agentes (≥3; nome, objetivo, problema resolvido, usuários, benefício) | Sim | **Dentro** do relatório |
| 3 | Arquitetura conceitual (fontes, agentes, usuários, entradas/saídas, interações) | Sim | **Dentro** do relatório |
| 4 | Prompts estruturados (≥1 por agente: objetivo, contexto, instrução principal, resultado esperado) | Sim | **Dentro** do relatório |
| 5 | Vídeo executivo (≤5 min, ≥1 apresentador, linguagem de diretoria) | Sim | **Link** dentro do relatório |

**Fora do escopo da Fase 1 (nada é desenvolvido agora):** modelagem de banco de dados, APIs e integrações, código dos agentes, protótipos, testes em ferramentas de IA e configuração de ferramenta de monitoramento (o monitoramento entra só como conceito, em OLIST-6 e OLIST-10). O enunciado diz que "não é esperado desenvolvimento técnico avançado"; isso fica para as Fases 3 (protótipos) e 4 (orquestração). Nesta fase, a única mão na massa é **analisar o dataset** (pedido literal do relatório), usando planilha. Arquitetura e prompts são **desenho conceitual**, escrito no relatório.

## 1.3 Os 10 critérios de avaliação → como cada um é atendido

| Critério FIAP | Como atendemos | Cards |
|---|---|---|
| 1. Visão estratégica | Espinha narrativa + matriz de priorização ligando IA a indicador de negócio | OLIST-5 |
| 2. Conectar IA ao negócio | Cada agente amarrado a problema real e KPI | OLIST-5, OLIST-6, OLIST-8 |
| 3. Capacidade analítica | Análises reproduzíveis sobre os CSVs, com regras de qualidade | OLIST-2, OLIST-3 |
| 4. Profundidade / qualidade dos insights | Recortes por segmento, separar fato × hipótese, não afirmar causalidade | OLIST-3 |
| 5. Estruturação executiva | Sumário executivo na abertura, uma mensagem por seção | OLIST-4, OLIST-7 |
| 6. Clareza para executivos | Linguagem sem jargão, poucas tabelas densas, "e daí?" em cada insight, vídeo para diretoria | OLIST-4, OLIST-7 |
| 7. Qualidade visual | Gráficos, diagramas, identidade visual única | OLIST-4, OLIST-7, OLIST-10 |
| 8. Organização/padronização | Template de seção, termos normalizados, checklist FIAP | OLIST-7 |
| 9. Criatividade e inovação | Recorte analítico próprio + diferencial de agente/arquitetura (seção 1.5) | OLIST-3, OLIST-8, OLIST-10 |
| 10. Evolução do projeto | Roadmap das 5 fases e decisões que serão preservadas | OLIST-6 |

## 1.4 O que aprendemos com o relatório de referência

**Estrutura que vale reaproveitar (lógica):**
Sumário executivo → Contexto/pergunta/escopo → Metodologia e regras de qualidade → Análises quantitativas → Limitações → Matriz de priorização → Mapa de agentes → Especificação (autonomia/limites) → Arquitetura em camadas → Prompts → KPIs → Riscos e matriz de autonomia → Roadmap 5 fases → Conclusão.

**Boas práticas dele que devemos manter (são o que dá qualidade):** separar fato × inferência × hipótese; contar pedido por `order_id`; agregar reviews por pedido antes de cruzar; não confundir recompra com churn; não afirmar causalidade; humano aprova qualquer ação que afete cliente/dinheiro/pedido.

**Lacunas dele que podemos superar (ganho de nota):**
- Sem gráficos (critério 7 pede qualidade visual) — o nosso terá.
- Diagrama de arquitetura só em tabela — o nosso será desenho de verdade.
- Mapa de agentes em tabela — o nosso será visual.
- Vídeo "não incluído" — o nosso precisa ter link.
- Análise geográfica só com 5 estados e sem recorte por categoria/vendedor/frete.
- Linguagem de "documento de trabalho"; o enunciado pede tom de consultoria para diretoria.

## 1.5 Regras anti-plágio (como ser "diferente" mantendo a lógica)

| Pode manter | Deve mudar |
|---|---|
| Ordem lógica das seções e a espinha problema→agente→KPI | Todo o texto: redação própria, escrita do zero (não parafrasear frase a frase) |
| Tipos de análise (atraso, nota, reviews, recompra, estados) | **Rodar nós mesmos** os cálculos nos CSVs; não copiar números do PDF. Se coincidirem, tudo bem — o método é nosso e documentado |
| Quantidade mínima de 3 agentes | Nomes, personas, escopo e fronteiras dos agentes; sugerido trocar ao menos 1 (ex.: trocar "Apoio ao Atendimento" por **Agente de Retenção/Pós-venda**, ou manter e adicionar um 4º) — **decisão do grupo em OLIST-8** |
| Princípio "humano aprova ação externa" | Pesos e critérios da matriz de priorização, escala, nomes dos critérios |
| Conceito de camadas na arquitetura | Desenho, nomes das camadas, exemplos de fluxo |
| Prompt com papel/tarefa/formato | Redação e estrutura dos prompts (sugestão: formato XML/seções diferente do dele), exemplos próprios |
| — | Identidade visual (paleta, tipografia, capa, ícones), títulos de seção, exemplos e analogias |
| — | Acrescentar ao menos **2 análises que ele não fez** (ver OLIST-3) |

> Regra prática de revisão: nenhuma frase de 8+ palavras igual à do PDF; nenhuma tabela com a mesma ordem de linhas e colunas; nenhuma figura com o mesmo desenho.

## 1.6 Metodologia de execução: orientada a hipóteses (como uma consultoria)

Em vez de esperar os dados ficarem prontos para só então pensar em agentes (cascata), o grupo trabalha **em paralelo desde o início**:

1. **Hipóteses primeiro (Onda 1):** Lorran lista oportunidades candidatas a partir dos 8 desafios do enunciado e rascunha os agentes candidatos; Igor prepara e valida os dados e começa o esqueleto da arquitetura; Diogo monta o template do relatório e adianta o roadmap. Ninguém fica parado esperando.
2. **Checkpoint 1 — os dados confirmam ou derrubam as hipóteses:** reunião curta em que os indicadores do Igor mantêm, ajustam ou descartam cada oportunidade e cada agente candidato.
3. **Aprofundar só o que sobreviveu (Onda 2):** matriz final, agentes finais, prompts, arquitetura.
4. **Checkpoint 2 — revisão cruzada:** cada pessoa revisa o card de outra contra os critérios de aceite.
5. **Integrar e comunicar (Ondas 3–4):** relatório, gráficos, vídeo.

Gestão: quadro Kanban simples (A fazer → Fazendo → Em revisão → Concluído); card só entra em "Concluído" com todos os critérios marcados e revisão de outra pessoa.

---

# PARTE 2 — Cronograma da sprint (26/10 a 02/11, entrega em 03/11)

## 2.1 Calendário

| Seg 26 | Ter 27 | Qua 28 | Qui 29 | Sex 30 | Sáb 31 | Dom 01 | Seg 02 | Ter 03 |
|---|---|---|---|---|---|---|---|---|
| Kickoff | ◆ Checkpoint 1 (noite) | | | ◆ Checkpoint 2 (noite) | carga leve | carga leve | **Finados (feriado)** = folga e revisão final | **ENTREGA** |

## 2.2 Gantt (█ = trabalho · ◆ = marco · ▲ = entrega que bloqueia outra pessoa)

| Card | Resp. | Prior. | 26 | 27 | 28 | 29 | 30 | 31 | 01 | 02 |
|---|---|---|---|---|---|---|---|---|---|---|
| Kickoff (30–60 min) | Todos | — | ◆ | | | | | | | |
| OLIST-7a Template visual | Diogo | Média | █ | | | | | | | |
| OLIST-2 Dados e indicadores-base | Igor | **Alta** | █ | █▲ | | | | | | |
| OLIST-5 Oportunidades e matriz | Lorran | Média | █ rasc. | █ rasc. | █ final | | | | | |
| OLIST-8 Agentes, autonomia e riscos | Lorran | **Alta** | █ rasc. | █ rasc.▲ | █ final | █ final | | | | |
| ◆ Checkpoint 1: fechar lista de agentes | Todos | — | | ◆ | | | | | | |
| OLIST-3 Insights e análises | Igor | **Alta** | | █ | █ | █▲ | | | | |
| OLIST-9 Prompts estruturados | Lorran | Média | | █ estrutura | █ | █ | █ revisão | | | |
| OLIST-10 Arquitetura conceitual | Igor | Média | █ esqueleto | | | █ | █ | | | |
| OLIST-6 Impacto, KPIs e roadmap | Diogo | Média | | █ roadmap | █ | █ | █ | | | |
| OLIST-4a Gráficos e anexo | Diogo | Média | | | | █ | █ | | | |
| OLIST-7b Montagem do relatório | Diogo | Média | | | | █ seções | █ seções | █ v1 | █ v2 | |
| ◆ Checkpoint 2: revisão cruzada | Todos | — | | | | | ◆ | | | |
| OLIST-4b Vídeo (roteiro → gravação → link) | Diogo | **Alta** | | | | | █ roteiro | █ gravação | █ edição | |
| Revisão anti-plágio + checklist FIAP | Igor (conduz) | Média | | | | | | █ | █ | |
| Folga: PDF final, teste do link | Todos | — | | | | | | | | █ |

## 2.3 O que roda em paralelo e o que bloqueia

**Em paralelo (a maior parte):** dados (Igor), oportunidades e agentes (Lorran) e template e roadmap (Diogo) começam juntos no dia 26, cada um partindo do enunciado. De 28 a 30, os três trabalham em frentes independentes: insights e arquitetura (Igor), agentes e prompts (Lorran), KPIs e gráficos (Diogo).

**Bloqueios entre pessoas (só 3), todos com prioridade Alta:**

| # | Quem entrega | O quê | Até | Quem fica esperando | Por que não dá para evitar | Como reduzir o impacto |
|---|---|---|---|---|---|---|
| 1 | Igor | Indicadores-base (OLIST-2) | 27, 18h | Checkpoint 1 → todos | Sem dados não dá para validar as hipóteses | Priorizar só 6 números: atraso, nota × atraso, % com comentário, cancelamento, recompra, atraso por UF |
| 2 | Lorran | Lista final de agentes (OLIST-8) | 27, noite | Diogo (KPIs, OLIST-6), Igor (arquitetura, OLIST-10) | KPI e arquitetura são por agente | Decisão tomada na reunião do Checkpoint 1; Diogo adianta o roadmap e Igor o esqueleto da arquitetura, que não dependem dos agentes |
| 3 | Igor | Achados-chave (OLIST-3) | 29, 12h | Diogo (gráficos, OLIST-4) | Os gráficos mostram esses achados | Igor manda os achados assim que ficam prontos, um a um; Diogo começa pelo gráfico de atraso × nota, que já sai dos indicadores-base |

O template e os gráficos, e o vídeo e a versão final do relatório, ficaram com a mesma pessoa (Diogo), então deixaram de ser bloqueios entre pessoas.

O que **não** bloqueia (e não deve virar espera):
- Montagem: Diogo vai encaixando cada seção no relatório assim que ela fica pronta (29–30), sem esperar todas.
- Prompts e arquitetura: Lorran começa a estrutura dos prompts e Igor o esqueleto da arquitetura com os agentes candidatos; após o Checkpoint 1, só ajustam.
- Matriz: os rascunhos de oportunidades e agentes não dependem de dados.

## 2.4 Balanceamento de carga (estimativa)

| Pessoa | Cards | Horas estimadas | Pico |
|---|---|---|---|
| Igor | OLIST-2 (6h), OLIST-3 (7h), OLIST-10 com monitoramento (8h) + revisão anti-plágio/checklist (3h) | ~24h | 26 a 29 |
| Lorran | OLIST-5 (5h), OLIST-8 (10h), OLIST-9 (7h) | ~22h | 26 a 30 |
| **Diogo** | OLIST-4 gráficos (5h) + vídeo (5h), OLIST-6 (5h), OLIST-7 template (1h) + montagem (11h) | **~27h** | **30 a 01** |

**Ponto de atenção:** de 30/10 a 01/11, o Diogo acumula a montagem do relatório e o vídeo. Para aliviar sem trocar cards:
- Igor conduz a revisão anti-plágio e o checklist FIAP (31–01), porque termina os cards dele no dia 30.
- Lorran revisa o roteiro e apresenta no vídeo a parte dos agentes, que são dele (sugestão: dois apresentadores).
- Diogo adianta o template (26) e o roadmap (27), que não dependem de ninguém.

As horas são estimativas para comparar a carga entre as pessoas; o grupo ajusta no kickoff.

---

# PARTE 3 — Épico e cards (formato Jira)

## ÉPICO OLIST-1 — Tech Challenge Fase 1: Relatório Executivo de IA Agêntica para a Olist

**Objetivo:** entregar um relatório executivo único (10–20 págs.) que responda "como a Olist pode usar IA Generativa e Agentes para melhorar operação e indicadores", contendo análises do dataset, mapa de ≥3 agentes, arquitetura conceitual, prompts por agente e link para vídeo de ≤5 min.

**Valor:** 90% da nota da fase; base reutilizada nas Fases 2–5.

**Definição de pronto do épico:**
- [ ] Os 5 entregáveis presentes (4 dentro do relatório + link do vídeo)
- [ ] Os 10 critérios de avaliação com evidência identificável
- [ ] Cada agente tem problema, benefício, impacto, usuários e riscos explícitos
- [ ] Todos os números reproduzíveis a partir dos CSVs
- [ ] Revisão anti-plágio feita (seção 1.5)
- [ ] Relatório entre 10 e 20 páginas, padrão visual único

**Responsáveis:** cada pessoa escolheu os seus 3 cards.

| Pessoa | Cards |
|---|---|
| Igor | OLIST-2 Dataset e indicadores · OLIST-3 Insights · OLIST-10 Arquitetura conceitual |
| Lorran | OLIST-5 Oportunidades e matriz · OLIST-8 Mapa de agentes e riscos · OLIST-9 Prompts |
| Diogo | OLIST-4 Gráficos e vídeo · OLIST-6 Impacto, KPIs e roadmap · OLIST-7 Montagem do relatório |

Os cards continuam organizados em 3 frentes de trabalho (Dados 2–4, Estratégia 5–7, Agentes 8–10), porque os cards de uma mesma frente se conectam. Cada frente agora tem mais de um responsável; o card diz quem faz.

**Regra de "uma fonte só"** (evita texto duplicado no relatório):
- Problema, objetivo, usuários, benefício, limites, **autonomia** e **riscos** de cada agente → só no OLIST-8 (Lorran)
- Impacto esperado, KPIs, roadmap e conclusão → só no OLIST-6 (Diogo)
- Por que priorizar cada oportunidade → só em OLIST-5

---

## Como ler os critérios de aceite dos cards

Cada critério é **binário** (cumpriu ou não cumpriu) e traz a **origem** entre colchetes, para sabermos o que estamos cobrindo:

- `[ENUNC]` = exigência literal do enunciado da FIAP
- `[FIAP-n]` = critério de avaliação número n (seção 1.3)
- `[QUAL]` = padrão de qualidade combinado pelo grupo (evita erro ou plágio)

Um card só vai para "Concluído" quando **todos** os itens estão marcados e outra pessoa do grupo revisou.

---

## FRENTE DADOS — Dados, Análises e Comunicação visual · Responsáveis: Igor (OLIST-2, 3) e Diogo (OLIST-4) · Cards: OLIST-2, OLIST-3, OLIST-4

### OLIST-2 · Dados — Preparar e validar o dataset e os indicadores-base
- **Responsável:** Igor
- **Prioridade:** **Alta** (bloqueia o Checkpoint 1) · **Datas:** 26 → 27 (indicadores-base até 27, 18h)
- **Tipo:** Story · **Onda:** 1 · **Depende de:** — · **Bloqueia:** OLIST-3, OLIST-5
- **Objetivo:** preparar o dataset da Olist e calcular os números básicos que todas as análises do relatório vão usar: total de pedidos, pedidos atrasados, notas das avaliações, avaliações com comentário, cancelamentos e clientes que compraram de novo.
- **O que o enunciado pede:** o relatório deve apresentar "análises realizadas no dataset" (p. 7), usando o dataset público da Olist e suas 8 tabelas (pp. 3–4). O grupo é avaliado pela "capacidade analítica" (critério 3, p. 5).
- **O que fazer:**
  - Baixar os 9 CSVs do Kaggle; inventariar tabelas, registros, granularidade e chaves. (Enunciado, pp. 3–4)
  - Definir regras de qualidade: contar pedido por `order_id`; agregar reviews por pedido; atraso = `delivered` com data real e estimada preenchidas; nulos não viram zero; geolocalização deduplicada por CEP. (Definição do grupo)
  - Calcular indicadores-base: pedidos, entregues válidos, taxa e média de atraso, distribuição de notas, % de reviews com comentário, cancelados/indisponíveis, recompra por `customer_unique_id`. (Enunciado, p. 7)
  - Entregar planilha com a fórmula de cada número. (Definição do grupo)
  - Ferramenta: Excel ou Google Sheets bastam, sem programação. A tabela `geolocation` tem ~1 milhão de linhas (no limite do Excel); se nenhuma análise usar coordenadas, use o estado do cliente (`customers`) e deixe essa tabela de fora. (Enunciado, pp. 4 e 7)
- **Critérios de aceite:**
  - [ ] CA1 `[FIAP-3]` As 8 tabelas citadas no enunciado (customers, orders, order_items, payments, order_reviews, products, sellers, geolocation) estão inventariadas com nº de registros e granularidade
  - [ ] CA2 `[FIAP-3]` Existe uma lista escrita de ≥ 6 regras de qualidade, em linguagem simples
  - [ ] CA3 `[FIAP-3]` A planilha traz ≥ 10 indicadores, cada um com definição, fórmula e tabela de origem
  - [ ] CA4 `[QUAL]` Um colega (Diogo ou Lorran) reproduziu ≥ 3 indicadores e os valores bateram
  - [ ] CA5 `[FIAP-3]` O período coberto (datas inicial e final) e o nº de pedidos estão declarados
  - [ ] CA6 `[QUAL]` Nenhum número foi copiado do relatório de referência; todos saem dos CSVs
- **Conexão com o restante:** alimenta OLIST-3 (análises) e OLIST-5 (a "evidência" da matriz). A seção "Metodologia" do relatório (OLIST-7) sai daqui.

### OLIST-3 · Dados — Gerar insights e análises de profundidade
- **Responsável:** Igor
- **Prioridade:** **Alta** (os achados-chave liberam os gráficos do Diogo) · **Datas:** 27 → 29 (achados-chave até 29, 12h)
- **Tipo:** Story · **Onda:** 2 · **Depende de:** OLIST-2 · **Bloqueia:** OLIST-4 (Diogo, gráficos); alimenta OLIST-5 e OLIST-6 sem bloqueá-los (eles usam os indicadores-base de OLIST-2)
- **Objetivo:** transformar os números do dataset em achados de negócio que mostrem onde estão os problemas e as oportunidades da Olist (por exemplo, se pedidos atrasados recebem notas piores). São esses achados que justificam a escolha dos agentes.
- **O que o enunciado pede:** o relatório deve trazer os "principais problemas ou oportunidades identificadas" e as "análises realizadas no dataset" (p. 7). O grupo é avaliado pela "profundidade das análises e qualidade dos insights" (critério 4, p. 5).
- **O que fazer:**
  - Análises "núcleo": atraso × nota; distribuição de notas; temas em comentários negativos; cancelamentos; recompra; atraso por estado. (Enunciado, pp. 2 e 7)
  - Análises diferenciais (≥ 2): atraso por categoria e por vendedor (concentração); frete/valor/peso × nota; tempo por etapa do ciclo (aprovação → postagem → entrega); atraso por faixa de dias × nota; sazonalidade mensal. (Enunciado, p. 5)
  - Para cada achado, escrever: **Fato · Leitura · Cautela · E daí?** (Enunciado, p. 5)
  - Eleger 4–6 achados principais, em ordem de relevância para os agentes. (Enunciado, p. 7)
- **Critérios de aceite:**
  - [ ] CA1 `[ENUNC]` As análises são feitas **no dataset** (exigência do relatório) e cobrem ≥ 5 das dimensões listadas no enunciado (clientes, pedidos, pagamentos, produtos, logística, vendedores, avaliações, geolocalização) — o mínimo de 5 é meta do grupo
  - [ ] CA2 `[FIAP-4]` ≥ 6 análises no total, das quais ≥ 2 são diferenciais (não existem no relatório de referência)
  - [ ] CA3 `[FIAP-4]` Todas trazem Fato, Leitura, Cautela e "E daí?" preenchidos
  - [ ] CA4 `[FIAP-4]` Nenhuma frase afirma causalidade; usa "associado a", "compatível com"
  - [ ] CA5 `[FIAP-2]` Cada um dos 4–6 achados-chave aponta qual dos desafios do enunciado ele ilustra (cliente, logística, retenção, reviews, eficiência, automação, decisão, escala)
  - [ ] CA6 `[QUAL]` Todo número tem fórmula na planilha de OLIST-2
  - [ ] CA7 `[QUAL]` Lista dos achados-chave entregue ao Diogo (gráficos e KPIs) e ao Lorran (oportunidades e agentes)
- **Conexão com o restante:** insumo direto da matriz (OLIST-5), dos KPIs/impacto (OLIST-6) e dos gráficos (OLIST-4).

### OLIST-4 · Dados — Comunicação visual: gráficos, anexo metodológico e vídeo executivo
- **Responsável:** Diogo
- **Prioridade:** Média (gráficos) · **Alta** (vídeo, bloqueia a versão final) · **Datas:** gráficos 29 → 30 · vídeo: roteiro 30, gravação 31, edição e link até 01 à noite
- **Tipo:** Story · **Onda:** 3 (gráficos) → 4 (vídeo) · **Depende de:** OLIST-3 e template de OLIST-7 (gráficos); conteúdo revisado no Checkpoint 2 (vídeo) · **Bloqueia:** OLIST-7 (final)
- **Objetivo:** apresentar os achados de forma visual no relatório (gráficos e números de destaque) e gravar o vídeo executivo, de até 5 minutos, que apresenta o projeto à diretoria da Olist.
- **O que o enunciado pede:** o vídeo é o entregável 5: até 5 minutos, ao menos um integrante apresentando, linguagem executiva, link dentro do relatório (p. 11). O relatório deve ser "visualmente organizado" (p. 6), e o grupo é avaliado pela "qualidade visual" (critério 7, p. 5).
- **O que fazer:**
  - 5–7 gráficos legíveis para executivos; título que diz a conclusão. (Enunciado, pp. 5–6)
  - 3–5 "números de destaque" para o sumário executivo. (Enunciado, p. 7)
  - Anexo: dicionário de dados resumido, regras de qualidade, limitações do dataset. (Definição do grupo)
  - Exportar em alta resolução no padrão visual do template (OLIST-7). (Enunciado, p. 5)
  - **Vídeo:** roteiro (problema → achados → agentes → impacto → riscos → próximo passo), slides de apoio opcionais (o enunciado permite), gravação, upload e inserção do link no relatório (OLIST-7). Sugestão: Diogo apresenta e Lorran apresenta a parte dos agentes; os três revisam o roteiro. (Enunciado, p. 11)
- **Critérios de aceite — gráficos e anexo:**
  - [ ] CA1 `[FIAP-7]` 5 a 7 gráficos prontos; cada um com título-conclusão, fonte e legenda
  - [ ] CA2 `[FIAP-6]` Cada gráfico passa no "teste dos 5 segundos": um leigo entende a mensagem sem explicação
  - [ ] CA3 `[FIAP-8]` Paleta e tipografia idênticas ao template do relatório
  - [ ] CA4 `[FIAP-5]` Entregues 3–5 números de destaque para o sumário executivo
  - [ ] CA5 `[FIAP-4]` O anexo declara limitações: dados de 2016–2018, sem custos internos, sem dados de atendimento, comentários em apenas parte das avaliações
  - [ ] CA6 `[QUAL]` Nenhum gráfico replica o desenho de figuras do relatório de referência
  - [ ] CA7 `[QUAL]` Arquivos em PNG/SVG nomeados por seção, prontos para o relatório (OLIST-7)
- **Critérios de aceite — vídeo:**
  - [ ] CA8 `[ENUNC]` Duração de até 5 minutos
  - [ ] CA9 `[ENUNC]` Pelo menos 1 integrante aparece apresentando
  - [ ] CA10 `[ENUNC]` Linguagem executiva, sem termos excessivamente técnicos, pensada para a diretoria da Olist
  - [ ] CA11 `[ENUNC]` Explica claramente os problemas e oportunidades identificados
  - [ ] CA12 `[QUAL]` Roteiro segue a mesma espinha narrativa do relatório e usa os mesmos números
  - [ ] CA13 `[QUAL]` Link testado em janela anônima (acesso liberado) e inserido no relatório (OLIST-7)
- **Conexão com o restante:** gráficos e link do vídeo entram no relatório (OLIST-7, também do Diogo); os números de destaque abrem o sumário executivo e o vídeo.

---

## FRENTE ESTRATÉGIA — Estratégia, Impacto e Integração · Responsáveis: Lorran (OLIST-5) e Diogo (OLIST-6, 7) · Cards: OLIST-5, OLIST-6, OLIST-7

### OLIST-5 · Estratégia — Oportunidades e matriz de priorização
- **Responsável:** Lorran
- **Prioridade:** Média (rascunho precisa estar pronto para o Checkpoint 1) · **Datas:** rascunho 26 → 27 · final 28
- **Tipo:** Story · **Onda:** 1 (rascunho, sem dados) → 2 (final) · **Depende de:** rascunho: nada; final: indicadores-base de OLIST-2 · **Bloqueia:** nada (é insumo do Checkpoint 1)
- **Objetivo:** listar as oportunidades de uso de IA Generativa e de agentes para os desafios da Olist e escolher, com critérios claros, quais serão atacadas primeiro. A escolha define quais agentes serão propostos.
- **O que o enunciado pede:** a Fase 1 existe para "identificar oportunidades iniciais de aplicação de IA Generativa e Agentes de IA" (p. 6). O relatório deve trazer os "principais problemas ou oportunidades" e as "sugestões iniciais de uso de IA" (p. 7), a partir dos desafios da Olist listados no contexto (p. 2). O grupo é avaliado pela "visão estratégica" (critério 1, p. 5).
- **O que fazer:**
  - Rascunho (Onda 1): listar 6–8 oportunidades candidatas a partir dos desafios do enunciado e usar como base dos agentes candidatos (OLIST-8). (Enunciado, p. 2)
  - Definir nossa matriz (critérios, pesos e escala próprios). (Enunciado, p. 5)
  - Final (Onda 2): pontuar com os dados do Igor, justificar cada nota em uma frase, escolher 3–4 vencedoras e indicar o que fica para segunda onda. (Enunciado, p. 7)
  - Para cada vencedora: problema, evidência nos dados, usuários impactados e por que priorizar (benefício, impacto e riscos detalhados ficam em OLIST-6 e OLIST-8 — regra de "uma fonte só"). (Enunciado, pp. 6–7)
- **Critérios de aceite:**
  - [ ] CA1 `[FIAP-1]` As oportunidades cobrem os 8 desafios citados no contexto do enunciado (experiência do cliente, eficiência logística, retenção, reviews, eficiência operacional, automação, apoio à decisão, escalabilidade) — cada um aparece em ≥ 1 oportunidade ou tem justificativa de exclusão
  - [ ] CA2 `[FIAP-1]` Matriz com critérios e pesos que somam 100%, e justificativa dos pesos
  - [ ] CA3 `[ENUNC]` Cada oportunidade escolhida cita ≥ 1 achado de OLIST-3 como evidência (o relatório pede "problemas ou oportunidades identificadas" a partir das análises)
  - [ ] CA4 `[ENUNC]` Cada oportunidade escolhida tem problema, evidência, usuários impactados e justificativa de prioridade
  - [ ] CA5 `[QUAL]` Notas identificadas como julgamento do grupo, não resultado estatístico
  - [ ] CA6 `[QUAL]` Oportunidades descartadas listadas com motivo
  - [ ] CA7 `[QUAL]` Pesos, nomes de critérios e escala diferentes da referência
  - [ ] CA8 `[FIAP-7]` Matriz apresentada em formato visual (heatmap, quadrante ou bolhas), não só tabela
  - [ ] CA9 `[QUAL]` Rascunho pronto antes do Checkpoint 1
- **Conexão com o restante:** define quais agentes serão especificados no OLIST-8; alimenta a seção "Oportunidades" do relatório.

### OLIST-6 · Estratégia — Impacto esperado, KPIs, roadmap e conclusão
- **Responsável:** Diogo
- **Prioridade:** Média · **Datas:** roadmap 27 (não depende de agentes) · KPIs e impacto 28 → 30
- **Tipo:** Story · **Onda:** 2 → 3 · **Depende de:** OLIST-2 (baselines), lista de agentes do Checkpoint 1 · **Bloqueia:** nada — a própria frente encaixa no relatório (OLIST-7)
- **Objetivo:** explicar o impacto que cada agente deve gerar no negócio da Olist, dizer como esse impacto será medido (indicadores) e mostrar como o projeto evolui nas próximas fases do curso.
- **O que o enunciado pede:** o relatório deve trazer o "impacto esperado para o negócio" (p. 7), e as orientações gerais pedem para sempre explicar "o impacto esperado" (p. 6). O grupo é avaliado pela "evolução do projeto" ao longo das 5 fases (critério 10, p. 5).
- **O que fazer:**
  - Para cada agente, escrever a cadeia: problema → mudança no processo → indicador → resultado de negócio. (Enunciado, pp. 6–7)
  - Definir KPIs com fórmula, fonte e baseline (quando existir no dataset; senão "medir no piloto"). (Enunciado, p. 5)
  - Separar o que **pode ser afirmado** com o dataset, o que exige mais dados e o que só se prova em operação real. (Definição do grupo)
  - Incluir 2–3 indicadores de saúde dos agentes, que o monitoramento (OLIST-10) acompanharia: qualidade das respostas, % de casos escalados para humano e custo por atendimento. (Definição do grupo)
  - Roadmap das Fases 1–5 (o monitoramento entra quando houver protótipo, na Fase 3, e vira rotina na Fase 5); conclusão e recomendação final. (Enunciado, pp. 2 e 5)
  - (Riscos e autonomia ficam no OLIST-8, do Lorran; aqui só se referencia.)
- **Critérios de aceite:**
  - [ ] CA1 `[ENUNC]` Cada agente tem impacto esperado para o negócio descrito e ≥ 2 KPIs com fórmula (o mínimo de 2 é meta do grupo)
  - [ ] CA2 `[ENUNC]` Cada agente tem o benefício traduzido em resultado de negócio pela cadeia completa (problema → mudança no processo → indicador → resultado)
  - [ ] CA3 `[ENUNC]` Os usuários envolvidos de cada agente estão citados e consistentes com o mapa de agentes (OLIST-8)
  - [ ] CA4 `[QUAL]` Nenhuma meta numérica (ex.: "reduzir 20%") sem baseline ou rotulada como hipótese
  - [ ] CA5 `[FIAP-4]` Há quadro "pode afirmar / precisa de mais dados / só prova em operação"
  - [ ] CA6 `[FIAP-10]` Roadmap cobre as 5 fases com o que fazemos em cada uma e o que preservamos da Fase 1
  - [ ] CA7 `[FIAP-1]` Conclusão traz uma recomendação clara de decisão para a diretoria
  - [ ] CA8 `[FIAP-8]` KPIs em tabela padronizada (mesmas colunas para todos os agentes)
- **Conexão com o restante:** usa achados (OLIST-3) e agentes (OLIST-8); alimenta sumário executivo e conclusão.

### OLIST-7 · Estratégia — Integração do relatório e qualidade final
- **Responsável:** Diogo
- **Prioridade:** Média (template e montagem; os gráficos e o vídeo são do mesmo responsável) · **Datas:** template 26 · seções 29 → 30 · v1 31 · v2 com link 01 · PDF final 02
- **Tipo:** Story · **Onda:** 0 (template) → 3 (montagem) → 4 (final) · **Depende de:** cada seção entra quando fica pronta (OLIST-4, 6, 9, 10), sem esperar todas · **Bloqueia:** entrega do épico
- **Objetivo:** montar o relatório executivo final, que reúne todas as partes do trabalho (análises, oportunidades, mapa de agentes, arquitetura, prompts e link do vídeo) e responde à pergunta da Fase 1.
- **O que o enunciado pede:** o relatório executivo é o entregável 1, com 10 a 20 páginas sugeridas (p. 7). Mapa de agentes, arquitetura, prompts e vídeo "devem estar inseridos dentro do relatório" (pp. 9 e 11). A pergunta a responder está na p. 7. O grupo é avaliado por "estruturação executiva" e por "organização, padronização e profissionalismo" (critérios 5 e 8, p. 5).
- **O que fazer:**
  - Criar o template visual (capa, paleta, tipografia) na Onda 0 e distribuir. (Enunciado, pp. 5–6)
  - Montar o relatório: capa, sumário executivo, contexto, método, análises, oportunidades, agentes, arquitetura, prompts, impacto/KPIs/riscos, roadmap, conclusão, link do vídeo, referências, anexo. (Enunciado, pp. 7–11)
  - Usar o relatório montado como base do roteiro do vídeo (OLIST-4) e inserir o link. (Enunciado, p. 11)
  - Revisão cruzada anti-plágio e checklist FIAP. (Enunciado, p. 5)
- **Critérios de aceite:**
  - [ ] CA1 `[ENUNC]` Relatório feito em Word, Google Docs, Notion, Canva Docs ou similar, com 10 a 20 páginas (faixa sugerida pelo enunciado)
  - [ ] CA2 `[ENUNC]` O relatório responde, de forma explícita, à pergunta "Como a Olist poderia utilizar IA Generativa e Agentes de IA para melhorar sua operação e seus indicadores de negócio?" no sumário e na conclusão
  - [ ] CA3 `[ENUNC]` O relatório contém: principais problemas ou oportunidades, análises realizadas no dataset, sugestões iniciais de uso de IA e impacto esperado para o negócio
  - [ ] CA4 `[ENUNC]` O mapa de agentes está **dentro** do relatório
  - [ ] CA5 `[ENUNC]` A arquitetura conceitual está **dentro** do relatório
  - [ ] CA6 `[ENUNC]` Os prompts estão **dentro** do relatório
  - [ ] CA7 `[ENUNC]` O link do vídeo está **dentro** do relatório e abre
  - [ ] CA8 `[FIAP-5]` Sumário executivo de ≤ 1 página, com recomendação e 3–5 números de destaque
  - [ ] CA9 `[FIAP-8]` Padrão visual único: mesma fonte, cores, estilo de título, legendas e numeração em todo o documento
  - [ ] CA10 `[FIAP-6]` Revisão de linguagem: nenhum termo técnico sem explicação; cada seção abre com uma frase-conclusão
  - [ ] CA11 `[QUAL]` Revisão anti-plágio feita por quem não escreveu o trecho (regra da seção 1.5); sem frases de 8+ palavras iguais às do PDF de referência
  - [ ] CA12 `[QUAL]` Checklist dos 10 critérios FIAP (seção 1.3) preenchido, com a página onde cada um é atendido
  - [ ] CA13 `[QUAL]` Sem texto de rascunho, "TODO", placeholders ou tabelas quebradas entre páginas
  - [ ] CA14 `[FIAP-9]` Há ao menos 3 elementos de diferenciação identificados (ex.: análises diferenciais, agente diferente, visuais próprios)
  - [ ] CA15 `[QUAL]` Capa com os nomes dos integrantes; referências citam o enunciado FIAP e o dataset Olist (Kaggle) com link
- **Conexão com o restante:** ponto de integração de todos os cards; entrega final.

---

## FRENTE AGENTES — Agentes, Riscos, Prompts e Arquitetura · Responsáveis: Lorran (OLIST-8, 9) e Igor (OLIST-10) · Cards: OLIST-8, OLIST-9, OLIST-10

### OLIST-8 · Agentes — Mapa de agentes, fichas, autonomia e riscos
- **Responsável:** Lorran
- **Prioridade:** **Alta** (a lista de agentes bloqueia KPIs, prompts e arquitetura) · **Datas:** rascunho 26 → 27 · lista fechada no Checkpoint 1 (27 à noite) · fichas, mapa e riscos 28 → 29
- **Tipo:** Story · **Onda:** 1 (rascunho, sem dados) → 2 (final) · **Depende de:** rascunho: só o enunciado; final: Checkpoint 1 · **Bloqueia:** OLIST-6 (Diogo), OLIST-9 (Lorran) e OLIST-10 (Igor)
- **Objetivo:** propor pelo menos 3 agentes de IA para a Olist e apresentá-los num mapa visual, com nome, objetivo, problema resolvido, usuários e benefício de cada um, além dos riscos. É desenho no papel: nada é construído nesta fase.
- **O que o enunciado pede:** o mapa de agentes é o entregável 2, com no mínimo 3 agentes e esses 5 campos para cada um (p. 8), dentro do relatório (p. 9). As orientações gerais pedem para sempre explicar "os riscos" (p. 6).
- **O que fazer:**
  - Rascunho (Onda 1): agentes candidatos a partir dos desafios do enunciado (junto com o rascunho de oportunidades do OLIST-5); levar ao Checkpoint 1. (Enunciado, p. 2)
  - Riscos de cada agente com mitigação (resposta inventada, viés, privacidade, autonomia excessiva, custo, adoção). (Enunciado, p. 6)
  - Decidir com o grupo os agentes finais (sugestão de diferencial: um agente de retenção/pós-venda ou de apoio à decisão para gestores). (Enunciado, p. 8)
  - Ficha por agente com os 5 campos do enunciado + quais dados usa, o que entrega, limites e quando chama humano. (Enunciado, p. 8)
  - Desenhar o mapa visual (Miro/Draw.io/Canva). (Enunciado, p. 8)
  - Justificar por que cada caso precisa de agente e não de regra simples. (Enunciado, pp. 6–7)
  - Definir nível de autonomia de cada agente. (Enunciado, p. 4)
- **Critérios de aceite:**
  - [ ] CA1 `[ENUNC]` ≥ 3 agentes definidos
  - [ ] CA2 `[ENUNC]` Cada agente tem, preenchidos: nome, objetivo, problema resolvido, usuários envolvidos, benefício esperado
  - [ ] CA3 `[ENUNC]` Mapa em diagrama simples e organizado, pouco texto, legível em uma página
  - [ ] CA4 `[ENUNC]` O mapa está dentro do relatório (imagem pronta para OLIST-7)
  - [ ] CA5 `[FIAP-1]` Cada agente está ligado a uma oportunidade da matriz de OLIST-5 e a um achado de OLIST-3
  - [ ] CA6 `[FIAP-2]` Cada agente tem um KPI de negócio associado (definido com o Diogo, no OLIST-6)
  - [ ] CA7 `[QUAL]` Cada agente tem limites explícitos: o que nunca faz e quando aciona humano
  - [ ] CA8 `[QUAL]` Justificativa "agente × regra simples × IA Generativa" para cada caso
  - [ ] CA9 `[FIAP-9]` Nomes, escopo e fronteiras dos agentes não repetem os da referência (ao menos 1 agente diferente)
  - [ ] CA10 `[QUAL]` Sem sobreposição: nenhuma responsabilidade pertence a dois agentes
  - [ ] CA11 `[ENUNC]` O mapa organiza visualmente os fluxos entre os agentes (boa prática pedida no enunciado)
  - [ ] CA12 `[QUAL]` Matriz de autonomia (faz sozinho / recomenda / exige aprovação humana) definida aqui
  - [ ] CA13 `[QUAL]` Entradas e saídas de cada agente descritas em linguagem de negócio (quais dados usa e o que entrega), sem detalhe técnico
  - [ ] CA14 `[ENUNC]` Cada agente tem seus riscos explicados, com mitigação (meta do grupo: ≥ 3 por agente), em tabela padronizada
- **Conexão com o restante:** origem de prompts (OLIST-9), arquitetura (OLIST-10) e KPIs (OLIST-6); a tabela de riscos entra direto no relatório; é o escopo que as próximas fases vão detalhar.

### OLIST-9 · Agentes — Prompts estruturados por agente
- **Responsável:** Lorran
- **Prioridade:** Média · **Datas:** estrutura padrão 27 · prompts 28 → 29 · revisão 30
- **Tipo:** Story · **Onda:** 2 · **Depende de:** lista de agentes do Checkpoint 1 (a estrutura começa antes) · **Bloqueia:** nada — entra no relatório quando fica pronto
- **Objetivo:** escrever, para cada agente do mapa, pelo menos um prompt estruturado que traduza o problema de negócio em instruções claras para a IA: o que o agente deve fazer, com quais informações e que resposta deve entregar.
- **O que o enunciado pede:** os prompts são o entregável 4: ao menos 1 por agente, com (a) objetivo, (b) contexto fornecido, (c) instrução principal e (d) resultado esperado (pp. 9–10), seguindo as boas práticas de clareza e alinhamento ao negócio (pp. 10–11), dentro do relatório (p. 11).
- **O que fazer:**
  - 1 prompt completo por agente com os 4 blocos: (a) objetivo do prompt, (b) contexto fornecido, (c) instrução principal, (d) resultado esperado. (Enunciado, pp. 9–10)
  - Regras anti-alucinação e de escalonamento para humano. (Enunciado, pp. 10–11)
  - 1 exemplo de entrada e saída por agente usando registros reais do dataset (que já é anonimizado), por exemplo uma review negativa real. (Enunciado, p. 10)
- **Critérios de aceite:**
  - [ ] CA1 `[ENUNC]` ≥ 1 prompt por agente do mapa (nenhum agente sem prompt)
  - [ ] CA2 `[ENUNC]` Cada prompt tem os blocos (a) objetivo, (b) contexto fornecido, (c) instrução principal, (d) resultado esperado, claramente identificados
  - [ ] CA3 `[ENUNC]` A instrução principal inclui: papel do agente, tarefa a executar e tipo de resposta esperada
  - [ ] CA4 `[ENUNC]` O formato de saída está definido (campos ou lista)
  - [ ] CA5 `[ENUNC]` Linguagem clara e sem ambiguidade; sem prompts excessivamente técnicos
  - [ ] CA6 `[QUAL]` O prompt proíbe inventar dados e diz o que fazer quando faltar informação
  - [ ] CA7 `[QUAL]` Cada prompt mostra um exemplo de entrada (registro real do dataset) e a saída esperada
  - [ ] CA8 `[QUAL]` Redação própria e estrutura diferente da referência
  - [ ] CA9 `[FIAP-8]` Os prompts seguem o mesmo bloco visual (mesmo layout para todos)
  - [ ] CA10 `[ENUNC]` Cada prompt está alinhado ao objetivo de negócio: o bloco (a) cita o problema e o KPI do agente (boa prática pedida no enunciado)
- **Conexão com o restante:** usa os limites de OLIST-8; entra no relatório (OLIST-7); um exemplo pode ser mostrado no vídeo.

### OLIST-10 · Agentes — Arquitetura conceitual (diagrama)
- **Responsável:** Igor
- **Prioridade:** Média · **Datas:** esqueleto 26 · diagrama final 29 → 30
- **Tipo:** Story · **Onda:** 2 · **Depende de:** lista de agentes do Checkpoint 1; o esqueleto (fontes, usuários, camadas) começa no dia 26 · **Bloqueia:** nada — entra no relatório quando fica pronto
- **Objetivo:** desenhar a arquitetura conceitual da solução: de onde vêm os dados, quais agentes existem, quem os usa, que informação entra e sai de cada um e como os agentes conversam entre si, sem detalhe técnico.
- **O que o enunciado pede:** a arquitetura conceitual é o entregável 3: fontes de dados, agentes, usuários, entradas e saídas e interações entre agentes, sem "detalhamento técnico avançado" (p. 9), dentro do relatório (p. 9).
- **O que fazer:**
  - Diagrama (Draw.io/Miro/Figma) com fontes de dados, agentes, usuários, entradas/saídas e interações entre agentes. (Enunciado, p. 9)
  - Camada de governança (humano decide, registros, privacidade). (Enunciado, pp. 4 e 6)
  - Camada de **monitoramento (observabilidade) dos agentes**: registrar cada execução (o que entrou, o que o agente respondeu, quem aprovou), acompanhar qualidade, custo e erros, e coletar o feedback de quem usa. Citar uma ferramenta como exemplo, como o **LangSmith** (ou o Langfuse, alternativa aberta), deixando claro que a escolha e a configuração ficam para as Fases 3–5. (Definição do grupo)
  - Fluxo narrado de 6–8 passos com um pedido atrasado atravessando os agentes. (Enunciado, p. 9)
  - Uma frase sobre o que precisaria ser conectado no futuro (sem modelagem de banco nem API: isso é das próximas fases). (Enunciado, pp. 7 e 9)
- **Critérios de aceite:**
  - [ ] CA1 `[ENUNC]` O diagrama mostra as **fontes de dados** (as tabelas do dataset usadas por cada agente)
  - [ ] CA2 `[ENUNC]` O diagrama mostra **todos os agentes** do mapa, com os mesmos nomes de OLIST-8
  - [ ] CA3 `[ENUNC]` O diagrama mostra os **usuários envolvidos**
  - [ ] CA4 `[ENUNC]` As **entradas e saídas de informação** estão rotuladas nas setas
  - [ ] CA5 `[ENUNC]` As **interações entre agentes** estão explícitas (quem passa o quê para quem)
  - [ ] CA6 `[ENUNC]` Sem detalhamento técnico avançado; legível em uma página por não técnico
  - [ ] CA7 `[ENUNC]` O diagrama está dentro do relatório (imagem pronta para OLIST-7)
  - [ ] CA8 `[FIAP-1]` Há camada de governança visível, com o ponto de aprovação humana
  - [ ] CA9 `[QUAL]` Exemplo narrado de ponta a ponta com um caso concreto
  - [ ] CA10 `[FIAP-9]` Desenho original: camadas, ordem e visual diferentes da referência
  - [ ] CA11 `[QUAL]` O diagrama mostra a camada de monitoramento ligada a todos os agentes, explicada em uma frase de negócio ("acompanhar se os agentes acertam, quanto custam e onde erram"), sem detalhe técnico
- **Conexão com o restante:** deriva de OLIST-8; a camada de governança reflete os riscos e a autonomia de OLIST-8; insumo para o vídeo.

---

## Matriz de rastreabilidade — nada do enunciado fica sem dono

Esta tabela usa só exigências **literais** do enunciado. Se uma linha não tiver card e critério, o requisito está descoberto.

| Requisito do enunciado | Card | Critério de aceite |
|---|---|---|
| **Entregável 1 — Relatório executivo** (Word/Docs/Notion/Canva; 10–20 págs. sugeridas) | OLIST-7 | CA1 |
| Responder à pergunta da Fase 1 | OLIST-7 | CA2 |
| Principais problemas ou oportunidades identificadas | OLIST-5, OLIST-7 | OLIST-5 CA3, CA4 · OLIST-7 CA3 |
| Análises realizadas no dataset | OLIST-3, OLIST-7 | OLIST-3 CA1 · OLIST-7 CA3 |
| Sugestões iniciais de uso de IA | OLIST-7, OLIST-8 | OLIST-8 CA1, CA8 · OLIST-7 CA3 |
| Impacto esperado para o negócio | OLIST-6, OLIST-7 | OLIST-6 CA1 · OLIST-7 CA3 |
| **Entregável 2 — Mapa de agentes:** ≥ 3 agentes | OLIST-8 | CA1 |
| Nome, objetivo, problema resolvido, usuários, benefício de cada agente | OLIST-8 | CA2 |
| Diagrama simples, fluxos organizados, pouco texto, clareza executiva | OLIST-8 | CA3, CA11 |
| Mapa dentro do relatório | OLIST-7, OLIST-8 | OLIST-8 CA4 · OLIST-7 CA4 |
| **Entregável 3 — Arquitetura:** fontes de dados | OLIST-10 | CA1 |
| Agentes propostos | OLIST-10 | CA2 |
| Usuários envolvidos | OLIST-10 | CA3 |
| Entradas e saídas de informação | OLIST-10 | CA4 |
| Possíveis interações entre agentes | OLIST-10 | CA5 |
| Sem detalhamento técnico avançado | OLIST-10 | CA6 |
| Arquitetura dentro do relatório | OLIST-7, OLIST-10 | OLIST-10 CA7 · OLIST-7 CA5 |
| **Entregável 4 — Prompts:** ≥ 1 por agente | OLIST-9 | CA1 |
| Blocos (a) objetivo, (b) contexto, (c) instrução, (d) resultado esperado | OLIST-9 | CA2 |
| Instrução com papel, tarefa e tipo de resposta | OLIST-9 | CA3 |
| Formato de resposta definido; linguagem clara, sem ambiguidade | OLIST-9 | CA4, CA5 |
| Prompt alinhado ao objetivo de negócio | OLIST-9 | CA10 |
| Prompts dentro do relatório | OLIST-7 | CA6 |
| **Entregável 5 — Vídeo:** até 5 min | OLIST-4 | CA8 |
| ≥ 1 integrante apresentando | OLIST-4 | CA9 |
| Linguagem executiva, sem termos técnicos excessivos, para a diretoria | OLIST-4 | CA10 |
| Explica problemas e oportunidades | OLIST-4 | CA11 |
| Link do vídeo dentro do relatório | OLIST-7 | CA7 |
| **Orientação geral:** explicar problema, benefício, impacto, usuários e riscos | OLIST-6, OLIST-8 | OLIST-8 CA2 (problema, usuários, benefício), CA14 (riscos) · OLIST-6 CA1, CA2 (impacto) |
| Pensar como consultoria, evitar foco técnico | OLIST-7 | CA10 |
| Projeto evolui ao longo das fases | OLIST-6 | CA6 |

| Critério FIAP | Cards que o cobrem |
|---|---|
| 1 Visão estratégica | OLIST-5 (CA1, CA2), OLIST-10 (CA8), OLIST-6 (CA7) |
| 2 Conectar IA ao negócio | OLIST-3 (CA5), OLIST-8 (CA5, CA6), OLIST-9 (CA10) |
| 3 Capacidade analítica | OLIST-2 (CA1–CA5), OLIST-3 (CA1) |
| 4 Profundidade dos insights | OLIST-3 (CA2–CA4), OLIST-4 (CA5), OLIST-6 (CA5) |
| 5 Estruturação executiva | OLIST-4 (CA4), OLIST-7 (CA8) |
| 6 Clareza para executivos | OLIST-4 (CA2, CA10), OLIST-7 (CA10) |
| 7 Qualidade visual | OLIST-4 (CA1), OLIST-5 (CA8), OLIST-8 (CA3), OLIST-10 (CA6) |
| 8 Organização/padronização | OLIST-4 (CA3), OLIST-8 (CA14), OLIST-9 (CA9), OLIST-6 (CA8), OLIST-7 (CA9) |
| 9 Criatividade e inovação | OLIST-3 (CA2), OLIST-8 (CA9), OLIST-10 (CA10), OLIST-7 (CA14) |
| 10 Evolução do projeto | OLIST-6 (CA6) |

## Riscos do plano e como tratar

| Risco | Ação |
|---|---|
| Diogo concentra o fim da sprint (montagem do relatório + vídeo, 30 a 01) | Template e roadmap adiantados em 26–27; Igor conduz a revisão anti-plágio; Lorran revisa o roteiro e apresenta a parte dos agentes |
| Sprint curta (1 semana) e feriado no dia 02 | Dia 02 usado só como folga; tudo pronto em 01; bloqueios com prioridade Alta e hora marcada |
| Lorran parado esperando dados | Rascunho de agentes na Onda 1, sem depender de dados (método orientado a hipóteses) |
| Agentes escolhidos antes dos dados não se sustentarem | Checkpoint 1 pode derrubar ou trocar agentes; OLIST-8 CA5 exige ligação com achado real |
| Texto ficar parecido com a referência | Escrever sem abrir o PDF; revisão cruzada (OLIST-7 CA11) |
| Números não baterem | OLIST-2 CA4 exige reprodução por 2ª pessoa |
| Relatório passar de 20 págs. | Poucos gráficos fortes; detalhes no anexo |
| Checkpoint 1 atrasar (dados não ficam prontos em 27) | Igor entrega só os 6 indicadores mínimos até 18h; o resto vai para OLIST-3 |

## Como conferir que o plano está completo
- Percorrer as duas tabelas de rastreabilidade: nenhuma linha sem card e sem critério.
- Cada pessoa com exatamente 3 cards; dependências sem ciclo (o único "vai e volta" é OLIST-7 montagem → OLIST-4 vídeo → OLIST-7 final, que são etapas diferentes).
- Nenhum critério marcado como `[ENUNC]` para algo que não está escrito no enunciado (metas do grupo aparecem como meta).
