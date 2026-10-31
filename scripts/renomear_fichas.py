"""Troca o nome do agente no cabeçalho das três fichas do Lorran (docs/abnt/assets/lorran).

Os nomes originais eram iguais aos do relatório de referência; os novos são os usados no relatório.
Os originais ficam guardados com o sufixo _original.png. Uso:
    python scripts/renomear_fichas.py
"""
from pathlib import Path

import matplotlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "docs" / "abnt" / "assets" / "lorran"
FONT = Path(matplotlib.get_data_path()) / "fonts" / "ttf" / "DejaVuSans-Bold.ttf"
NOVOS = {"ficha_agente1.png": "Sentinela de Entregas", "ficha_agente2.png": "Voz do Cliente", "ficha_agente3.png": "Copiloto de Atendimento"}

for nome, novo in NOVOS.items():
    orig = DIR / nome.replace(".png", "_original.png")
    if not orig.exists():
        Image.open(DIR / nome).save(orig)
    img = Image.open(orig).convert("RGB")
    a = np.asarray(img).astype(int)
    fundo = tuple(a[110, 1500])                          # cor do cabeçalho
    # caixa do título: pixels escuros na faixa do nome (y 85–140)
    faixa = a[85:140, 60:1300]
    escuro = (faixa.sum(axis=2) < 300)
    ys, xs = np.where(escuro)
    y0, y1 = 85 + ys.min(), 85 + ys.max()
    x0 = 60 + xs.min()
    cor = tuple(np.median(faixa[escuro], axis=0).astype(int))
    d = ImageDraw.Draw(img)
    d.rectangle([x0 - 4, y0 - 4, 1300, y1 + 4], fill=fundo)
    # tamanho de fonte com a mesma altura de maiúscula do título original
    alvo = y1 - y0
    size = 20
    while True:
        f = ImageFont.truetype(str(FONT), size)
        if f.getbbox("I")[3] - f.getbbox("I")[1] >= alvo * 0.80:
            break
        size += 1
    f = ImageFont.truetype(str(FONT), size)
    topo = f.getbbox("I")[1]
    d.text((x0 - f.getbbox(novo)[0], y0 - topo), novo, font=f, fill=cor)
    img.save(DIR / nome)
    print(f"{nome}: '{novo}' (fonte {size}px, cor {cor})")
