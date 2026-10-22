import json
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # non-interactive backend — saves file without needing a display
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from matplotlib.gridspec import GridSpec

# ── Load & clean ──────────────────────────────────────────────────────────────

with open("nadlan_deals.json", encoding="utf-8") as f:
    raw = json.load(f)

df = pd.DataFrame(raw)

# Parse dates
df["dealDate"] = pd.to_datetime(df["dealDate"], errors="coerce")
df["year"]     = df["dealDate"].dt.year
df["quarter"]  = df["dealDate"].dt.to_period("Q")

# Keep only residential apartments (filter out offices, stores, parking, land…)
RESIDENTIAL = {"דירה בבית קומות", "דירה", "דירת גן"}
df = df[df["dealNature"].isin(RESIDENTIAL)].copy()

# Drop rows without price or date
df = df.dropna(subset=["dealAmount", "dealDate", "year"])

# Remove obvious outliers (deals < 50k or > 20M ₪)
df = df[(df["dealAmount"] >= 50_000) & (df["dealAmount"] <= 20_000_000)]

# Normalize room counts to display strings
def room_label(r):
    if pd.isna(r):
        return "Unknown"
    if r == int(r):
        return f"{int(r)} rooms"
    return f"{r} rooms"

df["roomLabel"] = df["roomNum"].apply(room_label)

# Map Hebrew floor names → numeric
FLOOR_MAP = {
    "מרתף": -1, "קרקע": 0, "קומה \u200e0\u200f": 0, "עמודים": 0,
    "ראשונה": 1, "קומה \u200e1\u200f": 1,
    "שניה": 2,  "קומה \u200e2\u200f": 2,
    "שלישית": 3, "רביעית": 4, "חמישית": 5,
    "שישית": 6, "שביעית": 7, "שמינית": 8,
    "תשיעית": 9, "עשירית": 10, "אחת עשרה": 11,
    "שמונה עשרה": 18,
    "ביניים": 1, "בינים": 1,
    "שישית+שביעית": 6, "שישית שביעית": 6,
    "שביעית+שמינית": 7, "חמישית + שישית": 5,
    "שמינית+תשיעית": 8, "רביעית וחמישית": 4,
}
df["floorNum"] = df["floor"].map(FLOOR_MAP)

print(f"Residential deals after filtering: {len(df)}")
print(f"Year range: {int(df['year'].min())} – {int(df['year'].max())}")
print(f"Price range: ₪{df['dealAmount'].min():,.0f} – ₪{df['dealAmount'].max():,.0f}")

# ── Helper: format ₪ axis ─────────────────────────────────────────────────────

def shekel_fmt(x, _):
    if x >= 1_000_000:
        return f"₪{x/1_000_000:.1f}M"
    return f"₪{x/1_000:.0f}K"

COLORS = plt.cm.tab10.colors

# ── Figure layout ─────────────────────────────────────────────────────────────

fig = plt.figure(figsize=(18, 22))
fig.patch.set_facecolor("#f8f9fa")
gs = GridSpec(4, 2, figure=fig, hspace=0.45, wspace=0.3)

# ── 1. Median price per year ──────────────────────────────────────────────────

ax1 = fig.add_subplot(gs[0, :])
yearly = (
    df.groupby("year")["dealAmount"]
    .agg(median="median", q25=lambda x: x.quantile(0.25), q75=lambda x: x.quantile(0.75))
    .reset_index()
)
ax1.fill_between(yearly["year"], yearly["q25"], yearly["q75"],
                 alpha=0.2, color=COLORS[0], label="25–75th percentile")
ax1.plot(yearly["year"], yearly["median"], "o-", color=COLORS[0],
         linewidth=2.5, markersize=6, label="Median price")
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(shekel_fmt))
ax1.set_title("Median Apartment Sale Price — Herzl St., Bat Yam (1998–2025)",
              fontsize=14, fontweight="bold", pad=10)
ax1.set_xlabel("Year")
ax1.set_ylabel("Sale Price (₪)")
ax1.legend()
ax1.grid(axis="y", linestyle="--", alpha=0.4)
ax1.set_facecolor("white")

# Annotate first and last year
first_y = yearly.iloc[0]
last_y  = yearly.iloc[-1]
ax1.annotate(f"₪{first_y['median']/1e6:.2f}M", xy=(first_y["year"], first_y["median"]),
             xytext=(5, 12), textcoords="offset points", fontsize=9, color=COLORS[0])
ax1.annotate(f"₪{last_y['median']/1e6:.2f}M", xy=(last_y["year"], last_y["median"]),
             xytext=(5, 12), textcoords="offset points", fontsize=9, color=COLORS[0])

# ── 2. Price per sqm per year ─────────────────────────────────────────────────

ax2 = fig.add_subplot(gs[1, :])
sqm_df = df.dropna(subset=["priceSM"])
sqm_df = sqm_df[sqm_df["priceSM"] > 1000]  # filter bad values
yearly_sqm = (
    sqm_df.groupby("year")["priceSM"]
    .agg(median="median", q25=lambda x: x.quantile(0.25), q75=lambda x: x.quantile(0.75))
    .reset_index()
)
ax2.fill_between(yearly_sqm["year"], yearly_sqm["q25"], yearly_sqm["q75"],
                 alpha=0.2, color=COLORS[1])
ax2.plot(yearly_sqm["year"], yearly_sqm["median"], "s-", color=COLORS[1],
         linewidth=2.5, markersize=6, label="Median ₪/m²")
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₪{x:,.0f}"))
ax2.set_title("Median Price per m² Over Time", fontsize=13, fontweight="bold", pad=10)
ax2.set_xlabel("Year")
ax2.set_ylabel("₪ per m²")
ax2.legend()
ax2.grid(axis="y", linestyle="--", alpha=0.4)
ax2.set_facecolor("white")

# ── 3. Median price by room count over time ───────────────────────────────────

ax3 = fig.add_subplot(gs[2, :])
room_focus = [2.0, 3.0, 3.5, 4.0, 4.5, 5.0]
room_data  = df[df["roomNum"].isin(room_focus)]
pivot = (
    room_data.groupby(["year", "roomNum"])["dealAmount"]
    .median()
    .unstack("roomNum")
)
for i, rooms in enumerate(room_focus):
    if rooms in pivot.columns:
        series = pivot[rooms].dropna()
        label = f"{rooms:.0f}" if rooms == int(rooms) else f"{rooms}"
        ax3.plot(series.index, series.values, "o-", linewidth=2,
                 markersize=4, color=COLORS[i], label=f"{label} rooms")

ax3.yaxis.set_major_formatter(mticker.FuncFormatter(shekel_fmt))
ax3.set_title("Median Price by Number of Rooms", fontsize=13, fontweight="bold", pad=10)
ax3.set_xlabel("Year")
ax3.set_ylabel("Median Sale Price (₪)")
ax3.legend(title="Rooms", ncol=3)
ax3.grid(axis="y", linestyle="--", alpha=0.4)
ax3.set_facecolor("white")

# ── 4. Deal volume per year ───────────────────────────────────────────────────

ax4 = fig.add_subplot(gs[3, 0])
vol = df.groupby("year").size().reset_index(name="count")
bars = ax4.bar(vol["year"], vol["count"], color=COLORS[2], alpha=0.8, width=0.7)
ax4.set_title("Number of Deals per Year", fontsize=12, fontweight="bold", pad=8)
ax4.set_xlabel("Year")
ax4.set_ylabel("Number of Deals")
ax4.grid(axis="y", linestyle="--", alpha=0.4)
ax4.set_facecolor("white")

# ── 5. Price distribution: 1998–2009 vs 2010–2019 vs 2020–2025 ───────────────

ax5 = fig.add_subplot(gs[3, 1])
periods = [
    ("1998–2009", df[df["year"] <= 2009]["dealAmount"], COLORS[3]),
    ("2010–2019", df[(df["year"] >= 2010) & (df["year"] <= 2019)]["dealAmount"], COLORS[4]),
    ("2020–2025", df[df["year"] >= 2020]["dealAmount"], COLORS[0]),
]
for label, values, color in periods:
    vals = values[values <= 5_000_000]  # cap at 5M for readability
    ax5.hist(vals / 1e6, bins=30, alpha=0.6, color=color, label=label, density=True)

ax5.set_title("Price Distribution by Era", fontsize=12, fontweight="bold", pad=8)
ax5.set_xlabel("Sale Price (₪M)")
ax5.set_ylabel("Density")
ax5.legend()
ax5.grid(axis="y", linestyle="--", alpha=0.4)
ax5.set_facecolor("white")

# ── Save ──────────────────────────────────────────────────────────────────────

plt.savefig("nadlan_analysis.png", dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print("Saved to nadlan_analysis.png")

# ── Print summary table ───────────────────────────────────────────────────────

print("\n── Median price by year ──")
summary = df.groupby("year").agg(
    deals=("dealAmount", "count"),
    median_price=("dealAmount", "median"),
    median_sqm=("priceSM", "median"),
).reset_index()
summary["median_price"] = summary["median_price"].apply(lambda x: f"₪{x:,.0f}")
summary["median_sqm"]   = summary["median_sqm"].apply(lambda x: f"₪{x:,.0f}" if pd.notna(x) else "–")
print(summary.to_string(index=False))

print("Opening chart...")
import subprocess
subprocess.Popen(["open", "nadlan_analysis.png"])
