import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Retail Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("retail_sales_cleaned.csv")
    df["OrderDate"] = pd.to_datetime(df["OrderDate"])
    return df

df = load_data()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.title("📊 Dashboard Filters")

date_range = st.sidebar.date_input(
    "Date Range",
    [df["OrderDate"].min(), df["OrderDate"].max()]
)

select_all_regions = st.sidebar.checkbox("Select All Regions", value=True)
if select_all_regions:
    regions = list(df["Region"].unique())
else:
    regions = st.sidebar.multiselect(
        "Region",
        df["Region"].unique(),
        default=list(df["Region"].unique())
    )

select_all_categories = st.sidebar.checkbox("Select All Categories", value=True)
if select_all_categories:
    categories = list(df["Category"].unique())
else:
    categories = st.sidebar.multiselect(
        "Category",
        df["Category"].unique(),
        default=list(df["Category"].unique())
    )

select_all_segments = st.sidebar.checkbox("Select All Segments", value=True)
if select_all_segments:
    segments = list(df["Segment"].unique())
else:
    segments = st.sidebar.multiselect(
        "Segment",
        df["Segment"].unique(),
        default=list(df["Segment"].unique())
    )

# -----------------------------
# FILTER DATA
# -----------------------------
filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories)) &
    (df["Segment"].isin(segments)) &
    (
        df["OrderDate"].between(
            pd.to_datetime(date_range[0]),
            pd.to_datetime(date_range[1])
        )
    )
]

# -----------------------------
# TITLE
# -----------------------------
st.title("📈 Retail Sales Analytics Dashboard")
st.caption("Executive dashboard with real-time sales performance metrics")

# -----------------------------
# KPI CARDS
# -----------------------------
revenue = filtered_df["Sales"].sum()
profit = filtered_df["Profit"].sum()
orders = filtered_df["OrderID"].nunique()
aov = revenue / orders if orders > 0 else 0

filtered_df["YearMonth"] = (
    filtered_df["OrderDate"]
    .dt.to_period("M")
    .astype(str)
)

monthly_revenue = (
    filtered_df
    .groupby("YearMonth")["Sales"]
    .sum()
    .reset_index()
    .sort_values("YearMonth")
)
monthly_profit = (
    filtered_df
    .groupby("YearMonth")["Profit"]
    .sum()
    .reset_index()
    .sort_values("YearMonth")
)
monthly_orders = (
    filtered_df
    .groupby("YearMonth")["OrderID"]
    .nunique()
    .reset_index()
    .sort_values("YearMonth")
)
monthly_aov = (
    filtered_df
    .groupby("YearMonth")
    .apply(lambda x: x["Sales"].sum() / x["OrderID"].nunique() if x["OrderID"].nunique() > 0 else 0)
    .reset_index(name="AOV")
    .sort_values("YearMonth")
)


def render_sparkline(values, stroke_color, chart_id):
    values = list(values)
    if len(values) < 2:
        values = values + [values[0]] * (2 - len(values))
    width = 120
    height = 50
    min_val = min(values)
    max_val = max(values)
    span = max_val - min_val if max_val != min_val else 1
    points = []
    for index, val in enumerate(values):
        x = index * (width / (len(values) - 1))
        y = height - ((val - min_val) / span) * (height * 0.6) - 8
        points.append(f"{x:.1f},{y:.1f}")
    path = "M " + " L ".join(points)
    fill_path = f"{path} L {width},{height} L 0,{height} Z"
    return f'''
        <svg viewBox="0 0 {width} {height}" preserveAspectRatio="none">
            <defs>
                <linearGradient id="spark-{chart_id}" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="{stroke_color}" stop-opacity="0.95" />
                    <stop offset="100%" stop-color="{stroke_color}" stop-opacity="0.25" />
                </linearGradient>
            </defs>
            <path d="{fill_path}" fill="url(#spark-{chart_id})" opacity="0.18" />
            <path d="{path}" fill="none" stroke="{stroke_color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
    '''

sparkline_revenue = render_sparkline(monthly_revenue["Sales"].tail(10), "#CBD5E1", "revenue")
sparkline_profit = render_sparkline(monthly_profit["Profit"].tail(10), "#34D399", "profit")
sparkline_orders = render_sparkline(monthly_orders["OrderID"].tail(10), "#38BDF8", "orders")
sparkline_aov = render_sparkline(monthly_aov["AOV"].tail(10), "#FBBF24", "aov")

card_html = f"""
<style>
.kpi-grid {{
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 18px;
    margin-bottom: 28px;
}}
@media (max-width: 1040px) {{
    .kpi-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
}}
@media (max-width: 680px) {{
    .kpi-grid {{ grid-template-columns: 1fr; }}
}}
.kpi-card {{
    position: relative;
    min-height: 180px;
    border-radius: 20px;
    padding: 24px;
    overflow: hidden;
    background: rgba(15, 23, 42, 0.82);
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 20px 50px rgba(15, 23, 42, 0.18);
    backdrop-filter: blur(18px);
    transition: transform 0.28s ease, box-shadow 0.28s ease, filter 0.28s ease;
}}
.kpi-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 28px 70px rgba(15, 23, 42, 0.26);
}}
.kpi-card::before {{
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 20px;
    opacity: 0.16;
    pointer-events: none;
}}
.kpi-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    margin-bottom: 16px;
    position: relative;
    z-index: 1;
}}
.kpi-badge {{
    width: 46px;
    height: 46px;
    min-width: 46px;
    border-radius: 16px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: white;
    box-shadow: 0 16px 30px rgba(15, 23, 42, 0.26);
}}
.kpi-label {{
    font-size: 14px;
    font-weight: 500;
    color: rgba(241, 245, 249, 0.92);
    margin-bottom: 6px;
}}
.kpi-value {{
    display: block;
    font-size: 42px;
    font-weight: 700;
    line-height: 1;
    color: white;
    margin-bottom: 8px;
}}
.kpi-subtitle {{
    display: block;
    font-size: 13px;
    color: rgba(241, 245, 249, 0.72);
}}
.kpi-sparkline {{
    position: absolute;
    left: 24px;
    right: 24px;
    bottom: 18px;
    height: 56px;
    z-index: 1;
}}
.kpi-sparkline svg {{
    width: 100%;
    height: 100%;
}}
.card-revenue::before {{
    background: radial-gradient(circle at top left, rgba(79, 70, 229, 0.32), transparent 36%);
}}
.card-profit::before {{
    background: radial-gradient(circle at top left, rgba(16, 185, 129, 0.32), transparent 36%);
}}
.card-orders::before {{
    background: radial-gradient(circle at top left, rgba(14, 165, 233, 0.32), transparent 36%);
}}
.card-aov::before {{
    background: radial-gradient(circle at top left, rgba(245, 158, 11, 0.32), transparent 36%);
}}
.card-revenue .kpi-badge {{
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
}}
.card-profit .kpi-badge {{
    background: linear-gradient(135deg, #10B981 0%, #059669 100%);
}}
.card-orders .kpi-badge {{
    background: linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%);
}}
.card-aov .kpi-badge {{
    background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
}}
.icon {{ width: 22px; height: 22px; display: block; }}
</style>
<div class="kpi-grid">
    <div class="kpi-card card-revenue">
        <div class="kpi-header">
            <div>
                <span class="kpi-label">Revenue</span>
                <span class="kpi-value">${revenue:,.0f}</span>
                <span class="kpi-subtitle">Total Revenue</span>
            </div>
            <span class="kpi-badge">
                <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 8c1.657 0 3 1.343 3 3s-1.343 3-3 3-3 1.343-3 3" />
                    <path d="M9 4h6l1 2v2a7 7 0 0 1 0 14h-8a6 6 0 0 1 0-12v-2l1-2z" />
                </svg>
            </span>
        </div>
        <div class="kpi-sparkline">{sparkline_revenue}</div>
    </div>
    <div class="kpi-card card-profit">
        <div class="kpi-header">
            <div>
                <span class="kpi-label">Profit</span>
                <span class="kpi-value">${profit:,.0f}</span>
                <span class="kpi-subtitle">Total Profit</span>
            </div>
            <span class="kpi-badge">
                <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M5 12l5 5L21 6" />
                    <path d="M19 12h-6" />
                </svg>
            </span>
        </div>
        <div class="kpi-sparkline">{sparkline_profit}</div>
    </div>
    <div class="kpi-card card-orders">
        <div class="kpi-header">
            <div>
                <span class="kpi-label">Orders</span>
                <span class="kpi-value">{orders:,}</span>
                <span class="kpi-subtitle">Total Orders</span>
            </div>
            <span class="kpi-badge">
                <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M6 7h12l-1.5 9h-9L6 7z" />
                    <path d="M9 7V4a3 3 0 0 1 6 0v3" />
                    <path d="M10 16h.01M14 16h.01" />
                </svg>
            </span>
        </div>
        <div class="kpi-sparkline">{sparkline_orders}</div>
    </div>
    <div class="kpi-card card-aov">
        <div class="kpi-header">
            <div>
                <span class="kpi-label">AOV</span>
                <span class="kpi-value">${aov:,.2f}</span>
                <span class="kpi-subtitle">Average Order Value</span>
            </div>
            <span class="kpi-badge">
                <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M6 6h15l-1.5 9h-13.5L3 6z" />
                    <path d="M7 6V4a3 3 0 0 1 6 0v2" />
                    <path d="M9 16h.01M15 16h.01" />
                </svg>
            </span>
        </div>
        <div class="kpi-sparkline">{sparkline_aov}</div>
    </div>
</div>
"""

st.markdown(card_html, unsafe_allow_html=True)
st.markdown("---")

# -----------------------------
# MONTHLY SALES TREND
# -----------------------------
filtered_df["YearMonth"] = (
    filtered_df["OrderDate"]
    .dt.to_period("M")
    .astype(str)
)

monthly_sales = (
    filtered_df
    .groupby("YearMonth")["Sales"]
    .sum()
    .reset_index()
)

fig_monthly = px.line(
    monthly_sales,
    x="YearMonth",
    y="Sales",
    title="Monthly Sales Trend",
    markers=True,
    color_discrete_sequence=["#6366F1"]
)

fig_monthly.update_traces(
    line=dict(width=3, shape="spline", smoothing=1.2, color="#6366F1"),
    marker=dict(size=6, color="#A5B4FC", line=dict(width=0)),
    hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.0f}<extra></extra>"
)
fig_monthly.update_layout(
    height=420,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False, showline=False, tickfont=dict(color="#334155")),
    yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.15)", zeroline=False, tickfont=dict(color="#334155")),
    margin=dict(l=10, r=10, t=50, b=30),
    font=dict(color="#0F172A"),
    hoverlabel=dict(bgcolor="rgba(255,255,255,0.95)", font_color="#0F172A")
)

st.plotly_chart(fig_monthly, use_container_width=True)

# -----------------------------
# CATEGORY & REGION
# -----------------------------
col1, col2 = st.columns(2)

category_sales = (
    filtered_df
    .groupby("Category")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Sales", ascending=False)
)

fig_category = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    title="Sales by Category",
    text="Sales",
    color_discrete_sequence=["#3B82F6"]
)

fig_category.update_traces(
    marker=dict(
        color="#3B82F6",
        line=dict(width=0, color="rgba(0,0,0,0)"),
        opacity=0.95,
        cornerradius=12
    ),
    texttemplate="$%{y:,.0f}",
    textposition="outside"
)
fig_category.update_layout(
    height=420,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False, showline=False, tickfont=dict(color="#334155")),
    yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.15)", zeroline=False, tickfont=dict(color="#334155")),
    margin=dict(l=10, r=10, t=50, b=30),
    font=dict(color="#0F172A")
)

region_sales = (
    filtered_df
    .groupby("Region")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Sales", ascending=False)
)

fig_region = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    title="Sales by Region",
    text="Sales",
    color_discrete_sequence=["#8B5CF6"]
)

fig_region.update_traces(
    marker=dict(
        color="#8B5CF6",
        line=dict(width=0, color="rgba(0,0,0,0)"),
        opacity=0.95,
        cornerradius=12
    ),
    texttemplate="$%{y:,.0f}",
    textposition="outside"
)
fig_region.update_layout(
    height=420,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False, showline=False, tickfont=dict(color="#334155")),
    yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.15)", zeroline=False, tickfont=dict(color="#334155")),
    margin=dict(l=10, r=10, t=50, b=30),
    font=dict(color="#0F172A")
)

with col1:
    st.plotly_chart(fig_category, use_container_width=True)

with col2:
    st.plotly_chart(fig_region, use_container_width=True)

# -----------------------------
# TOP 10 CUSTOMERS
# -----------------------------
top_customers = (
    filtered_df
    .groupby("CustomerName")["Sales"]
    .sum()
    .nlargest(10)
    .reset_index()
)

fig_customers = px.bar(
    top_customers,
    x="Sales",
    y="CustomerName",
    orientation="h",
    title="Top 10 Customers",
    text="Sales",
    color_discrete_sequence=["#4F46E5"]
)

fig_customers.update_traces(
    marker=dict(
        color="#4F46E5",
        line=dict(width=0, color="rgba(0,0,0,0)"),
        opacity=0.95,
        cornerradius=12
    ),
    texttemplate="$%{x:,.0f}",
    textposition="outside"
)
fig_customers.update_layout(
    height=420,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.15)", zeroline=False, tickfont=dict(color="#334155")),
    yaxis=dict(showgrid=False, showline=False, tickfont=dict(color="#334155")),
    margin=dict(l=10, r=10, t=50, b=30),
    font=dict(color="#0F172A")
)

st.plotly_chart(fig_customers, use_container_width=True)

# -----------------------------
# DATA TABLE
# -----------------------------
st.subheader("📋 Filtered Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# -----------------------------
# DOWNLOAD CSV
# -----------------------------
csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)