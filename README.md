# Tech Challenge Agentic AI · Olist Intelligent Marketplace

Projeto do grupo **Diogo, Igor e Lorran** para o Tech Challenge da pós-graduação em Agentic AI (FIAP).
O mesmo repositório acompanha as 5 fases: cada fase reaproveita e expande o que a anterior deixou.

**Pergunta da Fase 1:** como a Olist poderia usar IA Generativa e Agentes de IA para melhorar sua operação e seus indicadores de negócio?

## Onde está cada coisa

```
Case FIAP/
├─ README.md
├─ requirements.txt          bibliotecas Python do projeto
├─ data/
│  ├─ raw/                   os 9 CSVs do Kaggle, intocados (fora do git; ver data/raw/README.md)
│  └─ processed/             bases geradas pelo notebook, ex.: base_pedidos.csv (fora do git)
├─ notebooks/
│  └─ 01_olist2_eda_indicadores.ipynb   EDA, regras de qualidade e indicadores-base (card OLIST-2)
├─ src/olist/                código reutilizável; a análise em si fica visível no notebook
│  ├─ config.py              caminhos e "dicionário" das tabelas (chave, granularidade, relações)
│  ├─ io.py                  leitura dos CSVs com tipos corretos
│  ├─ quality.py             registro das regras de qualidade
│  ├─ indicators.py          registro dos indicadores (definição, fórmula, origem, fórmula Excel)
│  ├─ viz.py                 estilo único dos gráficos
│  └─ export.py              Excel com fórmulas vivas e JSON
├─ scripts/
│  └─ build_docx.py          gera o relatório ABNT (Word) a partir de reports/indicadores.json
├─ reports/
│  ├─ figures/               gráficos em PNG
│  ├─ indicadores_olist.xlsx planilha: uma aba por indicador, com fórmula Excel e valor do Python
│  └─ indicadores.json       números para o Word e o Confluence
├─ docs/
│  ├─ case/                  enunciado, plano de execução e cronograma da sprint
│  └─ abnt/                  template FIAP (ABNT) e relatórios em Word
└─ fases/                    esqueleto das fases 2 a 5 (ainda não iniciadas)
```

## Como rodar

Requer Python 3.12 ou 3.13. O 3.15 ainda não tem todos os pacotes do Jupyter prontos para Windows.

```bash
py -3.13 -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
```

1. Baixe o dataset do Kaggle e coloque os 9 CSVs em `data/raw/`.
2. Abra `notebooks/01_olist2_eda_indicadores.ipynb` no VS Code ou Jupyter, selecione o kernel `.venv` e rode tudo (*Run All*).
   Ele gera a base de pedidos, as figuras, a planilha e o JSON.
3. Gere o Word: `.venv/Scripts/python scripts/build_docx.py` cria `docs/abnt/OLIST-2_relatorio.docx`.

## Fases do projeto

| Fase | Foco | Pasta | Situação |
|---|---|---|---|
| 1 | Diagnóstico, oportunidades, mapa de agentes, arquitetura conceitual, prompts e vídeo | `notebooks/`, `docs/` | em andamento (entrega 03/11) |
| 2 | Dados e preparação para os agentes | `fases/2-dados` | não iniciada |
| 3 | Protótipo dos agentes | `fases/3-agentes` | não iniciada |
| 4 | Arquitetura e integrações | `fases/4-arquitetura` | não iniciada |
| 5 | Monitoramento (ex.: LangSmith) e evolução | `fases/5-monitoramento` | não iniciada |

## Fase 1 · cards

O plano completo, com os critérios de aceite, está em `docs/case/Plano_Execucao_Tech_Challenge_Fase1.md`.

| Card | Responsável | Entregável no repositório |
|---|---|---|
| OLIST-2 · Dataset e indicadores-base | Igor | notebook 01, `reports/`, `docs/abnt/OLIST-2_relatorio.docx` |
| OLIST-3 · Achados de negócio | Igor | (próximo notebook) |
| OLIST-4 · Gráficos e vídeo | Diogo | — |
| OLIST-5 · Oportunidades e matriz | Lorran | — |
| OLIST-6 · Impacto, KPIs e roadmap | Diogo | — |
| OLIST-7 · Relatório final | Diogo | — |
| OLIST-8 · Mapa de agentes e riscos | Lorran | — |
| OLIST-9 · Prompts | Lorran | — |
| OLIST-10 · Arquitetura conceitual | Igor | — |

Dados: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle).
