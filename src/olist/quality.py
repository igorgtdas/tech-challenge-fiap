"""Registro das regras de qualidade.

A checagem de cada regra é escrita no notebook (para ficar visível); aqui só fica o
"caderno" que guarda o resultado e o transforma em tabela para Excel, Word e Confluence.
"""
from dataclasses import dataclass, asdict

import pandas as pd


@dataclass
class Rule:
    id: str
    regra: str          # a regra em linguagem simples
    motivo: str         # o problema do dataset que ela evita
    afetados: int       # quantos registros a regra muda ou exclui
    base: str           # "de quantos" (ex.: "99.441 pedidos")
    ok: bool            # a checagem passou?
    evidencia: str      # o que a checagem mostrou


class RuleBook:
    def __init__(self):
        self.rules: list[Rule] = []

    def add(self, **kwargs) -> Rule:
        rule = Rule(**kwargs)
        self.rules = [r for r in self.rules if r.id != rule.id] + [rule]
        status = "OK" if rule.ok else "ALERTA"
        print(f"[{status}] {rule.id} · {rule.regra}\n        {rule.evidencia}")
        return rule

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame([asdict(r) for r in self.rules])
