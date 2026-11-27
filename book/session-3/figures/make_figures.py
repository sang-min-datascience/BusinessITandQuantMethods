"""Draws the static figures for Session 3 (run: python make_figures.py).

Colours: blue, amber, teal from the book's palette (validated for colour-vision
deficiencies); amber lines are dashed as a second cue. Text stays in ink colours.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, AMBER, TEAL = "#2165B6", "#E9A23B", "#2A9D8F"
INK, MUTED, GRID = "#2B2B2B", "#6B6B6B", "#E4E4E4"
HERE = os.path.dirname(os.path.abspath(__file__))

plt.rcParams.update({
    "font.family": "sans-serif", "font.size": 11, "axes.edgecolor": "#BBBBBB",
    "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
    "grid.color": GRID, "grid.linewidth": 0.8, "lines.linewidth": 2.2,
    "svg.fonttype": "none", "legend.frameon": False,
})


def money(ax):
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))


def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, name), format="svg")
    plt.close(fig)


# 1. Cost and revenue, break-even at 25 bikes
q = np.linspace(0, 50, 200)
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.plot(q, 2600 + 260 * q, color=BLUE, label="Cost C(q) = 2600 + 260q")
ax.plot(q, 364 * q, color=AMBER, linestyle="--", label="Revenue R(q) = 364q")
ax.plot([25], [9100], "o", ms=8, color=INK, mec="white", mew=2, zorder=5)
ax.annotate("Break-even\n25 bikes, €9,100", (25, 9100), (29, 6200), color=INK,
            arrowprops=dict(arrowstyle="-", color=MUTED))
ax.text(50.5, 2600 + 260 * 50, "Cost", color=INK, va="center")
ax.text(50.5, 364 * 50, "Revenue", color=INK, va="center")
ax.text(4, 1400, "loss", color=MUTED, style="italic")
ax.text(40, 17500, "profit", color=MUTED, style="italic")
ax.set_xlim(0, 56); ax.set_ylim(0, 20000)
ax.set_xlabel("Bikes sold per month, q"); ax.set_ylabel("Euros per month"); money(ax)
ax.legend(loc="upper left")
save(fig, "cost-revenue.svg")

# 2. Average cost per bike falls towards 260
q = np.linspace(5, 60, 300)
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.plot(q, 2600 / q + 260, color=BLUE, label="Average cost AC(q) = 2600/q + 260")
ax.axhline(364, color=AMBER, linestyle="--", label="Price p = 364")
ax.axhline(260, color=MUTED, linewidth=1, linestyle=":")
ax.text(60.5, 260, "260", color=MUTED, va="center")
ax.plot([25], [364], "o", ms=8, color=INK, mec="white", mew=2, zorder=5)
ax.annotate("At 25 bikes, average cost = price", (25, 364), (30, 470), color=INK,
            arrowprops=dict(arrowstyle="-", color=MUTED))
ax.set_xlim(0, 64); ax.set_ylim(200, 800)
ax.set_xlabel("Bikes sold per month, q"); ax.set_ylabel("Euros per bike"); money(ax)
ax.legend(loc="upper right")
save(fig, "average-cost.svg")

# 3. Profit parabola with two break-even points and a maximum
q = np.linspace(0, 85, 300)
P = -2 * q**2 + 170 * q - 2600
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.axhline(0, color="#999999", linewidth=1)
ax.plot(q, P, color=TEAL)
for x in (20, 65):
    ax.plot([x], [0], "o", ms=8, color=INK, mec="white", mew=2, zorder=5)
    if x == 20:
        ax.text(x - 1.5, 120, f"q = {x}", ha="right", color=INK)
    else:
        ax.text(x + 1.5, 120, f"q = {x}", ha="left", color=INK)
ax.plot([42.5], [1012.5], "o", ms=8, color=INK, mec="white", mew=2, zorder=5)
ax.annotate("Maximum: q = 42.5, P = €1,012.50", (42.5, 1012.5), (46, 1150), color=INK,
            arrowprops=dict(arrowstyle="-", color=MUTED))
ax.set_xlim(0, 85); ax.set_ylim(-2800, 1500)
ax.set_xlabel("Bikes sold per month, q"); ax.set_ylabel("Profit in euros per month"); money(ax)
save(fig, "profit-parabola.svg")

# 4. Exponential versus linear growth
t = np.linspace(0, 36, 200)
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.plot(t, 10000 * 1.05**t, color=BLUE, label="+5 % per month: 10,000 · 1.05ᵗ")
ax.plot(t, 10000 + 500 * t, color=AMBER, linestyle="--", label="+€500 per month: 10,000 + 500t")
ax.text(36.5, 10000 * 1.05**36, "€57,918", color=INK, va="center")
ax.text(36.5, 28000, "€28,000", color=INK, va="center")
ax.set_xlim(0, 42); ax.set_ylim(0, 62000)
ax.set_xlabel("Months, t"); ax.set_ylabel("Monthly sales in euros"); money(ax)
ax.legend(loc="upper left")
save(fig, "exp-vs-linear.svg")

print("figures written to", HERE)
