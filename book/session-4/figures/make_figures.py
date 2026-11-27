"""Draws the static figures for Session 4 (run: python make_figures.py).

Same palette and style as Session 3: blue, amber (dashed where it is a line), teal.
"""
import os
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


# 1. Interest and repayment in each instalment: 12,000 at 5 % over 4 years
K0, i, n = 12000, 0.05, 4
A = K0 * i * (1 + i) ** n / ((1 + i) ** n - 1)
interest, repayment, balance = [], [], K0
for _ in range(n):
    interest.append(balance * i)
    repayment.append(A - balance * i)
    balance -= A - balance * i
years = list(range(1, n + 1))
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.grid(axis="x", visible=False)
ax.set_axisbelow(True)
ax.bar(years, repayment, width=0.6, color=BLUE, label="Repayment", edgecolor="white", linewidth=1.5)
ax.bar(years, interest, width=0.6, bottom=repayment, color=AMBER, label="Interest",
       edgecolor="white", linewidth=1.5)
for x, r, z in zip(years, repayment, interest):
    ax.text(x, r / 2, f"{r:,.0f}", ha="center", va="center", color="white", fontsize=10)
    ax.text(x, r + z + 60, f"interest {z:,.0f}", ha="center", va="bottom", color=INK, fontsize=10)
ax.text(4.42, repayment[-1] / 2, "Repayment", color=INK, va="center")
ax.text(4.42, A - 90, "Interest", color=INK, va="center")
ax.set_xlim(0.5, 5.2); ax.set_ylim(0, 4000)
ax.set_xticks(years); ax.set_xlabel("Year"); ax.set_ylabel("Euros"); money(ax)
ax.set_title(f"Every instalment is {A:,.2f} euros", loc="left", color=INK, fontsize=11)
save(fig, "loan-split.svg")

# 2. Book value: straight-line versus declining balance
t = list(range(6))
straight = [12000 - 2400 * x for x in t]
declining = [12000 * 0.75 ** x for x in t]
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.plot(t, straight, color=BLUE, marker="o", label="Straight-line, 2,400 a year")
ax.plot(t, declining, color=AMBER, linestyle="--", marker="o", label="Declining balance, 25 % a year")
ax.text(5.15, 0, "Straight-line: 0", color=INK, va="center")
ax.text(5.15, declining[-1], f"Declining: {declining[-1]:,.0f}", color=INK, va="center")
ax.set_xlim(0, 6.6); ax.set_ylim(-300, 12800)
ax.set_xlabel("Years after purchase"); ax.set_ylabel("Book value in euros"); money(ax)
ax.legend(loc="upper right")
save(fig, "depreciation.svg")
