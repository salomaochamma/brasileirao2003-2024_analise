from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

PASTA_IMAGENS = Path(__file__).resolve().parent.parent / "images"

SUPERFICIE = "#fcfcfb"
TINTA = "#0b0b0b"
TINTA_SECUNDARIA = "#52514e"
TINTA_SUAVE = "#898781"
GRADE = "#e1e0d9"
EIXO = "#c3c2b7"
DESTAQUE_FUNDO = "#f0efec"

AZUL = "#2a78d6"
LARANJA = "#eb6834"
VERMELHO = "#e34948"
CINZA = "#c3c2b7"

FONTE_DADOS = "Dados: Brasileirao_Dataset · Análise: Raphael Salomão Chamma"

def aplicar_estilo():
    plt.rcParams.update({
        "figure.facecolor": SUPERFICIE,
        "axes.facecolor": SUPERFICIE,
        "savefig.facecolor": SUPERFICIE,
        "figure.dpi": 110,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.3,
        "font.size": 11,
        "text.color": TINTA,
        "axes.labelcolor": TINTA_SECUNDARIA,
        "axes.edgecolor": EIXO,
        "axes.linewidth": 1,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.axisbelow": True,
        "grid.color": GRADE,
        "grid.linewidth": 1,
        "xtick.color": TINTA_SECUNDARIA,
        "ytick.color": TINTA_SECUNDARIA,
        "xtick.major.size": 0,
        "ytick.major.size": 0,
        "xtick.major.pad": 8,
        "ytick.major.pad": 8,
        "lines.linewidth": 2,
        "lines.solid_capstyle": "round",
        "lines.solid_joinstyle": "round",
        "legend.frameon": False,
    })


def titulo(ax, texto, subtitulo=None, espaco=0):
    ax.annotate(
        texto, xy=(0, 1), xycoords="axes fraction",
        xytext=(0, 34 + espaco), textcoords="offset points",
        fontsize=15, fontweight="bold", ha="left", va="bottom",
    )
    if subtitulo:
        ax.annotate(
            subtitulo, xy=(0, 1), xycoords="axes fraction",
            xytext=(0, 14 + espaco), textcoords="offset points",
            fontsize=11, color=TINTA_SECUNDARIA, ha="left", va="bottom",
        )


def fonte(ax, deslocamento=-42, texto=FONTE_DADOS):
    ax.annotate(
        texto, xy=(0, 0), xycoords="axes fraction",
        xytext=(0, deslocamento), textcoords="offset points",
        fontsize=9, color=TINTA_SUAVE, ha="left", va="top",
    )


def eixo_percentual(eixo, casas=0):
    eixo.set_major_formatter(PercentFormatter(1, decimals=casas))


def salvar(fig, nome):
    PASTA_IMAGENS.mkdir(exist_ok=True)
    fig.savefig(PASTA_IMAGENS / nome)
