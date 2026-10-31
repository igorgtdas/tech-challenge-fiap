"""Desenha o mapa de agentes (entregável 2, card OLIST-8): visão executiva, com pouco texto.

Uso (na raiz do projeto, com o .venv ativo):
    python scripts/diagrama_mapa_agentes.py

Gera docs/abnt/assets/mapa_agentes.png no mesmo estilo de quadro do Miro da arquitetura
(scripts/diagrama_arquitetura.py): usuários no alto, os três agentes com seu objetivo,
os fluxos entre eles e o benefício de cada um embaixo.
"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "abnt" / "assets" / "mapa_agentes.png"

NAVY = "#0A192F"
BLUE = "#00B4D8"
CORAL = "#FF4D4D"
INK = "#1F2933"
BOARD_BG = "#F4F5F7"
STICKY = "#FFF4B8"

fig, ax = plt.subplots(figsize=(8.6, 4.6))
ax.set_xlim(0, 100); ax.set_ylim(0, 50); ax.axis("off")
fig.patch.set_facecolor(BOARD_BG)
for gx in range(0, 101, 2):
    ax.scatter([gx] * 26, list(range(0, 51, 2)), s=0.5, color="#D5D8DE", zorder=0)


def person(cx, cy, label):
    ax.add_patch(Ellipse((cx, cy + 1.7), 2.4, 2.6, fc=NAVY, ec="none", zorder=4))
    ax.add_patch(Ellipse((cx, cy - 0.6), 4.2, 3.8, fc=NAVY, ec="none", zorder=4))
    ax.add_patch(Rectangle((cx - 2.3, cy - 2.6), 4.6, 2.0, fc=BOARD_BG, ec="none", zorder=4))
    ax.text(cx + 3.4, cy + 0.2, label, ha="left", va="center", fontsize=8, color=INK, zorder=4, linespacing=1.1)


def arrow(p0, p1, color=BLUE, lw=1.6):
    ax.annotate("", xy=p1, xytext=p0, arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=13), zorder=2)


agentes = [
    (3.0, "Voz do\nCliente", "lê e classifica as\navaliações por tema", "Experiência do\ncliente e qualidade",
     "problemas recorrentes\nvisíveis e tratados"),
    (37.0, "Sentinela de\nEntregas", "sinaliza pedidos com\nrisco de atraso", "Logística e\noperação",
     "menos atrasos e\nmenos notas ruins"),
    (71.0, "Copiloto de\nAtendimento", "prepara respostas\ncom fatos e fontes", "Atendentes e\nsupervisores",
     "atendimento rápido\ne padronizado"),
]
W = 26.0
for x, nome, objetivo, usuarios, beneficio in agentes:
    cx = x + W / 2
    person(x + 6.5, 43.0, usuarios)
    arrow((cx, 39.2), (cx, 33.2), color=NAVY, lw=1.3)
    ax.add_patch(FancyBboxPatch((x, 19.0), W, 14.0, boxstyle="round,pad=0,rounding_size=1.4", fc="white", ec=BLUE, lw=2.2, zorder=3))
    ax.text(cx, 28.9, nome, ha="center", va="center", fontsize=10, fontweight="bold", color=NAVY, zorder=4, linespacing=1.05)
    ax.text(cx, 22.8, objetivo, ha="center", va="center", fontsize=8.4, color=INK, zorder=4, linespacing=1.25)
    arrow((cx, 19.0), (cx, 15.4), color=BLUE, lw=1.3)
    ax.add_patch(FancyBboxPatch((x + 2.5, 5.6), W - 5.0, 9.6, boxstyle="round,pad=0,rounding_size=0.8", fc=STICKY, ec="#E8D36A", lw=1, zorder=3))
    ax.text(cx, 13.2, "BENEFÍCIO", ha="center", va="center", fontsize=6.8, fontweight="bold", color=NAVY, zorder=4)
    ax.text(cx, 9.0, beneficio, ha="center", va="center", fontsize=8.2, color=INK, zorder=4, linespacing=1.2)

# fluxos entre os agentes
arrow((29.0, 26.0), (37.0, 26.0))
ax.text(33.0, 29.6, "temas de\nentrega", ha="center", va="center", fontsize=6.8, color=INK, zorder=5, linespacing=1.0)
arrow((63.0, 26.0), (71.0, 26.0))
ax.text(67.0, 29.6, "alerta +\nevidências", ha="center", va="center", fontsize=6.8, color=INK, zorder=5, linespacing=1.0)

# regra comum aos três
ax.add_patch(FancyBboxPatch((3.0, 0.6), 94.0, 3.6, boxstyle="round,pad=0,rounding_size=0.8", fc="white", ec=CORAL, lw=1.4, zorder=3))
ax.text(50, 2.4, "Os três recomendam e encaminham: toda ação que afeta o cliente passa por aprovação humana.",
        ha="center", va="center", fontsize=8, color=NAVY, zorder=4)

OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, dpi=300, bbox_inches="tight", facecolor=BOARD_BG)
print(OUT)
