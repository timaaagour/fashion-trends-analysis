"""
Fashion Trends Analysis — Google Trends 2022–2025
Data Analyst: Fatima Aagour
Analyse de 3 tendances mode : Y2K Fashion, Quiet Luxury, Dopamine Dressing
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)

# ─────────────────────────────────────────
# 1. DONNÉES SIMULÉES (reproduction fidèle du PDF)
# ─────────────────────────────────────────

dates = pd.date_range("2022-01-01", "2025-10-01", freq="MS")

def simulate_trend(base, peak_month, peak_value, noise=8, trend=0):
    values = []
    for i, d in enumerate(dates):
        seasonal = np.sin(2 * np.pi * (d.month - peak_month) / 12) * (peak_value - base) / 2
        growth = trend * i / len(dates)
        noise_val = np.random.normal(0, noise)
        val = base + (peak_value - base) / 2 + seasonal + growth + noise_val
        values.append(max(0, min(100, val)))
    return values

# Y2K : stable et populaire autour de 55-65
y2k = simulate_trend(base=50, peak_month=7, peak_value=75, noise=10, trend=5)
# Quiet Luxury : pic 2023, ralentissement
quiet = []
for i, d in enumerate(dates):
    if d.year == 2022:
        v = np.random.uniform(2, 8)
    elif d.year == 2023 and d.month <= 6:
        v = 5 + (d.month * 3.5) + np.random.uniform(-2, 2)
    elif d.year == 2023 and d.month > 6:
        v = 28 - ((d.month - 6) * 1.2) + np.random.uniform(-2, 2)
    elif d.year == 2024:
        v = np.random.uniform(14, 22)
    else:
        v = np.random.uniform(18, 28)
    quiet.append(max(0, min(100, v)))

# Dopamine Dressing : quasi nul puis regain fort 2025
dopamine = []
for i, d in enumerate(dates):
    if d.year <= 2024:
        v = np.random.uniform(0, 6)
    else:
        v = 20 + (d.month * 6) + np.random.uniform(-3, 3)
    dopamine.append(max(0, min(100, v)))

df = pd.DataFrame({
    "date": dates,
    "Y2K Fashion": y2k,
    "Quiet Luxury": quiet,
    "Dopamine Dressing": dopamine,
})
df.to_csv("/home/claude/fashion_project/data/fashion_trends.csv", index=False)
print(f"✅ Dataset: {len(df)} mois | 2022–2025")

# ─────────────────────────────────────────
# 2. PALETTE & STYLE
# ─────────────────────────────────────────
GOLD   = "#C9A84C"
DARK   = "#1A1A1A"
CREAM  = "#F5F0E8"
GRAY   = "#888888"
LIGHT  = "#E8E0D0"
BLUE   = "#4A90D9"
PINK   = "#E8557A"

COLORS = {
    "Y2K Fashion":      BLUE,
    "Quiet Luxury":     GOLD,
    "Dopamine Dressing": PINK,
}

plt.rcParams.update({
    "font.family": "serif",
    "axes.facecolor": CREAM,
    "figure.facecolor": CREAM,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": LIGHT,
    "axes.labelcolor": DARK,
    "xtick.color": DARK,
    "ytick.color": DARK,
    "text.color": DARK,
})

# ─────────────────────────────────────────
# 3. VIZ 1 — TIME SERIES (reproduction du PDF)
# ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(13, 6), facecolor=CREAM)
ax.set_facecolor(CREAM)

for col, color in COLORS.items():
    ax.plot(df["date"], df[col], linewidth=2, color=color, label=col)
    ax.fill_between(df["date"], df[col], alpha=0.07, color=color)

ax.set_title("Fashion Trends on Google (2022–2025)", fontsize=14, fontweight="bold",
             color=DARK, pad=15)
ax.set_xlabel("Date", fontsize=10, color=GRAY)
ax.set_ylabel("Popularity Index", fontsize=10, color=GRAY)
ax.legend(frameon=False, fontsize=10)
ax.set_ylim(0, 110)
ax.spines["bottom"].set_color(GOLD)
ax.spines["bottom"].set_linewidth(1.5)

# Annotations clés
ax.axvline(pd.Timestamp("2023-06-01"), color=GOLD, linestyle="--", alpha=0.4, linewidth=1)
ax.text(pd.Timestamp("2023-07-01"), 35, "Pic Quiet Luxury", fontsize=8, color=GOLD, alpha=0.8)
ax.axvline(pd.Timestamp("2025-01-01"), color=PINK, linestyle="--", alpha=0.4, linewidth=1)
ax.text(pd.Timestamp("2025-02-01"), 10, "Regain\nDopamine", fontsize=8, color=PINK, alpha=0.8)

plt.tight_layout()
plt.savefig("/home/claude/fashion_project/images/01_time_series.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Viz 1 — Time series")

# ─────────────────────────────────────────
# 4. VIZ 2 — HEATMAP SAISONNIÈRE
# ─────────────────────────────────────────
df["year"]  = df["date"].dt.year
df["month"] = df["date"].dt.month
months_fr = ["Jan","Fév","Mar","Avr","Mai","Jun","Jul","Aoû","Sep","Oct","Nov","Déc"]

fig, axes = plt.subplots(1, 3, figsize=(15, 4), facecolor=CREAM)
fig.suptitle("Heatmap saisonnière — Popularité par mois et année", fontsize=13,
             fontweight="bold", color=DARK, y=1.02)

cmaps = ["Blues", "YlOrBr", "RdPu"]
trends = ["Y2K Fashion", "Quiet Luxury", "Dopamine Dressing"]

for ax, trend, cmap in zip(axes, trends, cmaps):
    ax.set_facecolor(CREAM)
    pivot = df.pivot_table(index="year", columns="month", values=trend)
    pivot.columns = months_fr[:len(pivot.columns)]

    im = ax.imshow(pivot.values, aspect="auto", cmap=cmap, vmin=0, vmax=100)
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns, fontsize=8, rotation=45)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index, fontsize=9)
    ax.set_title(trend, fontsize=11, fontweight="bold", color=DARK, pad=8)

    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            val = pivot.values[i, j]
            if not np.isnan(val):
                ax.text(j, i, f"{val:.0f}", ha="center", va="center",
                        fontsize=7, color="white" if val > 50 else DARK)

    plt.colorbar(im, ax=ax, shrink=0.8)

plt.tight_layout()
plt.savefig("/home/claude/fashion_project/images/02_heatmap_saisonniere.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Viz 2 — Heatmap saisonnière")

# ─────────────────────────────────────────
# 5. VIZ 3 — DASHBOARD SYNTHÈSE
# ─────────────────────────────────────────
fig = plt.figure(figsize=(14, 8), facecolor=CREAM)
fig.suptitle("Fashion Trends Dashboard — Synthèse 2022–2025", fontsize=15,
             fontweight="bold", color=DARK, y=0.98)

# Moyennes par année
ax1 = fig.add_subplot(2, 3, (1, 2))
ax1.set_facecolor(CREAM)
yearly = df.groupby("year")[trends].mean()
x = np.arange(len(yearly))
w = 0.25
for i, (trend, color) in enumerate(COLORS.items()):
    ax1.bar(x + i*w, yearly[trend], width=w, color=color, label=trend,
            edgecolor="white", linewidth=0.5)
ax1.set_xticks(x + w)
ax1.set_xticklabels(yearly.index)
ax1.set_title("Popularité moyenne par année", fontsize=11, fontweight="bold", color=DARK)
ax1.legend(frameon=False, fontsize=8)
ax1.spines["bottom"].set_color(GOLD)

# Dernière valeur connue
ax2 = fig.add_subplot(2, 3, 3)
ax2.set_facecolor(CREAM)
last_vals = df.iloc[-1][trends]
bars = ax2.barh(trends, last_vals.values,
                color=[COLORS[t] for t in trends], edgecolor="white", height=0.5)
for bar, val in zip(bars, last_vals.values):
    ax2.text(val + 1, bar.get_y() + bar.get_height()/2,
             f"{val:.0f}", va="center", fontsize=10, color=DARK)
ax2.set_title("Score Oct. 2025", fontsize=11, fontweight="bold", color=DARK)
ax2.set_xlim(0, 110)
ax2.spines["bottom"].set_color(GOLD)

# Insights textuels
ax3 = fig.add_subplot(2, 1, 2)
ax3.set_facecolor("#EDE8DC")
ax3.axis("off")
insights = [
    ("Y2K Fashion", BLUE,   "Tendance stable et toujours populaire\nMoyenne 2022–2025 : ~58/100"),
    ("Quiet Luxury", GOLD,   "Pic en mid-2023, puis ralentissement progressif\nMoyenne 2023 : ~22/100"),
    ("Dopamine Dressing", PINK, "Quasi absent jusqu'en 2025\nRegain fort : +400% en 2025"),
]
for i, (label, color, text) in enumerate(insights):
    x_pos = 0.05 + i * 0.33
    ax3.add_patch(mpatches.FancyBboxPatch((x_pos, 0.1), 0.28, 0.8,
                  boxstyle="round,pad=0.02", facecolor="white",
                  edgecolor=color, linewidth=2, transform=ax3.transAxes))
    ax3.text(x_pos + 0.14, 0.75, f"■ {label}", ha="center", va="center",
             fontsize=10, fontweight="bold", color=color, transform=ax3.transAxes)
    ax3.text(x_pos + 0.14, 0.38, text, ha="center", va="center",
             fontsize=9, color=DARK, transform=ax3.transAxes, linespacing=1.6)

ax3.set_title("Insights clés", fontsize=11, fontweight="bold", color=DARK, pad=8)

plt.tight_layout()
plt.savefig("/home/claude/fashion_project/images/03_dashboard_synthese.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Viz 3 — Dashboard synthèse")

# ─────────────────────────────────────────
# 6. VIZ 4 — CONCLUSION (style PDF)
# ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6), facecolor="#C4B89A")
ax.set_facecolor("#C4B89A")
ax.axis("off")

ax.text(0.5, 0.88, "Ce que nous dit la data :", ha="center", va="center",
        fontsize=18, fontweight="bold", color=DARK, transform=ax.transAxes,
        fontfamily="serif")

conclusions = [
    (BLUE,  "Y2K",              "Tendance stable et toujours populaire"),
    (GOLD,  "Quiet Luxury",     "Un pic en 2023, puis ralentissement"),
    (PINK,  "Dopamine Dressing","Regain fort en 2025"),
]

for i, (color, label, text) in enumerate(conclusions):
    y = 0.62 - i * 0.18
    ax.add_patch(plt.Rectangle((0.08, y - 0.04), 0.025, 0.07,
                 facecolor=color, transform=ax.transAxes))
    ax.text(0.12, y, f"{label} : ", ha="left", va="center",
            fontsize=13, fontweight="bold", color=color, transform=ax.transAxes)
    ax.text(0.12 + len(label)*0.012, y, text, ha="left", va="center",
            fontsize=12, color=DARK, transform=ax.transAxes)

ax.add_patch(plt.Rectangle((0.15, 0.08), 0.70, 0.12,
             facecolor=DARK, transform=ax.transAxes, zorder=5))
ax.text(0.5, 0.14, "2025 = Sobriété chic + Audace colorée",
        ha="center", va="center", fontsize=13, fontweight="bold",
        color="white", transform=ax.transAxes, zorder=6)

ax.text(0.5, 0.02, "Par Fatima Aagour | Data x Mode",
        ha="center", va="center", fontsize=9, color=DARK,
        transform=ax.transAxes, style="italic")

plt.tight_layout()
plt.savefig("/home/claude/fashion_project/images/04_conclusion.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Viz 4 — Conclusion")

print("\n✅ Toutes les visualisations générées dans /images/")
