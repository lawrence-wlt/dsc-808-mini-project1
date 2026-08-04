import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Interactive Sales Dashboard", layout="wide")

st.title("📊 Interactive Sales Dashboard")
st.caption("Loaded from sample_data.csv")


# ---------- Load data ----------
@st.cache_data
def load_data():
    return pd.read_csv("sample_data.csv")

df = load_data()

# ---------- Sidebar filters  ----------
st.sidebar.header("Filters")

if "product" in df.columns:
    products = sorted(df["product"].dropna().unique().tolist())
    selected_products = st.sidebar.multiselect("Product", products, default=products)
    df = df[df["product"].isin(selected_products)]

if "region" in df.columns:
    regions = sorted(df["region"].dropna().unique().tolist())
    selected_regions = st.sidebar.multiselect("Region", regions, default=regions)
    df = df[df["region"].isin(selected_regions)]

if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"])
    min_date, max_date = df["date"].min(), df["date"].max()
    date_range = st.sidebar.date_input("Date range", (min_date, max_date))
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start, end = date_range
        df = df[(df["date"] >= pd.Timestamp(start)) & (df["date"] <= pd.Timestamp(end))]

# ---------- KPI cards ----------
col1, col2, col3 = st.columns(3)
col1.metric("Total orders", f"{len(df):,}")
if "revenue" in df.columns:
    col2.metric("Total revenue", f"KES {df['revenue'].sum():,.0f}")
if "units_sold" in df.columns:
    col3.metric("Units sold", f"{df['units_sold'].sum():,}")

st.divider()

# ---------- Charts ----------
left, right = st.columns(2)

with left:
    if "date" in df.columns and "revenue" in df.columns:
        st.subheader("Revenue over time")
        trend = df.groupby(df["date"].dt.date)["revenue"].sum().reset_index()
        fig = px.line(trend, x="date", y="revenue")
        st.plotly_chart(fig, use_container_width=True)

with right:
    if "product" in df.columns and "revenue" in df.columns:
        st.subheader("Revenue by product")
        product_summary = df.groupby("product")["revenue"].sum().reset_index()
        fig2 = px.bar(product_summary, x="product", y="revenue")
        st.plotly_chart(fig2, use_container_width=True)

st.subheader("Raw data")
st.dataframe(df, use_container_width=True)
