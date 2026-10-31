"""Desenha a arquitetura conceitual dos agentes (card OLIST-10) no estilo de um quadro do Miro.

Uso (na raiz do projeto, com o .venv ativo):
    python scripts/diagrama_arquitetura.py

Gera reports/figures/o10_arquitetura.png. Segue as diretrizes visuais do grupo (OLIST-4/7):
retângulos arredondados = agentes; cilindros = bases de dados; ícones de pessoa = usuários;
coral apenas para governança e risco; linhas ortogonais com legenda.
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Rectangle, Wedge

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from olist import config  # noqa: E402

NAVY = "#0A192F"      # cabeçalhos e estrutura
BLUE = "#00B4D8"      # agentes e fluxos
CORAL = "#FF4D4D"     # governança e risco
INK = "#1F2933"
MUTED = "#6B7280"
BOARD_BG = "#F4F5F7"
STICKY = "#FFF4B8"
TOOL_BG = "#E9F9FC"
FUTURE = "#9CA3AF"
LANE = "#E8ECF2"

fig, ax = plt.subplots(figsize=(13, 10))
ax.set_xlim(0, 100); ax.set_ylim(0, 79); ax.axis("off")
fig.patch.set_facecolor(BOARD_BG)

# grade de pontos do quadro (Miro)
for gx in range(0, 101, 2):
    ax.scatter([gx] * 40, list(range(0, 80, 2)), s=0.6, color="#D5D8DE", zorder=0)


def lane(y, h, title, x=1, w=77.5, color=NAVY):
    """Raia com cabeçalho lateral (texto na vertical), como um frame do Miro."""
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.6", fc="white", ec="#D1D5DB", lw=1, zorder=1))
    ax.add_patch(FancyBboxPatch((x, y), 3.4, h, boxstyle="round,pad=0,rounding_size=0.6", fc=LANE, ec="none", zorder=1))
    ax.text(x + 1.7, y + h / 2, title, rotation=90, ha="center", va="center", fontsize=7.6, fontweight="bold", color=color, zorder=5, linespacing=1.1)


def card(x, y, w, h, title, sub="", ec=BLUE, fc="white", tc=NAVY, fs=10, lw=2, sfs=7.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2", fc=fc, ec=ec, lw=lw, zorder=3))
    ax.text(x + w / 2, y + h - (1.7 if sub else h / 2), title, ha="center", va="center", fontsize=fs, fontweight="bold", color=tc, zorder=4)
    if sub:
        ax.text(x + w / 2, y + (h - 2.8) / 2, sub, ha="center", va="center", fontsize=sfs, color=INK, zorder=4, linespacing=1.25)


def person(cx, cy, label, color=NAVY):
    ax.add_patch(Circle((cx, cy + 1.6), 0.9, fc=color, ec="none", zorder=4))
    ax.add_patch(Wedge((cx, cy - 0.4), 1.6, 0, 180, fc=color, ec="none", zorder=4))
    if label:
        ax.text(cx, cy - 1.2, label, ha="center", va="top", fontsize=7.4, color=INK, zorder=4, linespacing=1.15)


def cylinder(cx, y, label, future=False):
    w, h = 7.4, 4.6
    ec = FUTURE if future else NAVY
    fc = "white" if future else "#EEF2F7"
    ls = (0, (3, 2)) if future else "-"
    ax.add_patch(Rectangle((cx - w / 2, y), w, h, fc=fc, ec="none", zorder=3))
    ax.plot([cx - w / 2, cx - w / 2], [y, y + h], color=ec, lw=1.2, ls=ls, zorder=4)
    ax.plot([cx + w / 2, cx + w / 2], [y, y + h], color=ec, lw=1.2, ls=ls, zorder=4)
    ax.add_patch(Ellipse((cx, y), w, 1.4, fc=fc, ec=ec, lw=1.2, ls=ls, zorder=3))
    ax.add_patch(Ellipse((cx, y + h), w, 1.4, fc=fc, ec=ec, lw=1.2, ls=ls, zorder=5))
    ax.text(cx, y + h / 2 - 0.3, label, ha="center", va="center", fontsize=6.5, color=MUTED if future else NAVY, zorder=6, linespacing=1.1)


def tag(x, y, text, color=INK, fs=6.8):
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=color, zorder=7,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#E5E7EB", lw=0.6))


def path(points, color=BLUE, lw=1.6, ls="-", head=True, z=2):
    """Conector ortogonal (lista de pontos) com seta no fim."""
    xs, ys = zip(*points)
    ax.plot(xs, ys, color=color, lw=lw, ls=ls, zorder=z, solid_capstyle="round")
    if head:
        ax.annotate("", xy=points[-1], xytext=points[-2], arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=11), zorder=z)


# ---------------------------------------------------------------- título do quadro
ax.text(1, 78.6, "Olist · Arquitetura conceitual dos agentes", fontsize=13, fontweight="bold", color=NAVY, va="top")
ax.text(1, 76.4, "Fase 1 · desenho conceitual, sem implementação   ·   * ferramenta sugerida, fora da proposta original do Lorran", fontsize=8, color=MUTED, va="top")

# ---------------------------------------------------------------- usuários
lane(65.0, 9.0, "USUÁRIOS E\nGATILHOS")
people = [(13, "Atendente\n(SAC)"), (28, "Logística e\noperação"), (44, "Experiência do\ncliente e qualidade"), (59, "Gestores")]
for cx, lab in people:
    person(cx, 70.0, lab)
card(66.5, 66.6, 10.5, 5.6, "Rotina diária", "varredura dos\npedidos em aberto", ec=NAVY, fs=7.8, sfs=6.8)

# ---------------------------------------------------------------- orquestrador
lane(52.0, 11.0, "ORQUES-\nTRAÇÃO")
card(25, 53.2, 30, 5.6, "Agente Orquestrador (router)", "entende o pedido e escolhe o especialista", ec=NAVY, fc="#EEF2F7")
for cx, _ in people:
    path([(cx, 65.6), (cx, 61.4)], color=NAVY, lw=1.1, head=False)
path([(71.75, 66.6), (71.75, 61.4)], color=NAVY, lw=1.1, head=False)
path([(13, 61.4), (71.75, 61.4)], color=NAVY, lw=1.1, head=False)
path([(40, 61.4), (40, 58.8)], color=NAVY, lw=1.3)
tag(52, 61.4, "pergunta, pedido ou varredura")

# ---------------------------------------------------------------- especialistas
lane(33.0, 17.0, "AGENTES\nESPECIALISTAS")
ag = {
    "voz": (6.0, "Voz do Cliente", "classifica avaliações por tema\ne sentimento, com evidência"),
    "sen": (31.0, "Sentinela de Entregas", "sinaliza pedidos com risco\nde atraso e recomenda ação"),
    "cop": (56.0, "Copiloto de Atendimento", "reúne fatos e prepara a\nresposta para o atendente"),
}
W = 20.0
for key, (x, t, s) in ag.items():
    card(x, 36.0, W, 9.8, t, s, fs=9)
path([(40, 53.2), (40, 48.4)], color=BLUE, lw=1.4, head=False)
path([(16, 48.4), (66, 48.4)], color=BLUE, lw=1.4, head=False)
for key, (x, *_r) in ag.items():
    path([(x + W / 2, 48.4), (x + W / 2, 45.8)], color=BLUE, lw=1.4)
tag(28.5, 48.4, "tarefa + contexto")
# interações entre especialistas
path([(26.0, 40.0), (31.0, 40.0)], color=BLUE, lw=1.3)
ax.text(28.5, 42.4, "temas de\nentrega", fontsize=6.1, color=INK, ha="center", va="center", zorder=6, linespacing=1.05)
path([(51.0, 40.0), (56.0, 40.0)], color=BLUE, lw=1.3)
ax.text(53.5, 42.4, "alerta +\nevidências", fontsize=6.1, color=INK, ha="center", va="center", zorder=6, linespacing=1.05)
# saída dos especialistas para o validador (barramento coral)
for key, (x, *_r) in ag.items():
    path([(x + W - 2, 36.0), (x + W - 2, 34.4)], color=CORAL, lw=1.2, head=False)
path([(24.0, 34.4), (79.2, 34.4), (79.2, 56.0), (80.6, 56.0)], color=CORAL, lw=1.4)
tag(70.5, 34.4, "resposta + evidências", color=CORAL)

# ---------------------------------------------------------------- ferramentas
lane(18.5, 12.6, "FERRAMENTAS\n(TOOLS)")
tools = {
    "voz": ["buscar_avaliacoes", "consultar_contexto_pedido", "resumir_temas_periodo *", "registrar_classificacao *"],
    "sen": ["listar_pedidos_em_aberto", "consultar_pedido", "consultar_rastreamento", "consultar_prazo_postagem *", "calcular_risco_rota *", "historico_vendedor *"],
    "cop": ["consultar_pedido", "buscar_pedidos_do_cliente *", "consultar_pagamento *", "buscar_politica", "consultar_historico_atendimento", "consultar_alertas_agentes"],
}
for key, (x, *_r) in ag.items():
    ax.add_patch(FancyBboxPatch((x, 20.8), W, 9.2, boxstyle="round,pad=0,rounding_size=0.8", fc=TOOL_BG, ec=BLUE, lw=1, ls=(0, (4, 2)), zorder=3))
    for i, tname in enumerate(tools[key]):
        ax.text(x + 0.9, 29.0 - i * 1.5, "▸ " + tname, fontsize=6.4, color=NAVY, va="center", zorder=4, family="DejaVu Sans Mono")
    path([(x + 4, 36.0), (x + 4, 30.0)], color=BLUE, lw=1.3)

# ---------------------------------------------------------------- API
card(6.0, 12.6, 70.0, 4.2, "API de dados Olist", "", ec=NAVY, fc=NAVY, tc="white", fs=9)
ax.text(41, 13.3, "cada ferramenta chama um endpoint, que consulta as tabelas", fontsize=6.6, color="#CFE8F0", ha="center", zorder=5)
for key, (x, *_r) in ag.items():
    path([(x + W / 2, 20.8), (x + W / 2, 16.8)], color=NAVY, lw=1.3)
tag(16, 18.8, "chamada"); tag(41, 18.8, "chamada"); tag(66, 18.8, "chamada")

# ---------------------------------------------------------------- dados
ax.add_patch(FancyBboxPatch((1, 0.6), 98.5, 10.0, boxstyle="round,pad=0,rounding_size=0.6", fc="white", ec="#D1D5DB", lw=1, zorder=1))
ax.add_patch(FancyBboxPatch((1, 0.6), 3.4, 10.0, boxstyle="round,pad=0,rounding_size=0.6", fc=LANE, ec="none", zorder=1))
ax.text(2.7, 5.6, "DADOS", rotation=90, ha="center", va="center", fontsize=7.6, fontweight="bold", color=NAVY, zorder=5)
tabelas = ["orders", "order_items", "order_\nreviews", "products", "sellers", "customers", "payments", "geo-\nlocation"]
futuras = ["rastreamento\n(futuro)", "políticas e\nbase conhec.\n(futuro)", "histórico de\natendimento\n(futuro)"]
xs = [9.5 + i * 8.6 for i in range(len(tabelas) + len(futuras))]
for cx, nome in zip(xs, tabelas + futuras):
    cylinder(cx, 2.4, nome, future=nome in futuras)
for cx in xs[:len(tabelas)]:
    ax.plot([cx, cx], [7.7, 12.6], color=NAVY, lw=0.8, zorder=2)
for cx in xs[len(tabelas):]:
    ax.plot([cx, cx, 76.0], [7.7, 11.4, 11.4], color=FUTURE, lw=0.8, ls=(0, (3, 2)), zorder=2)

# ---------------------------------------------------------------- governança (direita)
ax.add_patch(FancyBboxPatch((80.6, 33.0), 18.9, 41.0, boxstyle="round,pad=0,rounding_size=0.6", fc="white", ec="#F5B5B5", lw=1.2, zorder=1))
ax.text(90.05, 72.6, "GOVERNANÇA", fontsize=8.4, fontweight="bold", color=CORAL, ha="center", zorder=5)
ax.text(90.05, 71.0, "nada sai para o cliente sem aprovação", fontsize=6.0, color=CORAL, ha="center", va="center", style="italic", zorder=5)
card(82.0, 52.0, 16.1, 8.4, "Agente Validador", "confere fontes, regras\ne limites de autonomia", ec=CORAL, fs=8.8, sfs=6.9)
ax.add_patch(FancyBboxPatch((82.0, 35.0), 16.1, 11.0, boxstyle="round,pad=0,rounding_size=1.2", fc="#FFF1F1", ec=CORAL, lw=2, zorder=3))
person(86.0, 40.8, "", color=CORAL)
ax.text(92.6, 43.2, "Aprovação\nhumana", fontsize=8.8, fontweight="bold", color=CORAL, ha="center", va="center", zorder=4)
ax.text(92.6, 38.0, "atendente ou\nsupervisor decide", fontsize=6.9, color=INK, ha="center", va="center", zorder=4)
path([(90.05, 52.0), (90.05, 46.0)], color=CORAL, lw=1.4)
tag(90.05, 49.0, "afeta o cliente? sim", color=CORAL, fs=6.4)
# saídas para os usuários
path([(98.1, 40.5), (99.2, 40.5), (99.2, 68.4), (77.6, 68.4)], color=CORAL, lw=1.4)
tag(89.0, 68.4, "resposta aprovada", color=CORAL, fs=6.5)
path([(84.0, 60.4), (84.0, 65.8), (77.6, 65.8)], color=BLUE, lw=1.2, ls=(0, (4, 2)))
tag(89.6, 63.6, "não: alerta ou\nrelatório interno", fs=6.2)

# ---------------------------------------------------------------- monitoramento
ax.add_patch(FancyBboxPatch((80.6, 12.6), 18.9, 18.4, boxstyle="round,pad=0,rounding_size=0.8", fc=STICKY, ec="#E8D36A", lw=1, zorder=3))
ax.text(90.05, 28.8, "Monitoramento", fontsize=9.2, fontweight="bold", color=NAVY, ha="center", zorder=4)
ax.text(90.05, 26.8, "(ex.: LangSmith ou Langfuse)", fontsize=6.6, color=MUTED, ha="center", zorder=4)
ax.text(90.05, 20.0, "registra cada execução:\no que entrou, o que o\nagente respondeu e\nquem aprovou. Mostra se\nos agentes acertam,\nquanto custam e\nonde erram.",
        fontsize=6.7, color=INK, ha="center", va="center", zorder=4, linespacing=1.3)
path([(79.2, 34.4), (79.2, 22.0), (80.6, 22.0)], color=MUTED, lw=1.0, ls=(0, (2, 2)))

out = config.FIGURES / "o10_arquitetura.png"
fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=BOARD_BG)
print(out)
