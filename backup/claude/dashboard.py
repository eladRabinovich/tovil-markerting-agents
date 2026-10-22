import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from pathlib import Path

DATA_FILE = Path(__file__).parent / "nadlan_deals.json"

st.set_page_config(page_title="Nadlan — Herzl St. Bat Yam", layout="wide")

# Dark theme constants matching Streamlit's dark mode
BG      = "#0e1117"   # Streamlit dark background
PLOT_BG = "#1a1c23"   # slightly lighter for chart area
GRID    = "#2e3039"
FONT    = "#e8eaf0"
LAYOUT  = dict(plot_bgcolor=PLOT_BG, paper_bgcolor=BG, font=dict(color=FONT))

# ── Load & clean ──────────────────────────────────────────────────────────────

@st.cache_data
def load_data():
    with open(DATA_FILE, encoding="utf-8") as f:
        raw = json.load(f)
    df = pd.DataFrame(raw)
    df["dealDate"] = pd.to_datetime(df["dealDate"], errors="coerce")
    df["year"] = df["dealDate"].dt.year
    RESIDENTIAL = {"דירה בבית קומות", "דירה", "דירת גן"}
    df = df[df["dealNature"].isin(RESIDENTIAL)].copy()
    df = df.dropna(subset=["dealAmount", "dealDate", "year"])
    df = df[(df["dealAmount"] >= 50_000) & (df["dealAmount"] <= 20_000_000)]
    df["year"] = df["year"].astype(int)
    # Clean room numbers — keep halves (2.5, 3.5, 4.5) as-is
    df = df.dropna(subset=["roomNum"])
    df["rooms"] = df["roomNum"].apply(lambda r: f"{r:.0f}" if r == int(r) else f"{r:.1f}")
    return df

df = load_data()

# ── Sidebar controls ──────────────────────────────────────────────────────────

st.sidebar.title("Filters")

all_rooms = sorted(df["roomNum"].unique())
room_labels = [f"{r:.0f}" if r == int(r) else f"{r:.1f}" for r in all_rooms]
room_options = dict(zip(room_labels, all_rooms))

selected_room_labels = st.sidebar.multiselect(
    "Number of rooms",
    options=list(room_options.keys()),
    default=[k for k in room_options if k in ("2", "3", "3.5", "4", "4.5", "5")],
)
selected_rooms = [room_options[l] for l in selected_room_labels]

year_min, year_max = int(df["year"].min()), int(df["year"].max())
year_range = st.sidebar.slider("Year range", year_min, year_max, (year_min, year_max))

metric = st.sidebar.radio(
    "Price metric",
    ["Sale price (₪)", "Price per m² (₪/m²)"],
    index=0,
)
price_col = "dealAmount" if metric == "Sale price (₪)" else "priceSM"
price_label = "Sale Price (₪)" if price_col == "dealAmount" else "₪ per m²"

agg_func = st.sidebar.radio("Aggregation", ["Median", "Mean"], index=0)
agg = "median" if agg_func == "Median" else "mean"

# ── Filter data ───────────────────────────────────────────────────────────────

mask = (
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1])
)
if selected_rooms:
    mask &= df["roomNum"].isin(selected_rooms)

filtered = df[mask].copy()

if price_col == "priceSM":
    filtered = filtered.dropna(subset=["priceSM"])
    filtered = filtered[filtered["priceSM"] > 1000]

# ── Header ────────────────────────────────────────────────────────────────────

st.title("🏠 Apartment Sales — Herzl St., Bat Yam")
st.caption(f"Showing {len(filtered):,} deals · {year_range[0]}–{year_range[1]}")

if filtered.empty:
    st.warning("No data for selected filters.")
    st.stop()

# ── KPI row ───────────────────────────────────────────────────────────────────

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total deals", f"{len(filtered):,}")
col2.metric(f"{agg_func} price", f"₪{filtered[price_col].agg(agg):,.0f}")
col3.metric("Cheapest deal", f"₪{filtered['dealAmount'].min():,.0f}")
col4.metric("Most expensive", f"₪{filtered['dealAmount'].max():,.0f}")

st.divider()

# ── Chart 0: Overall avg price trend + YoY % change ─────────────────────────

st.subheader(f"{agg_func} {price_label} per Year (All Selected Rooms)")

overall = (
    filtered.groupby("year")[price_col]
    .agg(agg)
    .reset_index(name="price")
    .sort_values("year")
)
overall["yoy_pct"] = overall["price"].pct_change() * 100

fig0 = make_subplots(specs=[[{"secondary_y": True}]])

fig0.add_trace(
    go.Scatter(
        x=overall["year"], y=overall["price"],
        mode="lines+markers",
        name=price_label,
        line=dict(color="#2196F3", width=3),
        marker=dict(size=7),
        hovertemplate="%{x}: ₪%{y:,.0f}<extra></extra>",
    ),
    secondary_y=False,
)

fig0.add_trace(
    go.Bar(
        x=overall["year"], y=overall["yoy_pct"],
        name="YoY change (%)",
        marker_color=[
            "#ef5350" if v < 0 else "#66bb6a"
            for v in overall["yoy_pct"].fillna(0)
        ],
        opacity=0.6,
        hovertemplate="%{x}: %{y:.1f}%<extra></extra>",
    ),
    secondary_y=True,
)

fig0.update_layout(
    height=420,
    hovermode="x unified",
    legend=dict(orientation="h", y=1.08),
    bargap=0.3,
    **LAYOUT,
)
fig0.update_yaxes(
    title_text=price_label, tickformat="₪,.0f",
    showgrid=True, gridcolor=GRID, secondary_y=False
)
fig0.update_yaxes(
    title_text="YoY Change (%)", ticksuffix="%",
    showgrid=False, secondary_y=True
)
fig0.update_xaxes(showgrid=False)
st.plotly_chart(fig0, use_container_width=True)

st.divider()

# ── Chart 1: Price trend over time by room count ──────────────────────────────

st.subheader(f"{agg_func} {price_label} Over Time by Room Count")

yearly = (
    filtered.groupby(["year", "rooms"])[price_col]
    .agg(agg)
    .reset_index(name="price")
)

fig1 = px.line(
    yearly, x="year", y="price",
    color="rooms",
    markers=True,
    labels={"price": price_label, "year": "Year", "rooms": "Rooms"},
    color_discrete_sequence=px.colors.qualitative.Set2,
)
fig1.update_traces(line_width=2.5, marker_size=6)
fig1.update_layout(
    height=420,
    hovermode="x unified",
    yaxis_tickformat="₪,.0f",
    legend_title="Rooms",
    **LAYOUT,
)
fig1.update_xaxes(showgrid=False)
fig1.update_yaxes(showgrid=True, gridcolor=GRID)
st.plotly_chart(fig1, use_container_width=True)

# ── Chart 2: Box plot — price distribution per room count ────────────────────

st.subheader(f"{price_label} Distribution by Room Count")

fig2 = px.box(
    filtered, x="rooms", y=price_col,
    color="rooms",
    points="outliers",
    labels={"rooms": "Rooms", price_col: price_label},
    color_discrete_sequence=px.colors.qualitative.Set2,
    category_orders={"rooms": sorted(filtered["rooms"].unique(),
                                     key=lambda x: float(x))},
)
fig2.update_layout(
    height=380,
    showlegend=False,
    yaxis_tickformat="₪,.0f",
    **LAYOUT,
)
fig2.update_yaxes(showgrid=True, gridcolor=GRID)
st.plotly_chart(fig2, use_container_width=True)

# ── Chart 3 & 4 side by side ─────────────────────────────────────────────────

left, right = st.columns(2)

with left:
    st.subheader("Deal Volume per Year")
    vol = filtered.groupby(["year", "rooms"]).size().reset_index(name="count")
    fig3 = px.bar(
        vol, x="year", y="count", color="rooms",
        labels={"count": "Deals", "year": "Year", "rooms": "Rooms"},
        color_discrete_sequence=px.colors.qualitative.Set2,
        category_orders={"rooms": sorted(filtered["rooms"].unique(),
                                         key=lambda x: float(x))},
    )
    fig3.update_layout(
        height=360, barmode="stack",
        legend_title="Rooms",
        **LAYOUT,
    )
    fig3.update_xaxes(showgrid=False)
    fig3.update_yaxes(showgrid=True, gridcolor=GRID)
    st.plotly_chart(fig3, use_container_width=True)

with right:
    st.subheader("Room Count Share Over Time")
    room_share = (
        filtered.groupby(["year", "rooms"])
        .size()
        .reset_index(name="count")
    )
    total_per_year = room_share.groupby("year")["count"].transform("sum")
    room_share["pct"] = room_share["count"] / total_per_year * 100

    fig4 = px.area(
        room_share, x="year", y="pct", color="rooms",
        labels={"pct": "Share (%)", "year": "Year", "rooms": "Rooms"},
        color_discrete_sequence=px.colors.qualitative.Set2,
        groupnorm="",
        category_orders={"rooms": sorted(filtered["rooms"].unique(),
                                         key=lambda x: float(x))},
    )
    fig4.update_layout(
        height=360,
        legend_title="Rooms",
        yaxis_ticksuffix="%",
        **LAYOUT,
    )
    fig4.update_xaxes(showgrid=False)
    fig4.update_yaxes(showgrid=True, gridcolor=GRID)
    st.plotly_chart(fig4, use_container_width=True)

# ── Raw data table ────────────────────────────────────────────────────────────

with st.expander("Raw data"):
    display_cols = ["dealDate", "address", "rooms", "assetArea", "floor",
                    "dealAmount", "priceSM", "yearBuilt", "dealNature"]
    show = filtered[[c for c in display_cols if c in filtered.columns]].copy()
    show = show.sort_values("dealDate", ascending=False)
    show["dealAmount"] = show["dealAmount"].apply(lambda x: f"₪{x:,.0f}")
    show["priceSM"] = show["priceSM"].apply(
        lambda x: f"₪{x:,.0f}" if pd.notna(x) else "–"
    )
    st.dataframe(show, use_container_width=True, hide_index=True)
