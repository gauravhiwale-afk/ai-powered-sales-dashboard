# ==========================================================
# 📦 IMPORTS
# ==========================================================
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os
import google.generativeai as genai
from dotenv import load_dotenv


# ==========================================================
# 🔐 ENVIRONMENT & GEMINI SETUP
# ==========================================================
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.0-flash")


# ==========================================================
# 🔢 NUMBER FORMATTER (K / M)
# ==========================================================
def format_number(value):
    if value >= 1_000_000:
        return f"${value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"${value/1_000:.2f}K"
    else:
        return f"${value:.2f}"


# ==========================================================
# 🤖 AI EXECUTIVE SUMMARY FUNCTION
# ==========================================================
@st.cache_data(show_spinner=False)
def generate_ai_summary(kpis_dict):

    prompt = f"""
    You are a senior business analyst.

    Based on the following KPI data:

    Total Revenue: {kpis_dict['revenue']}
    Total Profit: {kpis_dict['profit']}
    Profit Margin: {kpis_dict['margin']}%
    Total Orders: {kpis_dict['orders']}
    Top Region: {kpis_dict['top_region']}
    Top Sub-Category: {kpis_dict['top_subcategory']}

    Write a concise executive summary (3-4 bullet points).

    Include:
    - Biggest strength
    - Biggest risk or concern
    - One recommended action

    Use clear business language.
    Do NOT repeat raw numbers excessively.
    """

    response = model.generate_content(prompt)
    return response.text


# ==========================================================
# 🏷 PAGE TITLE
# ==========================================================
st.title("📊 AI-Powered Sales Dashboard")
st.markdown("Real-time KPI analysis with AI-generated executive insights.")


# ==========================================================
# 🗄 DATABASE CONNECTION
# ==========================================================
conn = sqlite3.connect("sales.db")


# ==========================================================
# 🎛 SIDEBAR FILTERS
# ==========================================================
st.sidebar.header("Filters")

regions = pd.read_sql_query(
    "SELECT DISTINCT region FROM orders", conn
)["region"].tolist()
regions.insert(0, "All")

categories = pd.read_sql_query(
    "SELECT DISTINCT category FROM orders", conn
)["category"].tolist()
categories.insert(0, "All")

selected_region = st.sidebar.selectbox("Select Region", regions)
selected_category = st.sidebar.selectbox("Select Category", categories)


# ==========================================================
# 🔎 DYNAMIC WHERE CLAUSE
# ==========================================================
conditions = []

if selected_region != "All":
    conditions.append(f"region = '{selected_region}'")

if selected_category != "All":
    conditions.append(f"category = '{selected_category}'")

where_clause = (
    "WHERE " + " AND ".join(conditions)
    if conditions else ""
)


# ==========================================================
# 📊 KPI CALCULATION
# ==========================================================
kpi_query = f"""
SELECT 
    SUM(sales) as total_revenue,
    SUM(profit) as total_profit,
    COUNT(*) as total_orders
FROM orders
{where_clause}
"""

kpi_df = pd.read_sql_query(kpi_query, conn)

total_revenue = kpi_df["total_revenue"][0] or 0
total_profit = kpi_df["total_profit"][0] or 0
total_orders = kpi_df["total_orders"][0] or 0

profit_margin = (
    (total_profit / total_revenue) * 100
    if total_revenue else 0
)

# Top Region
top_region_df = pd.read_sql_query(f"""
SELECT region, SUM(sales) as revenue
FROM orders
{where_clause}
GROUP BY region
ORDER BY revenue DESC
LIMIT 1
""", conn)

top_region = (
    top_region_df["region"][0]
    if not top_region_df.empty else "N/A"
)

# Top Sub-Category
top_category_df = pd.read_sql_query(f"""
SELECT "sub-category", SUM(sales) as revenue
FROM orders
{where_clause}
GROUP BY "sub-category"
ORDER BY revenue DESC
LIMIT 1
""", conn)

top_subcategory = (
    top_category_df["sub-category"][0]
    if not top_category_df.empty else "N/A"
)


# ==========================================================
# 📈 KPI DISPLAY (BOXED)
# ==========================================================
with st.container(border=True):

    row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)

    row1_col1.metric("Total Revenue", format_number(total_revenue))
    row1_col2.metric("Total Profit", format_number(total_profit))
    row1_col3.metric("Profit Margin", f"{profit_margin:.2f}%")
    row1_col4.metric("Total Orders", f"{total_orders:,}")

    row2_col1, row2_col2 = st.columns(2)
    row2_col1.metric("Top Region", top_region)
    row2_col2.metric("Top Sub-Category", top_subcategory)

st.divider()


# ==========================================================
# 📦 PREPARE DATA FOR AI
# ==========================================================
kpi_data = {
    "revenue": format_number(total_revenue),
    "profit": format_number(total_profit),
    "margin": round(profit_margin, 2),
    "orders": f"{total_orders:,}",
    "top_region": top_region,
    "top_subcategory": top_subcategory
}


# ==========================================================
# 🤖 AI EXECUTIVE SUMMARY
# ==========================================================
st.subheader("🤖 AI Executive Summary")

if st.button("Generate AI Insights"):
    with st.spinner("Generating insights..."):
        try:
            summary = generate_ai_summary(kpi_data)
            st.info(summary)
        except Exception:
            st.warning("AI summary temporarily unavailable. Please try again.")

st.divider()

# ==========================================================
# 📊 REVENUE BY REGION
# ==========================================================
region_df = pd.read_sql_query(f"""
SELECT region, SUM(sales) as revenue
FROM orders
{where_clause}
GROUP BY region
ORDER BY revenue DESC
""", conn)

st.subheader("Revenue by Region")

fig_region = px.bar(
    region_df,
    x="region",
    y="revenue",
    color="revenue",
    color_continuous_scale="Blues"
)

st.plotly_chart(fig_region, width="stretch")


# ==========================================================
# 🏆 TOP 10 SUB-CATEGORIES
# ==========================================================
product_df = pd.read_sql_query(f"""
SELECT "sub-category", SUM(sales) as revenue
FROM orders
{where_clause}
GROUP BY "sub-category"
ORDER BY revenue DESC
LIMIT 10
""", conn)

st.subheader("Top 10 Sub-Categories by Revenue")

fig_products = px.bar(
    product_df,
    x="revenue",
    y="sub-category",
    orientation="h",
    color="revenue",
    color_continuous_scale="Greens"
)

st.plotly_chart(fig_products, width="stretch")


# ==========================================================
# 🌎 TOP 10 STATES
# ==========================================================
state_df = pd.read_sql_query(f"""
SELECT state, SUM(sales) as revenue
FROM orders
{where_clause}
GROUP BY state
ORDER BY revenue DESC
LIMIT 10
""", conn)

st.subheader("Top 10 States by Revenue")

fig_states = px.bar(
    state_df,
    x="revenue",
    y="state",
    orientation="h",
    color="revenue",
    color_continuous_scale="Oranges"
)

st.plotly_chart(fig_states, width="stretch")


# ==========================================================
# 🗺 US CHOROPLETH MAP
# ==========================================================
us_state_abbrev = {
    "Alabama": "AL","Arizona": "AZ","Arkansas": "AR","California": "CA",
    "Colorado": "CO","Connecticut": "CT","Delaware": "DE",
    "District of Columbia": "DC","Florida": "FL","Georgia": "GA",
    "Idaho": "ID","Illinois": "IL","Indiana": "IN","Iowa": "IA",
    "Kansas": "KS","Kentucky": "KY","Louisiana": "LA",
    "Maine": "ME","Maryland": "MD","Massachusetts": "MA",
    "Michigan": "MI","Minnesota": "MN","Mississippi": "MS",
    "Missouri": "MO","Montana": "MT","Nebraska": "NE",
    "Nevada": "NV","New Hampshire": "NH","New Jersey": "NJ",
    "New Mexico": "NM","New York": "NY","North Carolina": "NC",
    "North Dakota": "ND","Ohio": "OH","Oklahoma": "OK",
    "Oregon": "OR","Pennsylvania": "PA","Rhode Island": "RI",
    "South Carolina": "SC","South Dakota": "SD","Tennessee": "TN",
    "Texas": "TX","Utah": "UT","Vermont": "VT",
    "Virginia": "VA","Washington": "WA","West Virginia": "WV",
    "Wisconsin": "WI","Wyoming": "WY"
}

map_df = pd.read_sql_query(f"""
SELECT state, SUM(sales) as revenue
FROM orders
{where_clause}
GROUP BY state
""", conn)

map_df["state_code"] = map_df["state"].map(us_state_abbrev)

st.subheader("Revenue by State (US Map)")

fig_map = px.choropleth(
    map_df,
    locations="state_code",
    locationmode="USA-states",
    color="revenue",
    scope="usa",
    color_continuous_scale="Blues"
)

st.plotly_chart(fig_map, width="stretch")


# ==========================================================
# 📌 FOOTER
# ==========================================================
st.caption("Data Source: Superstore Dataset | Built with SQL, Python, Streamlit & Gemini AI")

conn.close()