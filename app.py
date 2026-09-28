"""
app.py  –  Sales Analytics Dashboard
=====================================
Run locally:
    streamlit run app.py

Deploy: push to GitHub → connect on share.streamlit.io
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

from src.data_loader   import load_data
from src.data_cleaning import clean_data, get_data_summary
from src import analysis as an
from src import visualization as viz

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem 1.4rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .metric-card h3 { font-size: 1.6rem; margin: 0; }
    .metric-card p  { font-size: 0.85rem; margin: 0; opacity: 0.85; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background: #f0f2f6; border-radius: 8px 8px 0 0;
        padding: 6px 18px; font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# DATA LOAD (cached)
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(show_spinner="Loading data…")
def get_data():
    raw = load_data()
    return clean_data(raw)

df_full = get_data()


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR FILTERS
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/combo-chart.png", width=64)
    st.title("Sales Analytics")
    st.markdown("---")

    years = sorted(df_full["Year"].unique())
    sel_years = st.multiselect("📅 Year", years, default=years)

    regions = sorted(df_full["Region"].unique())
    sel_regions = st.multiselect("🌍 Region", regions, default=regions)

    categories = sorted(df_full["Category"].unique())
    sel_cats = st.multiselect("🗂 Category", categories, default=categories)

    segments = sorted(df_full["Segment"].unique())
    sel_segs = st.multiselect("👥 Segment", segments, default=segments)

    st.markdown("---")
    st.caption("Data: Superstore Sales Dataset")
    st.caption("Built with Streamlit + Plotly")

# Apply filters
df = df_full[
    df_full["Year"].isin(sel_years) &
    df_full["Region"].isin(sel_regions) &
    df_full["Category"].isin(sel_cats) &
    df_full["Segment"].isin(sel_segs)
].copy()

if df.empty:
    st.warning("⚠️ No data for the selected filters. Please adjust the sidebar.")
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════

tabs = st.tabs([
    "🏠 Home",
    "📈 Sales",
    "💰 Profit",
    "🌍 Regional",
    "📦 Products",
    "👥 Customers",
    "🔮 Forecast",
])


# ─────────────────────────────────────────────────────────────────────────────
# TAB 0 – HOME / KPI OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────
with tabs[0]:
    st.header("📊 Sales Analytics Dashboard")
    st.markdown("Interactive business intelligence dashboard for Superstore retail data.")

    kpis = an.get_kpis(df)

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    for col, (label, value) in zip([c1,c2,c3,c4,c5,c6], kpis.items()):
        prefix = "$" if "Sales" in label or "Profit" in label or "Value" in label else ""
        suffix = "%" if "%" in label else ""
        col.metric(label, f"{prefix}{value:,.0f}{suffix}")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(viz.sales_profit_dual(an.monthly_trend(df)), use_container_width=True)
    with col2:
        st.plotly_chart(viz.subcategory_treemap(an.sales_by_subcategory(df)), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(viz.region_pie(an.sales_by_region(df)), use_container_width=True)
    with col4:
        st.plotly_chart(viz.segment_donut(an.sales_by_segment(df)), use_container_width=True)

    with st.expander("📋 Dataset Summary"):
        summary = get_data_summary(df_full)
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Rows", f"{summary['rows']:,}")
        s2.metric("Columns", summary["columns"])
        s3.metric("Date Range", summary["date_range"])
        s4.metric("Missing Values", summary["missing_values"])


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 – SALES ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
with tabs[1]:
    st.header("📈 Sales Analysis")

    monthly = an.monthly_trend(df)
    st.plotly_chart(viz.monthly_sales_trend(monthly), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(viz.category_sales_bar(an.sales_by_category(df)), use_container_width=True)
    with col2:
        yearly = an.yearly_trend(df)
        fig = viz.monthly_sales_trend(monthly)   # re-use monthly
        st.plotly_chart(
            __import__("plotly.express", fromlist=["bar"]).bar(
                yearly, x="Year", y="Sales", title="Yearly Sales",
                color_discrete_sequence=["#4F8EF7"], text_auto=".2s"
            ), use_container_width=True
        )

    st.plotly_chart(viz.subcategory_treemap(an.sales_by_subcategory(df)), use_container_width=True)

    with st.expander("📄 Monthly Data Table"):
        st.dataframe(monthly.style.format({"Sales": "${:,.0f}", "Profit": "${:,.0f}"}),
                     use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 – PROFIT ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
with tabs[2]:
    st.header("💰 Profit Analysis")

    monthly = an.monthly_trend(df)
    st.plotly_chart(viz.monthly_profit_trend(monthly), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(viz.category_profit_bar(an.sales_by_category(df)), use_container_width=True)
    with col2:
        st.plotly_chart(viz.discount_profit_bar(an.discount_impact(df)), use_container_width=True)

    st.subheader("🔻 Least Profitable Products")
    bp = an.bottom_products(df, 10)
    st.dataframe(bp.style.format({"Sales": "${:,.0f}", "Profit": "${:,.0f}"}),
                 use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 – REGIONAL ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
with tabs[3]:
    st.header("🌍 Regional Analysis")

    reg = an.sales_by_region(df)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(viz.region_sales_bar(reg), use_container_width=True)
    with col2:
        st.plotly_chart(viz.region_profit_bar(reg), use_container_width=True)

    st.plotly_chart(viz.region_pie(reg), use_container_width=True)

    st.subheader("📊 State-level Sales (Top 15)")
    state_df = an.sales_by_state(df).head(15)
    import plotly.express as px
    fig = px.bar(state_df.sort_values("Sales"), x="Sales", y="State",
                 orientation="h", color="Sales",
                 color_continuous_scale="Blues", text_auto=".2s",
                 title="Top 15 States by Sales")
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📄 Region Data Table"):
        st.dataframe(reg.style.format({"Sales": "${:,.0f}", "Profit": "${:,.0f}"}),
                     use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 – PRODUCT ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
with tabs[4]:
    st.header("📦 Product Analysis")

    n_products = st.slider("Number of top products to show", 5, 20, 10)
    tp = an.top_products(df, n_products)

    st.plotly_chart(viz.top_products_bar(tp), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(viz.product_profit_scatter(tp), use_container_width=True)
    with col2:
        st.plotly_chart(viz.discount_profit_bar(an.discount_impact(df)), use_container_width=True)

    with st.expander("📄 Top Products Table"):
        st.dataframe(
            tp.style.format({"Sales": "${:,.0f}", "Profit": "${:,.0f}"}),
            use_container_width=True
        )


# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 – CUSTOMER ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
with tabs[5]:
    st.header("👥 Customer Analysis")

    n_cust = st.slider("Number of top customers to show", 5, 20, 10)
    tc = an.top_customers(df, n_cust)

    st.plotly_chart(viz.top_customers_bar(tc), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        seg = an.customer_segment_analysis(df)
        st.plotly_chart(viz.customer_segment_bar(seg), use_container_width=True)
    with col2:
        st.plotly_chart(viz.segment_donut(an.sales_by_segment(df)), use_container_width=True)

    with st.expander("📄 Top Customers Table"):
        st.dataframe(
            tc.style.format({"Sales": "${:,.0f}", "Profit": "${:,.0f}"}),
            use_container_width=True
        )


# ─────────────────────────────────────────────────────────────────────────────
# TAB 6 – SALES FORECAST
# ─────────────────────────────────────────────────────────────────────────────
with tabs[6]:
    st.header("🔮 Sales Forecasting – Linear Regression")
    st.markdown("Trains a simple Linear Regression on monthly sales to project future performance.")

    months_ahead = st.slider("Months to forecast ahead", 3, 24, 6)

    monthly_data = an.prepare_forecast_data(df)

    X = monthly_data[["Month_Index"]].values
    y = monthly_data["Sales"].values

    # Train / test split (80 / 20)
    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mae   = mean_absolute_error(y_test, y_pred)
    r2    = r2_score(y_test, y_pred)
    rmse  = np.sqrt(np.mean((y_test - y_pred) ** 2))

    m1, m2, m3 = st.columns(3)
    m1.metric("MAE",  f"${mae:,.0f}")
    m2.metric("RMSE", f"${rmse:,.0f}")
    m3.metric("R² Score", f"{r2:.3f}")

    # Future predictions
    last_idx = monthly_data["Month_Index"].max()
    future_indices = np.arange(last_idx + 1, last_idx + 1 + months_ahead).reshape(-1, 1)
    future_sales   = model.predict(future_indices)

    # Build future date labels
    last_period = pd.Period(monthly_data["YearMonth"].iloc[-1], freq="M")
    future_periods = [str(last_period + i + 1) for i in range(months_ahead)]

    future_df = pd.DataFrame({
        "YearMonth": future_periods,
        "Predicted_Sales": np.maximum(future_sales, 0),
    })

    st.plotly_chart(viz.forecast_chart(monthly_data, future_df), use_container_width=True)

    with st.expander("📄 Forecast Values"):
        st.dataframe(
            future_df.style.format({"Predicted_Sales": "${:,.0f}"}),
            use_container_width=True
        )

    st.info("💡 **Note:** Linear Regression captures the overall trend. For production, consider ARIMA, Prophet, or LSTM models.")
