"""Shared matplotlib style for the thesis figures."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

# Prefer a serif CJK font that also contains the Unicode minus sign.
_CJK_CANDIDATES = ["Noto Serif CJK SC", "Noto Sans CJK SC", "DengXian",
                   "Source Han Serif SC", "Microsoft YaHei", "SimHei",
                   "WenQuanYi Zen Hei", "AR PL UMing CN"]
_available = {f.name for f in font_manager.fontManager.ttflist}
CJK_FONT = next((name for name in _CJK_CANDIDATES if name in _available), None)

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ([CJK_FONT] if CJK_FONT else []) + ["DejaVu Serif"],
    "axes.unicode_minus": False,
    "mathtext.fontset": "cm",
    "font.size": 10.0,
    "axes.labelsize": 10.5,
    "axes.titlesize": 10.5,
    "legend.fontsize": 9.0,
    "xtick.labelsize": 9.0,
    "ytick.labelsize": 9.0,
    "axes.linewidth": 0.9,
    "lines.linewidth": 1.5,
    "lines.markersize": 4.2,
    "figure.dpi": 120,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

# Okabe-Ito colour-blind safe palette
C = {
    "blue": "#0072B2",
    "orange": "#E69F00",
    "green": "#009E73",
    "red": "#D55E00",
    "purple": "#CC79A7",
    "sky": "#56B4E9",
    "yellow": "#F0E442",
    "black": "#000000",
    "grey": "#666666",
}
THETA_COLORS = ["#0072B2", "#56B4E9", "#009E73", "#E69F00", "#D55E00"]


def save(fig, path):
    fig.savefig(path)
    plt.close(fig)
    print("wrote", path)
