"""Registro dos achados de negócio (card OLIST-3).

Cada análise vira um achado no formato **Fato · Leitura · Cautela · E daí?**:
- Fato ....... o que os números mostram, sem interpretação;
- Leitura .... o que o fato sugere sobre o negócio;
- Cautela .... o limite da conclusão (associação não é causa, viés do dado, tamanho da amostra);
- E daí? ..... o que isso muda para a Olist e para a escolha dos agentes.

Os números citados no texto vêm de métricas registradas no IndicatorBook (com fórmula Excel),
para que cada número do relatório possa ser conferido na planilha.
"""
import re
from dataclasses import dataclass, field, asdict

import pandas as pd

# Os 8 desafios da Olist listados no enunciado (p. 2)
DESAFIOS = {
    "cliente": "Experiência do cliente",
    "logistica": "Eficiência logística",
    "retencao": "Retenção e fidelização",
    "reviews": "Gestão de avaliações (reviews)",
    "eficiencia": "Eficiência operacional",
    "automacao": "Automação de processos",
    "decisao": "Apoio à tomada de decisão",
    "escala": "Escalabilidade da operação",
}

# As 8 dimensões do dataset citadas no enunciado (p. 3–4)
DIMENSOES = ["clientes", "pedidos", "pagamentos", "produtos", "logística", "vendedores", "avaliações", "geolocalização"]

# Expressões que afirmam causa; o texto dos achados não pode usá-las (CA4)
CAUSAL = [r"\bcausa(m|r|do|da)?\b", r"\bprovoca", r"\bleva(m)? a\b", r"\bfaz(em)? com que\b",
          r"\bdevido a\b", r"\bpor causa\b", r"\bresulta(m)? em\b", r"\bgera(m)?\b", r"\bcomprova",
          r"\bderruba", r"\bdesorganiza", r"\bexplica(m)?\b", r"\bpiora(m)? a\b", r"\bfaz(em)? cair\b"]


@dataclass
class Finding:
    id: str
    tipo: str                 # "núcleo" ou "diferencial"
    titulo: str               # a conclusão em uma frase
    pergunta: str             # a pergunta que a análise responde
    dimensoes: list           # dimensões do dataset usadas
    desafios: list            # chaves de DESAFIOS
    fato: str
    leitura: str
    cautela: str
    e_dai: str
    metricas: list = field(default_factory=list)   # ids das métricas (abas do Excel)
    figura: str = ""                               # nome do PNG em reports/figures

    def markdown(self) -> str:
        desafios = ", ".join(DESAFIOS[d] for d in self.desafios)
        return (
            f"#### {self.id} · {self.titulo}\n\n"
            f"*Pergunta:* {self.pergunta}  \n*Tipo:* análise {self.tipo} · *Dimensões:* {', '.join(self.dimensoes)} · "
            f"*Desafios do enunciado:* {desafios} · *Métricas na planilha:* {', '.join(self.metricas) or '—'}\n\n"
            f"| | |\n|---|---|\n"
            f"| **Fato** | {self.fato} |\n| **Leitura** | {self.leitura} |\n"
            f"| **Cautela** | {self.cautela} |\n| **E daí?** | {self.e_dai} |\n"
        )


@dataclass
class KeyFinding:
    rank: int
    titulo: str
    resumo: str               # 1–2 frases com o número principal
    achados: list             # ids dos achados que sustentam
    desafios: list            # chaves de DESAFIOS
    para_quem: str            # quem usa este achado nos próximos cards
    oportunidade: str         # que tipo de solução o achado pede (sem escolher o agente: isso é OLIST-8)


class FindingBook:
    def __init__(self):
        self.items: list[Finding] = []
        self.keys: list[KeyFinding] = []

    def add(self, **kwargs) -> None:
        f = Finding(**kwargs)
        self.items = [i for i in self.items if i.id != f.id] + [f]
        try:
            from IPython.display import Markdown, display
            display(Markdown(f.markdown()))
        except ImportError:
            print(f.markdown())

    def add_key(self, **kwargs) -> KeyFinding:
        k = KeyFinding(**kwargs)
        self.keys = [i for i in self.keys if i.rank != k.rank] + [k]
        self.keys.sort(key=lambda x: x.rank)
        return k

    def causal_check(self) -> pd.DataFrame:
        """Procura linguagem causal nos textos (CA4). Devolve as ocorrências; vazio = OK."""
        hits = []
        for f in self.items:
            for campo in ("titulo", "fato", "leitura", "cautela", "e_dai"):
                texto = getattr(f, campo)
                for pat in CAUSAL:
                    for m in re.finditer(pat, texto, flags=re.I):
                        # "não é causa" e "não prova causa" são justamente a cautela: permitidos
                        antes = texto[max(0, m.start() - 12):m.start()].lower()
                        if "não " in antes or "nem " in antes:
                            continue
                        hits.append({"achado": f.id, "campo": campo, "trecho": texto[max(0, m.start() - 30):m.end() + 30]})
        for k in self.keys:
            for campo in ("titulo", "resumo"):
                for pat in CAUSAL:
                    for m in re.finditer(pat, getattr(k, campo), flags=re.I):
                        hits.append({"achado": f"K{k.rank}", "campo": campo, "trecho": getattr(k, campo)[max(0, m.start() - 30):m.end() + 30]})
        return pd.DataFrame(hits, columns=["achado", "campo", "trecho"])

    def coverage(self) -> pd.DataFrame:
        return pd.DataFrame([{"dimensão": d, "achados": ", ".join(f.id for f in self.items if d in f.dimensoes)} for d in DIMENSOES])

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame([{**asdict(f), "dimensoes": ", ".join(f.dimensoes),
                              "desafios": ", ".join(DESAFIOS[d] for d in f.desafios),
                              "metricas": ", ".join(f.metricas)} for f in self.items])

    def keys_frame(self) -> pd.DataFrame:
        return pd.DataFrame([{**asdict(k), "achados": ", ".join(k.achados),
                              "desafios": ", ".join(DESAFIOS[d] for d in k.desafios)} for k in self.keys])
