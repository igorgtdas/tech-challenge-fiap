"""Exporta o resultado do OLIST-2 para Excel (com fórmulas vivas) e JSON.

Estrutura do Excel:
- Leia-me ........ como usar a planilha
- Indicadores .... um indicador por linha; o valor é fórmula que aponta para a aba do indicador
- Regras ......... as regras de qualidade e o resultado de cada checagem
- Inventario ..... as tabelas do dataset, registros, chave e granularidade
- base_pedidos ... 1 linha por pedido (a base usada pelas fórmulas)
- I01, I02, ... .. uma aba por indicador: definição, fórmula Excel viva, valor do Python e a tabela calculada
"""
import json
import re
from datetime import datetime

import numpy as np
import pandas as pd
from xlsxwriter.utility import xl_col_to_name

from . import config
from .indicators import IndicatorBook

BASE_SHEET = "base_pedidos"
TABLE_START = 13  # linha (0-based) do cabeçalho da tabela nas abas de indicador (abaixo das até 4 fórmulas de valor)


def _resolver(base_cols: dict, n_base: int, sheet: str, tab_cols: dict, tab_first: int, tab_last: int):
    """Troca {base:col}, {tab:col} e {cell:col} por referências reais do Excel."""
    def resolve(formula: str, row: int | None = None) -> str:
        def sub(m):
            kind, col = m.group(1), m.group(2)
            if kind == "base":
                L = xl_col_to_name(base_cols[col])
                return f"{BASE_SHEET}!${L}$2:${L}${n_base + 1}"
            L = xl_col_to_name(tab_cols[col])
            if kind == "tab":
                return f"'{sheet}'!${L}${tab_first}:${L}${tab_last}"
            return f"{L}{row}"
        return re.sub(r"\{(base|tab|cell):([^}]+)\}", sub, formula)
    return resolve


def _clean(v):
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.floating,)):
        return float(v)
    if isinstance(v, pd.Timestamp):
        return v.to_pydatetime()
    return v


def to_excel(book: IndicatorBook, rules: pd.DataFrame, inventory: pd.DataFrame, base: pd.DataFrame, path=None):
    path = path or config.EXCEL_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    base_cols = {c: i for i, c in enumerate(base.columns)}

    with pd.ExcelWriter(path, engine="xlsxwriter", datetime_format="dd/mm/yyyy hh:mm", date_format="dd/mm/yyyy") as xw:
        wb = xw.book
        h1 = wb.add_format({"bold": True, "font_size": 14, "font_color": "#0b0b0b"})
        lab = wb.add_format({"bold": True, "font_color": "#52514e"})
        wrap = wb.add_format({"text_wrap": True, "valign": "top"})
        num = wb.add_format({"num_format": "#,##0.00"})
        pct = wb.add_format({"num_format": "0.0%"})
        dt = wb.add_format({"num_format": "dd/mm/yyyy"})
        hi = wb.add_format({"bold": True, "bg_color": "#e8f1fc", "border": 1})
        live = {k: wb.add_format({"bold": True, "bg_color": "#e8f1fc", "border": 1, "num_format": f}) for k, f in [("%", "0.0%"), ("data", "dd/mm/yyyy"), ("", "#,##0.00")]}
        ok_f = wb.add_format({"bold": True, "font_color": "#008300"})

        def fmt_for(unidade):
            return pct if unidade == "%" else (dt if unidade == "data" else num)

        # Leia-me
        ws = wb.add_worksheet("Leia-me")
        lines = [
            ("OLIST-2 · Indicadores-base do dataset Olist", h1),
            (f"Gerado pelo notebook notebooks/01_olist2_eda_indicadores.ipynb em {datetime.now():%d/%m/%Y %H:%M}.", None),
            ("", None),
            ("Como conferir um número sem Python:", lab),
            ("1. Abra a aba Indicadores e escolha um indicador; a coluna 'aba' diz onde ele está calculado.", None),
            ("2. Na aba do indicador, a célula azul é uma fórmula do Excel sobre a aba base_pedidos (ou sobre a tabela da própria aba).", None),
            ("3. Ao lado está o valor calculado no Python. A coluna 'confere' mostra OK quando os dois são iguais.", None),
            ("", None),
            ("A aba base_pedidos tem 1 linha por pedido, já com as regras de qualidade aplicadas (ver aba Regras).", None),
            ("Células vazias na base são dados ausentes: nunca foram trocadas por zero (regra R5).", None),
        ]
        for r, (text, f) in enumerate(lines):
            ws.write(r, 0, text, f)
        ws.set_column(0, 0, 120)

        # Indicadores (preenchida depois das abas, para saber as células de valor)
        summary_rows = []

        # base_pedidos
        base.to_excel(xw, sheet_name=BASE_SHEET, index=False)
        wsb = xw.sheets[BASE_SHEET]
        wsb.freeze_panes(1, 0)
        wsb.set_column(0, len(base.columns) - 1, 16)

        # uma aba por indicador
        for ind in book.items:
            sheet = ind.id
            ws = wb.add_worksheet(sheet)
            ws.set_column(0, 0, 34)
            ws.set_column(1, 12, 18)
            ws.write(0, 0, f"{ind.id} · {ind.nome}", h1)
            for r, (k, v) in enumerate([
                ("Definição", ind.definicao), ("Fórmula", ind.formula),
                ("Tabelas de origem", ind.tabelas), ("Regras aplicadas", ind.regras),
                ("Cálculo em Python", ind.codigo),
            ], start=1):
                ws.write(r, 0, k, lab)
                ws.write(r, 1, v)

            tab = ind.tabela
            tab_cols = {c: i for i, c in enumerate(tab.columns)} if tab is not None else {}
            tab_first, tab_last = TABLE_START + 2, TABLE_START + 1 + (len(tab) if tab is not None else 0)
            resolve = _resolver(base_cols, len(base), sheet, tab_cols, tab_first, tab_last)

            # fórmulas vivas do valor: rótulo | fórmula Excel | valor Python | confere
            ws.write(6, 0, "Valor", lab)
            ws.write(6, 1, "fórmula Excel", lab)
            ws.write(6, 2, "valor no Python", lab)
            ws.write(6, 3, "confere", lab)
            value_cell = None
            items = list(ind.excel.items())
            expected_values = ind.esperados if ind.esperados is not None else [ind.valor]
            for k, (label, formula) in enumerate(items):
                row = 7 + k
                kind = "data" if label in ("início", "fim") else ("%" if ind.unidade == "%" else "")
                f = fmt_for(kind)
                expected = expected_values[k] if k < len(expected_values) else None
                ws.write(row, 0, label)
                ws.write_formula(row, 1, "=" + resolve(formula), live[kind])
                if expected is not None and not isinstance(expected, str):
                    ws.write(row, 2, _clean(expected), f)
                    ws.write_formula(row, 3, f'=IF(ABS(B{row+1}-C{row+1})< 0.000001,"OK","DIFERENTE")', ok_f)
                if k == 0:
                    value_cell = f"'{sheet}'!$B${row + 1}"

            # tabela calculada
            if tab is not None:
                ws.write(TABLE_START - 1, 0, "Tabela calculada", lab)
                for c, name in enumerate(tab.columns):
                    ws.write(TABLE_START, c, name, hi)
                for r, rec in enumerate(tab.itertuples(index=False), start=TABLE_START + 1):
                    for c, v in enumerate(rec):
                        v = _clean(v)
                        if v is None or (isinstance(v, float) and np.isnan(v)):
                            continue
                        col = tab.columns[c]
                        if col in ind.excel_linhas:
                            continue
                        ws.write(r, c, v)
                    for col, formula in ind.excel_linhas.items():
                        ws.write_formula(r, tab_cols[col], "=" + resolve(formula, row=r + 1), pct if "taxa" in col or "%" in col else num)

            summary_rows.append((ind, sheet, value_cell))

        # Indicadores
        ws = wb.add_worksheet("Indicadores")
        cols = ["id", "nome", "definição", "fórmula", "tabelas de origem", "regras", "valor (fórmula)", "valor (texto)", "aba"]
        widths = [6, 30, 50, 50, 26, 10, 16, 18, 8]
        for c, (name, w) in enumerate(zip(cols, widths)):
            ws.write(0, c, name, hi)
            ws.set_column(c, c, w, wrap if c in (2, 3) else None)
        for r, (ind, sheet, cell) in enumerate(summary_rows, start=1):
            ws.write_row(r, 0, [ind.id, ind.nome, ind.definicao, ind.formula, ind.tabelas, ind.regras])
            if cell and not isinstance(ind.valor, str):
                ws.write_formula(r, 6, f"={cell}", fmt_for(ind.unidade))
            ws.write(r, 7, ind.texto())
            ws.write_url(r, 8, f"internal:'{sheet}'!A1", string=sheet)
        ws.freeze_panes(1, 2)

        rules.to_excel(xw, sheet_name="Regras", index=False)
        xw.sheets["Regras"].set_column(0, 0, 6)
        xw.sheets["Regras"].set_column(1, 2, 60, wrap)
        xw.sheets["Regras"].set_column(3, 6, 18)
        inventory.to_excel(xw, sheet_name="Inventario", index=False)
        xw.sheets["Inventario"].set_column(0, 10, 20)

        # ordem das abas: Leia-me, Indicadores, Regras, Inventario, base, I01...
        order = ["Leia-me", "Indicadores", "Regras", "Inventario", BASE_SHEET] + [i.id for i in book.items]
        wb.worksheets_objs.sort(key=lambda s: order.index(s.name))
        wb.worksheets_objs[0].activate()
    return path


def to_json(book: IndicatorBook, rules: pd.DataFrame, inventory: pd.DataFrame, meta: dict, path=None):
    path = path or config.JSON_PATH
    path.parent.mkdir(parents=True, exist_ok=True)

    def plain(v):
        v = _clean(v)
        if isinstance(v, datetime):
            return v.strftime("%Y-%m-%d")
        if isinstance(v, (list, tuple)):
            return [plain(x) for x in v]
        return v

    data = {
        "meta": {k: plain(v) for k, v in meta.items()},
        "indicadores": [
            {
                "id": i.id, "nome": i.nome, "definicao": i.definicao, "formula": i.formula,
                "tabelas": i.tabelas, "regras": i.regras, "valor": plain(i.valor),
                "unidade": i.unidade, "texto": i.texto(),
            }
            for i in book.items
        ],
        "regras": json.loads(rules.to_json(orient="records", force_ascii=False)),
        "inventario": json.loads(inventory.to_json(orient="records", force_ascii=False)),
    }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
