"""Leitura dos CSVs brutos com tipos corretos (datas como data, CEP como texto)."""
import pandas as pd

from . import config


def load_table(name: str) -> pd.DataFrame:
    """Lê uma tabela pelo nome curto (ex.: "orders"), sem alterar nenhum valor."""
    spec = config.TABLES[name]
    path = config.RAW / spec["file"]
    header = pd.read_csv(path, nrows=0, encoding="utf-8-sig").columns
    dtypes = {c: "string" for c in header if c in config.TEXT_COLUMNS}
    df = pd.read_csv(path, dtype=dtypes, encoding="utf-8-sig")
    for col in spec["dates"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def load_all() -> dict[str, pd.DataFrame]:
    """Lê as 9 tabelas e devolve {nome: DataFrame}."""
    return {name: load_table(name) for name in config.TABLES}
