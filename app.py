import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)


# ============================================================
# CREATE SAMPLE DATA
# ============================================================

@st.cache_data
def create_data():

    np.random.seed(42)

    n = 1000

    states = [
        "Rajasthan",
        "Delhi",
        "Maharashtra",
        "Gujarat",
        "Karnataka",
        "Tamil Nadu",
        "Uttar Pradesh",
        "West Bengal",
        "Telangana",
        "Madhya Pradesh"
    ]

    categories = [
        "Electronics",
        "Furniture",
        "Clothing",
        "Beauty",
        "Books"
    ]

    segments = [
        "Consumer",
        "Corporate",
        "Home Office"
    ]

    products = [
        "Laptop",
        "Smartphone",
        "Headphones",
        "Office Chair",
        "Desk",
        "Sofa",
        "T-Shirt",
        "Jeans",
        "Shoes",
        "Skincare Kit",
        "Perfume",
        "Novel",
        "Notebook",
        "Tablet",
        "Smartwatch"
    ]

    dates = pd.date_range(
        start="2025-01-01",
        end="2025-12-31",
        periods=n
    )

    df = pd.DataFrame({
        "Order_ID": [f"ORD{10001 + i}" for i in range(n)],
        "Customer_ID": [
            f"CUST{1001 + np.random.randint(0, 350)}"
            for _ in range(n)
        ],
        "Order_Date": dates,
        "State": np.random.choice(states, n),
        "Category": np.random.choice(categories, n),
        "Customer_Segment": np.random.choice(segments, n),
        "Product": np.random.choice(products, n),
        "Quantity": np.random.randint(1, 6, n)
    })

    prices = {
        "Laptop": 65000,
        "Smartphone": 35000,
        "Headphones": 5000,
        "Office Chair": 12000,
        "Desk": 15000,
        "Sofa": 40000,
        "T-Shirt": 1200,
        "Jeans": 2500,
        "Shoes": 3500,
        "Skincare Kit": 2500,
        "Perfume": 4000,
        "Novel": 700,
        "Notebook": 300,
        "Tablet": 22000,
        "Smartwatch": 8000
    }

    df["Unit_Price"] = df["Product"].map(prices)

    df["Sales"] = (
        df["Quantity"] *
        df["Unit_Price"]
    )

    df["Profit"] = (
        df["Sales"] *
        np.random.uniform(0.08, 0.30, n)
    ).round(2)

    return df


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    data_folder = Path("data")
    data_folder.mkdir(exist_ok=True)

    file_path = data_folder / "ecommerce_sales.csv"

    if file_path.exists():

        df = pd.read_csv(file_path)

        df["Order_Date"] = pd.to_datetime(
            df["Order_Date"]
        )

        return df

    else:

        df = create_data()

        df.to_csv(
            file_path,
            index=False
        )

        return df


df = load_data()


# ============================================================
# DASHBOARD HEADER
# ============================================================

st.title(
    "🛒 E-Commerce Sales & Customer Analytics Dashboard"
)

st.caption(
    "Interactive business dashboard built with "
    "Python • Pandas • Plotly • Streamlit"
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Dashboard Filters")


min_date = df["Order_Date"].min().date()
max_date = df["Order_Date"].max().date()


date_range = st.sidebar.date_input(
    "Order Date",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


states = st.sidebar.multiselect(
    "State",
    options=sorted(df["State"].unique()),
    default=sorted(df["State"].unique())
)


categories = st.sidebar.multiselect(
    "Category",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)


segments = st.sidebar.multiselect(
    "Customer Segment",
    options=sorted(df["Customer_Segment"].unique()),
    default=sorted(df["Customer_Segment"].unique())
)


# ============================================================
# DATE HANDLING
# ============================================================

if isinstance(date_range, tuple) and len(date_range) == 2:

    start_date = date_range[0]
    end_date = date_range[1]

else:

    start_date = date_range
    end_date = date_range


# ============================================================
# FILTER DATA
# ============================================================

filtered = df[
    (df["Order_Date"].dt.date >= start_date)
    &
    (df["Order_Date"].dt.date <= end_date)
    &
    (df["State"].isin(states))
    &
    (df["Category"].isin(categories))
    &
    (df["Customer_Segment"].isin(segments))
].copy()


# ============================================================
# EMPTY DATA CHECK
# ============================================================

if filtered.empty:

    st.warning(
        "⚠️ No data matches the selected filters."
    )

    st.stop()


# ============================================================
# KPI CALCULATIONS
# ============================================================

revenue = filtered["Sales"].sum()

profit = filtered["Profit"].sum()

orders = filtered["Order_ID"].nunique()

customers = filtered["Customer_ID"].nunique()

units_sold = filtered["Quantity"].sum()

unique_products = filtered["Product"].nunique()

average_order_value = (
    revenue / orders
    if orders > 0
    else 0
)

profit_margin = (
    (profit / revenue) * 100
    if revenue > 0
    else 0
)


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "💰 Revenue",
        f"₹{revenue / 100000:.2f} L"
    )


with col2:

    st.metric(
        "📦 Orders",
        f"{orders:,}"
    )


with col3:

    st.metric(
        "👥 Customers",
        f"{customers:,}"
    )


with col4:

    st.metric(
        "📈 Profit",
        f"₹{profit / 100000:.2f} L"
    )


with col5:

    st.metric(
        "📊 Profit Margin",
        f"{profit_margin:.1f}%"
    )


st.divider()


# ============================================================
# MONTHLY REVENUE & PROFIT
# ============================================================

monthly = (
    filtered
    .assign(
        Month=filtered["Order_Date"]
        .dt
        .to_period("M")
        .astype(str)
    )
    .groupby("Month", as_index=False)[
        ["Sales", "Profit"]
    ]
    .sum()
)


fig_trend = px.line(
    monthly,
    x="Month",
    y=["Sales", "Profit"],
    markers=True,
    title="📈 Monthly Revenue & Profit"
)


fig_trend.update_layout(
    xaxis_title="Month",
    yaxis_title="Amount (₹)",
    legend_title="Metric"
)


st.plotly_chart(
    fig_trend,
    use_container_width=True
)


# ============================================================
# SALES BY CATEGORY
# ============================================================

category_sales = (
    filtered
    .groupby("Category", as_index=False)["Sales"]
    .sum()
    .sort_values(
        "Sales",
        ascending=False
    )
)


fig_category = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    title="🛍️ Sales by Category",
    text_auto=".2s"
)


fig_category.update_layout(
    xaxis_title="Category",
    yaxis_title="Sales (₹)"
)


st.plotly_chart(
    fig_category,
    use_container_width=True
)


# ============================================================
# TOP STATES
# ============================================================

state_sales = (
    filtered
    .groupby(
        "State",
        as_index=False
    )[["Sales", "Profit"]]
    .sum()
    .sort_values(
        "Sales",
        ascending=False
    )
)


fig_state = px.bar(
    state_sales.head(10),
    x="Sales",
    y="State",
    orientation="h",
    title="🇮🇳 Top States by Revenue",
    text_auto=".2s"
)


fig_state.update_layout(
    xaxis_title="Revenue (₹)",
    yaxis_title="State"
)


st.plotly_chart(
    fig_state,
    use_container_width=True
)


# ============================================================
# TOP PRODUCTS
# ============================================================

product_sales = (
    filtered
    .groupby(
        "Product",
        as_index=False
    )[["Sales", "Profit", "Quantity"]]
    .sum()
    .sort_values(
        "Sales",
        ascending=False
    )
)


fig_product = px.bar(
    product_sales.head(10),
    x="Sales",
    y="Product",
    orientation="h",
    title="🏆 Top 10 Products by Revenue",
    text_auto=".2s"
)


fig_product.update_layout(
    xaxis_title="Revenue (₹)",
    yaxis_title="Product"
)


st.plotly_chart(
    fig_product,
    use_container_width=True
)


# ============================================================
# CUSTOMER & ORDER ANALYSIS
# ============================================================

st.subheader(
    "👥 Customer & Order Analysis"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Average Order Value",
        f"₹{average_order_value:,.0f}"
    )


with col2:

    st.metric(
        "Units Sold",
        f"{units_sold:,}"
    )


with col3:

    st.metric(
        "Unique Products",
        f"{unique_products:,}"
    )


# ============================================================
# CUSTOMER SEGMENTS
# ============================================================

segment_sales = (
    filtered
    .groupby(
        "Customer_Segment",
        as_index=False
    )["Sales"]
    .sum()
    .sort_values(
        "Sales",
        ascending=False
    )
)


fig_segment = px.pie(
    segment_sales,
    names="Customer_Segment",
    values="Sales",
    title="👥 Revenue by Customer Segment"
)


st.plotly_chart(
    fig_segment,
    use_container_width=True
)


# ============================================================
# TOP PRODUCTS TABLE
# ============================================================

st.subheader(
    "🏆 Top Products"
)


top_products = (
    filtered
    .groupby("Product", as_index=False)
    .agg(
        Revenue=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Units=("Quantity", "sum")
    )
    .sort_values(
        "Revenue",
        ascending=False
    )
    .head(10)
)


st.dataframe(
    top_products,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.subheader(
    "💡 Business Insights"
)


best_category = category_sales.iloc[0]["Category"]

best_state = state_sales.iloc[0]["State"]

best_product = product_sales.iloc[0]["Product"]


col1, col2, col3 = st.columns(3)


with col1:

    st.info(
        f"**Top Category**\n\n"
        f"{best_category}"
    )


with col2:

    st.info(
        f"**Top State**\n\n"
        f"{best_state}"
    )


with col3:

    st.info(
        f"**Top Product**\n\n"
        f"{best_product}"
    )


# ============================================================
# RAW DATA
# ============================================================

with st.expander(
    "🔍 View Filtered Raw Data"
):

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "E-Commerce Analytics Dashboard | "
    "Built with Python • Pandas • Plotly • Streamlit"
)