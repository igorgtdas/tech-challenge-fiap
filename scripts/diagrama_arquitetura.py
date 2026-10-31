"""Desenha a arquitetura conceitual dos agentes (card OLIST-10) no estilo de um quadro do Miro.

Uso (na raiz do projeto, com o .venv ativo):
    python scripts/diagrama_arquitetura.py

Gera reports/figures/o10_arquitetura.png e docs/abnt/assets/arquitetura_agentes_olist10.png.
Segue as diretrizes visuais do grupo (OLIST-4/7): retângulos arredondados = agentes;
cilindros = bases de dados; ícones de pessoa = usuários; coral só nas bordas de governança;
linhas ortogonais com legenda.

O quadro é desenhado em formato retrato (8,6 × 11,6 pol.) para que, ocupando a largura da
página do relatório (16 cm), o texto fique legível.
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Rectangle, Wedge

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from olist import config  # noqa: E402

NAVY = "#0A192F"      # cabeçalhos, estrutura e texto de destaque
BLUE = "#00B4D8"      # agentes e fluxos
CORAL = "#FF4D4D"     # bordas de governança
INK = "#1F2933"
MUTED = "#6B7280"
BOARD_BG = "#F4F5F7"
STICKY = "#FFF4B8"
TOOL_BG = "#E9F9FC"
FUTURE = "#9CA3AF"
LANE = "#E8ECF2"

fig, ax = plt.subplots(figsize=(8.6, 11.6))
ax.set_xlim(0, 100); ax.set_ylim(0, 79); ax.axis("off")
fig.patch.set_facecolor(BOARD_BG)

# grade de pontos do quadro (Miro)
for gx in range(0, 101, 2):
    ax.scatter([gx] * 40, list(range(0, 80, 2)), s=0.5, color="#D5D8DE", zorder=0)

MAIN_R = 81.5         # borda direita das raias principais
GOV_X, GOV_W = 83.5, 16.0


def lane(y, h, title, x=1, w=MAIN_R - 1):
    """Raia com cabeçalho lateral (texto na vertical), como um frame do Miro."""
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.6", fc="white", ec="#D1D5DB", lw=1, zorder=1))
    ax.add_patch(FancyBboxPatch((x, y), 3.4, h, boxstyle="round,pad=0,rounding_size=0.6", fc=LANE, ec="none", zorder=1))
    ax.text(x + 1.7, y + h / 2, title, rotation=90, ha="center", va="center", fontsize=7.2, fontweight="bold", color=NAVY, zorder=5, linespacing=1.1)


def card(x, y, w, h, title, sub="", ec=BLUE, fc="white", tc=NAVY, fs=9, lw=2, sfs=7.4):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2", fc=fc, ec=ec, lw=lw, zorder=3))
    two = "\n" in title
    ax.text(x + w / 2, y + h - ((2.5 if two else 1.6) if sub else h / 2), title, ha="center", va="center", fontsize=fs, fontweight="bold",
            color=tc, zorder=4, linespacing=1.05)
    if sub:
        ax.text(x + w / 2, y + (h - (4.4 if two else 2.6)) / 2, sub, ha="center", va="center", fontsize=sfs, color=INK, zorder=4, linespacing=1.25)


def person(cx, cy, label, color=NAVY, bg="white"):
    ax.add_patch(Ellipse((cx, cy + 1.6), 2.4, 1.7, fc=color, ec="none", zorder=4))
    ax.add_patch(Ellipse((cx, cy - 0.4), 4.0, 2.6, fc=color, ec="none", zorder=4))
    ax.add_patch(Rectangle((cx - 2.2, cy - 1.8), 4.4, 1.4, fc=bg, ec="none", zorder=4))
    if label:
        ax.text(cx, cy - 1.2, label, ha="center", va="top", fontsize=8, color=INK, zorder=4, linespacing=1.15)


def cylinder(cx, y, label, future=False):
    w, h = 7.6, 5.0
    ec = FUTURE if future else NAVY
    fc = "white" if future else "#EEF2F7"
    ls = (0, (3, 2)) if future else "-"
    ax.add_patch(Rectangle((cx - w / 2, y), w, h, fc=fc, ec="none", zorder=3))
    ax.plot([cx - w / 2, cx - w / 2], [y, y + h], color=ec, lw=1.2, ls=ls, zorder=4)
    ax.plot([cx + w / 2, cx + w / 2], [y, y + h], color=ec, lw=1.2, ls=ls, zorder=4)
    ax.add_patch(Ellipse((cx, y), w, 1.2, fc=fc, ec=ec, lw=1.2, ls=ls, zorder=3))
    ax.add_patch(Ellipse((cx, y + h), w, 1.2, fc=fc, ec=ec, lw=1.2, ls=ls, zorder=5))
    ax.text(cx, y + h / 2 - 0.2, label, ha="center", va="center", fontsize=7.4, color=MUTED if future else NAVY, zorder=6, linespacing=1.1)


def tag(x, y, text, fs=7.2):
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=INK, zorder=7, linespacing=1.1,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#E5E7EB", lw=0.6))


def path(points, color=BLUE, lw=1.6, ls="-", head=True, z=2):
    """Conector ortogonal (lista de pontos) com seta no fim."""
    xs, ys = zip(*points)
    ax.plot(xs, ys, color=color, lw=lw, ls=ls, zorder=z, solid_capstyle="round")
    if head:
        ax.annotate("", xy=points[-1], xytext=points[-2], arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=12), zorder=z)


# ---------------------------------------------------------------- título do quadro
ax.text(1, 78.7, "Olist · Arquitetura conceitual dos agentes", fontsize=14, fontweight="bold", color=NAVY, va="top")
ax.text(1, 76.6, "Fase 1 · desenho conceitual, sem implementação  ·  * ferramenta sugerida, fora da proposta original do Lorran",
        fontsize=7.6, color=MUTED, va="top")

# ---------------------------------------------------------------- usuários
lane(65.0, 9.4, "USUÁRIOS E\nGATILHOS")
people = [(12, "Atendente\n(SAC)"), (27, "Logística e\noperação"), (43, "Experiência\ndo cliente"), (57, "Gestores")]
for cx, lab in people:
    person(cx, 70.4, lab)
card(66.0, 66.6, 14.2, 6.4, "Rotina diária", "varredura dos\npedidos abertos", ec=NAVY, fs=8.4, sfs=7.4)

# ---------------------------------------------------------------- orquestrador
lane(52.0, 11.0, "ORQUES-\nTRAÇÃO")
card(20.0, 53.4, 40.0, 5.8, "Agente Orquestrador (router)", "entende o pedido e escolhe o especialista", ec=NAVY, fc="#EEF2F7", fs=10, sfs=7.8)
for cx, _ in people:
    path([(cx, 65.8), (cx, 61.6)], color=NAVY, lw=1.2, head=False)
path([(73.1, 66.6), (73.1, 61.6)], color=NAVY, lw=1.2, head=False)
path([(12, 61.6), (73.1, 61.6)], color=NAVY, lw=1.2, head=False)
path([(40, 61.6), (40, 59.2)], color=NAVY, lw=1.4)
tag(56.5, 61.6, "pergunta, pedido ou varredura")

# ---------------------------------------------------------------- especialistas
lane(33.0, 17.0, "AGENTES\nESPECIALISTAS")
W = 22.0
ag = {
    "voz": (5.5, "Voz do\nCliente", "classifica avaliações\npor tema e sentimento,\ncom evidência"),
    "sen": (32.5, "Sentinela de\nEntregas", "sinaliza pedidos com\nrisco de atraso e\nrecomenda a ação"),
    "cop": (59.5, "Copiloto de\nAtendimento", "reúne os fatos e\nprepara a resposta\npara o atendente"),
}
for key, (x, t, s) in ag.items():
    card(x, 36.0, W, 10.6, t, s, fs=8.8, sfs=7.4)
path([(40, 53.4), (40, 48.6)], color=BLUE, lw=1.5, head=False)
path([(16.5, 48.6), (70.5, 48.6)], color=BLUE, lw=1.5, head=False)
for key, (x, *_r) in ag.items():
    path([(x + W / 2, 48.6), (x + W / 2, 46.2)], color=BLUE, lw=1.5)
tag(27.5, 48.6, "tarefa + contexto")
# interações entre especialistas
path([(27.5, 39.8), (32.5, 39.8)], color=BLUE, lw=1.4)
ax.text(30.0, 42.4, "temas\nde en-\ntrega", fontsize=6.6, color=INK, ha="center", va="center", zorder=6, linespacing=1.0)
path([(54.5, 39.8), (59.5, 39.8)], color=BLUE, lw=1.4)
ax.text(57.0, 42.4, "alerta\n+ evi-\ndências", fontsize=6.6, color=INK, ha="center", va="center", zorder=6, linespacing=1.0)
# saída dos especialistas para o validador (barramento coral)
for key, (x, *_r) in ag.items():
    path([(x + W - 2.5, 36.0), (x + W - 2.5, 34.4)], color=CORAL, lw=1.3, head=False)
path([(25.0, 34.4), (82.6, 34.4), (82.6, 56.4), (GOV_X + 1.0, 56.4)], color=CORAL, lw=1.5)
tag(70.0, 34.4, "resposta + evidências")

# ---------------------------------------------------------------- ferramentas
lane(18.5, 12.8, "FERRAMENTAS\n(TOOLS)")
tools = {
    "voz": ["buscar_avaliacoes", "consultar_contexto_pedido", "resumir_temas_periodo *", "registrar_classificacao *"],
    "sen": ["listar_pedidos_em_aberto", "consultar_pedido", "consultar_rastreamento", "consultar_prazo_postagem *", "calcular_risco_rota *", "historico_vendedor *"],
    "cop": ["consultar_pedido", "buscar_pedidos_do_cliente *", "consultar_pagamento *", "buscar_politica", "consultar_historico_atendimento", "consultar_alertas_agentes"],
}
for key, (x, *_r) in ag.items():
    ax.add_patch(FancyBboxPatch((x, 20.6), W, 9.6, boxstyle="round,pad=0,rounding_size=0.8", fc=TOOL_BG, ec=BLUE, lw=1, ls=(0, (4, 2)), zorder=3))
    for i, tname in enumerate(tools[key]):
        ax.text(x + 0.7, 29.2 - i * 1.5, tname, fontsize=6.3, color=NAVY, va="center", zorder=4)
    path([(x + 4, 36.0), (x + 4, 30.2)], color=BLUE, lw=1.4)

# ---------------------------------------------------------------- API
card(5.5, 12.0, 76.0, 5.0, "API de dados Olist", "", ec=NAVY, fc=NAVY, tc="white", fs=9.4)
ax.text(43.5, 12.9, "cada ferramenta chama um endpoint, que consulta as tabelas", fontsize=7.2, color="#CFE8F0", ha="center", zorder=5)
for key, (x, *_r) in ag.items():
    path([(x + W / 2, 20.6), (x + W / 2, 17.0)], color=NAVY, lw=1.4)
for key, (x, *_r) in ag.items():
    tag(x + W / 2, 18.8, "chamada")

# ---------------------------------------------------------------- dados
ax.add_patch(FancyBboxPatch((1, 0.6), 98.5, 10.2, boxstyle="round,pad=0,rounding_size=0.6", fc="white", ec="#D1D5DB", lw=1, zorder=1))
ax.add_patch(FancyBboxPatch((1, 0.6), 3.4, 10.2, boxstyle="round,pad=0,rounding_size=0.6", fc=LANE, ec="none", zorder=1))
ax.text(2.7, 5.7, "DADOS", rotation=90, ha="center", va="center", fontsize=7.2, fontweight="bold", color=NAVY, zorder=5)
tabelas = ["orders", "order_\nitems", "order_\nreviews", "pro-\nducts", "sellers", "custo-\nmers", "pay-\nments", "geo-\nlocation"]
futuras = ["rastrea-\nmento\n(futuro)", "políticas\n(futuro)", "atendi-\nmento\n(futuro)"]
xs = [9.2 + i * 8.55 for i in range(len(tabelas) + len(futuras))]
for cx, nome in zip(xs, tabelas + futuras):
    cylinder(cx, 2.2, nome, future=nome in futuras)
for cx in xs[:len(tabelas)]:
    ax.plot([cx, cx], [7.8, 12.0], color=NAVY, lw=0.9, zorder=2)
for cx in xs[len(tabelas):]:
    ax.plot([cx, cx, 81.5], [7.8, 11.4, 11.4], color=FUTURE, lw=0.9, ls=(0, (3, 2)), zorder=2)

# ---------------------------------------------------------------- governança (direita)
ax.add_patch(FancyBboxPatch((GOV_X, 33.0), GOV_W, 41.4, boxstyle="round,pad=0,rounding_size=0.6", fc="white", ec="#F5B5B5", lw=1.2, zorder=1))
gx = GOV_X + GOV_W / 2
ax.text(gx, 72.8, "GOVERNANÇA", fontsize=8.6, fontweight="bold", color=NAVY, ha="center", zorder=5)
ax.text(gx, 70.6, "nada sai para o\ncliente sem\naprovação", fontsize=6.8, color=INK, ha="center", va="center", style="italic", zorder=5, linespacing=1.1)
card(GOV_X + 0.8, 52.0, GOV_W - 1.6, 8.8, "Agente\nValidador", "confere fontes,\nregras e limites\nde autonomia", ec=CORAL, tc=NAVY, fs=8.4, sfs=6.9)
ax.add_patch(FancyBboxPatch((GOV_X + 0.8, 35.0), GOV_W - 1.6, 11.6, boxstyle="round,pad=0,rounding_size=1.2", fc="#FFF1F1", ec=CORAL, lw=2, zorder=3))
person(gx, 43.4, "", color=NAVY, bg="#FFF1F1")
ax.text(gx, 40.2, "Aprovação\nhumana", fontsize=8.4, fontweight="bold", color=NAVY, ha="center", va="center", zorder=4, linespacing=1.1)
ax.text(gx, 37.0, "atendente ou\nsupervisor decide", fontsize=6.8, color=INK, ha="center", va="center", zorder=4, linespacing=1.1)
path([(gx, 52.0), (gx, 46.6)], color=CORAL, lw=1.5)
tag(gx, 49.3, "afeta o\ncliente? sim", fs=6.8)
# saídas para os usuários
path([(GOV_X + GOV_W - 0.8, 41.0), (99.3, 41.0), (99.3, 67.6), (MAIN_R + 0.2, 67.6)], color=CORAL, lw=1.5)
tag(gx + 0.5, 67.6, "resposta\naprovada", fs=6.8)
path([(GOV_X + 3.0, 60.8), (GOV_X + 3.0, 64.6), (MAIN_R + 0.2, 64.6)], color=BLUE, lw=1.3, ls=(0, (4, 2)))
tag(gx + 1.5, 62.7, "não: alerta ou\nrelatório interno", fs=6.4)

# ---------------------------------------------------------------- monitoramento
ax.add_patch(FancyBboxPatch((GOV_X, 12.0), GOV_W, 19.2, boxstyle="round,pad=0,rounding_size=0.8", fc=STICKY, ec="#E8D36A", lw=1, zorder=3))
ax.text(gx, 29.4, "Monitora-\nmento", fontsize=8.6, fontweight="bold", color=NAVY, ha="center", va="center", zorder=4, linespacing=1.05)
ax.text(gx, 26.6, "(LangSmith ou\nLangfuse)", fontsize=6.6, color=MUTED, ha="center", va="center", zorder=4, linespacing=1.1)
ax.text(gx, 18.8, "registra cada\nexecução: o que\nentrou, o que o\nagente respondeu\ne quem aprovou.\nMostra se os\nagentes acertam,\nquanto custam e\nonde erram.",
        fontsize=6.6, color=INK, ha="center", va="center", zorder=4, linespacing=1.25)
path([(82.6, 34.4), (82.6, 22.0), (GOV_X, 22.0)], color=MUTED, lw=1.0, ls=(0, (2, 2)))

ASSETS = ROOT / "docs" / "abnt" / "assets"
for out in (config.FIGURES / "o10_arquitetura.png", ASSETS / "arquitetura_agentes_olist10.png"):
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor=BOARD_BG)
    print(out)
