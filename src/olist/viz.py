"""Estilo único dos gráficos: mesma paleta, tipografia e anatomia em todas as figuras.

Regras seguidas:
- título diz a conclusão; subtítulo diz o que está sendo medido;
- uma cor por série, na ordem fixa da paleta (nunca reciclada);
- grade e eixos discretos; rótulos de valor só onde ajudam;
- rodapé com a fonte ("Fonte: elaboração própria a partir do dataset Olist").
"""
import matplotlib.pyplot as plt
from matplotlib import font_manager

from . import config

# Paleta categórica (ordem fixa) e cores de texto/superfície
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6"]
MUTED = "#b9b8b2"        # barras "de contexto" (ex.: meses de borda)
TEXT = "#0b0b0b"
TEXT_2 = "#52514e"
GRID = "#e6e5e0"
SURFACE = "#ffffff"
SOURCE = "Fonte: elaboração própria a partir do dataset Olist (Kaggle)."


def setup():
    """Aplica o estilo global do matplotlib (chamar uma vez no início do notebook)."""
    family = "Arial" if any(f.name == "Arial" for f in font_manager.fontManager.ttflist) else "DejaVu Sans"
    plt.rcParams.update({
        "font.family": family,
        "font.size": 10,
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "axes.edgecolor": GRID,
        "axes.labelcolor": TEXT_2,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlecolor": TEXT,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": GRID,
        "grid.linewidth": 0.8,
        "xtick.color": TEXT_2,
        "ytick.color": TEXT_2,
        "legend.frameon": False,
        "figure.dpi": 110,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
    })


def titles(ax, title: str, subtitle: str = ""):
    """Título-conclusão em negrito e subtítulo explicativo logo abaixo."""
    ax.set_title(title, pad=24 if subtitle else 10)
    if subtitle:
        ax.text(0, 1.02, subtitle, transform=ax.transAxes, color=TEXT_2, fontsize=10, va="bottom")


def save(fig, name: str):
    """Acrescenta a fonte no rodapé e salva em reports/figures/<name>.png."""
    config.FIGURES.mkdir(parents=True, exist_ok=True)
    fig.text(0.01, -0.02, SOURCE, color=TEXT_2, fontsize=8, ha="left", va="top")
    path = config.FIGURES / f"{name}.png"
    fig.savefig(path)
    return path


def fmt_int(n) -> str:
    return f"{int(n):,}".replace(",", ".")


def fmt_pct(x, digits: int = 1) -> str:
    return f"{x:.{digits}%}".replace(".", ",")
