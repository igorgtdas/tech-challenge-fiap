"""Registro dos indicadores.

Cada indicador guarda o que o relatório precisa citar (definição, fórmula, tabela de
origem, regras aplicadas) e o que o Excel precisa reproduzir:

- `tabela`: a tabela calculada, que vai para a aba do indicador;
- `excel`: fórmulas vivas do valor, {rótulo: fórmula};
- `excel_linhas`: fórmulas linha a linha da tabela, {coluna: fórmula com {row}}.

Nas fórmulas, `{base:coluna}` aponta para a coluna da aba base_pedidos e `{tab:coluna}`
para a coluna da própria tabela do indicador. O export troca isso por intervalos reais.
"""
from dataclasses import dataclass, field

import pandas as pd


@dataclass
class Indicator:
    id: str
    nome: str
    definicao: str
    formula: str            # em linguagem simples
    tabelas: str            # tabelas de origem do dataset
    regras: str             # regras de qualidade aplicadas (ex.: "R1, R4")
    valor: object           # número (ou texto, no caso do período)
    unidade: str = ""       # "%", "dias", "R$", "pedidos"...
    codigo: str = ""        # o cálculo em pandas, como texto
    tabela: pd.DataFrame | None = None
    excel: dict = field(default_factory=dict)
    excel_linhas: dict = field(default_factory=dict)
    esperados: list | None = None   # valores do Python para cada fórmula de `excel` (padrão: [valor])

    def texto(self) -> str:
        v = self.valor
        if isinstance(v, str):
            return v
        if self.unidade == "%":
            return f"{v:.1%}".replace(".", ",")
        if self.unidade == "R$":
            return "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        if isinstance(v, float) and not float(v).is_integer():
            return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".").rstrip("0").rstrip(",") + (f" {self.unidade}" if self.unidade else "")
        return f"{int(v):,}".replace(",", ".") + (f" {self.unidade}" if self.unidade else "")


class IndicatorBook:
    def __init__(self):
        self.items: list[Indicator] = []

    def add(self, **kwargs) -> Indicator:
        ind = Indicator(**kwargs)
        self.items = [i for i in self.items if i.id != ind.id] + [ind]
        print(f"{ind.id} · {ind.nome}: {ind.texto()}")
        return ind

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame([
            {
                "id": i.id, "nome": i.nome, "definicao": i.definicao, "formula": i.formula,
                "tabelas": i.tabelas, "regras": i.regras, "valor": i.texto(),
            }
            for i in self.items
        ])
