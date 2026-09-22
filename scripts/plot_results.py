"""Compact paper-style figures from the recorded experimental aggregates."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "results/summary.json").read_text())
OUT = ROOT / "assets/figures"
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({
    "font.family": "serif", "font.serif": ["STIXGeneral"],
    "mathtext.fontset": "stix", "font.size": 10,
    "axes.labelsize": 10, "xtick.labelsize": 9, "ytick.labelsize": 10,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.linewidth": .65, "xtick.major.width": .6, "ytick.major.width": .6,
    "svg.fonttype": "none", "pdf.fonttype": 42,
    "savefig.bbox": "tight", "savefig.pad_inches": .08,
})
GRAY, TEAL, BLUE = "#92999f", "#177b79", "#3c6089"


def save(fig, name):
    for extension in ("png", "svg", "pdf"):
        fig.savefig(OUT / f"{name}.{extension}", dpi=300, facecolor="white")
    plt.close(fig)


text = DATA["text"]
assert len(text["tasks"]) == len(text["base_percent"]) == len(text["adapted_percent"])
fig, ax = plt.subplots(figsize=(5.5, 2.55))
for row, (base, adapted) in enumerate(zip(text["base_percent"], text["adapted_percent"])):
    y = 3 - row
    ax.plot([base, adapted], [y, y], color="#bdcaca", lw=1.5, zorder=2)
    ax.scatter(base, y, s=29, facecolors="white", edgecolors=GRAY, linewidths=1.2, zorder=3)
    ax.scatter(adapted, y, s=32, color=TEAL, linewidths=0, zorder=3)
    for value, color in [(base, "#626a71"), (adapted, TEAL)]:
        ax.annotate(f"{value:.1f}", (value, y), xytext=(0, 7),
                    textcoords="offset points", ha="center", fontsize=9, color=color)
ax.set(xlim=(0, 100), ylim=(-.45, 3.6), yticks=[3, 2, 1, 0],
       yticklabels=text["tasks"], xlabel="Reference-label agreement (%)")
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0, pad=8)
ax.xaxis.set_major_locator(MultipleLocator(20))
ax.grid(axis="x", color="#e7e9eb", lw=.5)
ax.set_axisbelow(True)
ax.legend(handles=[
    Line2D([], [], marker="o", linestyle="none", markerfacecolor="white", markeredgecolor=GRAY, markersize=5, label="Base 0.8B"),
    Line2D([], [], marker="o", linestyle="none", color=TEAL, markersize=5, label="Adapted 0.8B"),
], frameon=False, loc="lower center", bbox_to_anchor=(.5, 1.01), ncol=2,
          fontsize=9, handletextpad=.4, columnspacing=2)
fig.subplots_adjust(left=.19, right=.97, bottom=.2, top=.85)
save(fig, "text_results")


drive = DATA["driving"]
assert len(drive["model_labels"]) == len(drive["pdm"]) == len(drive["latency_p50_ms"]) == 2
fig, ax = plt.subplots(figsize=(4.4, 3.0))
ax.axhline(drive["oracle"], color=GRAY, linestyle=(0, (4, 3)), linewidth=.9)
ax.text(150, drive["oracle"]+.008, f"Candidate oracle  {drive['oracle']:.4f}", fontsize=9, color="#697178")
for i, color in enumerate([TEAL, BLUE]):
    x, y = drive["latency_p50_ms"][i], drive["pdm"][i]
    ax.scatter(x, y, s=44, color=color, edgecolor="white", linewidth=.5, zorder=3)
    ax.annotate(f"{drive['model_labels'][i]}\n({x} ms, {y:.4f})", (x, y),
                xytext=(8, 10) if i == 0 else (-8, 10),
                textcoords="offset points", ha="left" if i == 0 else "right",
                fontsize=9, color=color, linespacing=1.4)
ax.set(xlim=(140, 375), ylim=(.48, .72), xlabel="End-to-end latency, p50 (ms)", ylabel="PDM score")
ax.xaxis.set_major_locator(MultipleLocator(50))
ax.yaxis.set_major_locator(MultipleLocator(.05))
ax.grid(color="#e7e9eb", linewidth=.5)
ax.set_axisbelow(True)
fig.subplots_adjust(left=.16, right=.97, bottom=.19, top=.96)
save(fig, "driving_results")
