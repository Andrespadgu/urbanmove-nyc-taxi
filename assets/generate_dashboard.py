"""
Regenerates assets/dashboard.png from the figures in docs/.
Run from the project root: python assets/generate_dashboard.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.image import imread

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS  = os.path.join(ROOT, "docs")
OUT   = os.path.join(ROOT, "assets", "dashboard.png")

BG   = "#0D1B2A"
CIAN = "#00B4D8"
WHT  = "#FFFFFF"

panels = [
    ("fig_resumen_entropia_franja.png", "Shannon Entropy by Time Slot",        "H(zone|franja) · 6 categories"),
    ("fig4_kl_divergencia.png",         "KL Divergence: Weekday vs Weekend",   "KL = 0.164 bits · 3.71% overhead"),
    ("fig_rec1_posicionamiento.png",    "Driver Positioning · Peak Coverage",  "88.2% demand in 3 zones · 17h–22h"),
    ("fig_rec3_modelos_separados.png",  "GMM Dispatch Models · Ambiguous",     "23.4% ambiguous → 2 models needed"),
]

fig = plt.figure(figsize=(20, 11), facecolor=BG)

fig.text(0.5, 0.965, "UrbanMove — Unsupervised Analysis of NYC Taxi Demand",
         ha="center", va="top", fontsize=22, fontweight="bold", color=WHT)
fig.text(0.5, 0.935,
         "50,000 trips · Information Theory · K-Means/DBSCAN · GMM/EM · 3 Quantified Operational Recommendations",
         ha="center", va="top", fontsize=11, color="#90CAD8")

ax_line = fig.add_axes([0.04, 0.920, 0.92, 0.003])
ax_line.set_facecolor(CIAN)
ax_line.axis("off")

gs = gridspec.GridSpec(2, 2, figure=fig,
                       left=0.04, right=0.96, top=0.905, bottom=0.07,
                       wspace=0.025, hspace=0.08)

for idx, (fname, title, subtitle) in enumerate(panels):
    row, col = divmod(idx, 2)
    img = imread(os.path.join(DOCS, fname))
    ax = fig.add_subplot(gs[row, col])
    ax.imshow(img, aspect="auto")
    ax.set_facecolor(BG)
    for spine in ax.spines.values():
        spine.set_edgecolor(CIAN)
        spine.set_linewidth(1.2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(0.02, 0.97, title, transform=ax.transAxes,
            fontsize=9.5, fontweight="bold", color=WHT, va="top", ha="left",
            bbox=dict(boxstyle="round,pad=0.3", facecolor=BG, alpha=0.8, edgecolor="none"))
    ax.text(0.02, 0.865, subtitle, transform=ax.transAxes,
            fontsize=7.5, color=CIAN, va="top", ha="left",
            bbox=dict(boxstyle="round,pad=0.2", facecolor=BG, alpha=0.7, edgecolor="none"))

fig.text(0.5, 0.025,
         "Dataset: NYC Taxi Trip Duration (Kaggle) · Jan–Jun 2016 · Seed 42 · scikit-learn 1.3",
         ha="center", va="bottom", fontsize=9, color="#90CAD8")

fig.savefig(OUT, dpi=150, bbox_inches="tight", facecolor=BG)
plt.close()
print(f"dashboard saved → {OUT}")
