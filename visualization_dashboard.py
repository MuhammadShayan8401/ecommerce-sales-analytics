# streamlit_dashboard_interactive.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# -----------------------------
# Database connection
# -----------------------------
username = "root"
password = "ssuet+3452836744"  # replace with your MySQL password
host = "localhost"
database = "ecommerce_sales"

engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@{host}/{database}")

# -----------------------------
# Streamlit page configuration
# -----------------------------
st.set_page_config(page_title="E-Commerce Sales Dashboard", layout="wide")
st.title("📊 E-Commerce Sales Analytics Dashboard")

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔧 Filters")

# Load distinct values for filters
categories = pd.read_sql("SELECT DISTINCT Category FROM superstore;", engine)["Category"].tolist()
sub_categories = pd.read_sql("SELECT DISTINCT Sub_Category FROM superstore;", engine)["Sub_Category"].tolist()
regions = pd.read_sql("SELECT DISTINCT Region FROM superstore;", engine)["Region"].tolist()
years = pd.read_sql("SELECT DISTINCT YEAR(Order_Date) AS Year FROM superstore;", engine)["Year"].tolist()

selected_category = st.sidebar.multiselect("Category", categories, default=categories)
selected_sub_category = st.sidebar.multiselect("Sub-Category", sub_categories, default=sub_categories)
selected_region = st.sidebar.multiselect("Region", regions, default=regions)
selected_year = st.sidebar.multiselect("Year", years, default=years)

# -----------------------------
# Apply filters to SQL queries
# -----------------------------
filters = []

if selected_category:
    filters.append(f"Category IN ({', '.join([f'\"{c}\"' for c in selected_category])})")
if selected_sub_category:
    filters.append(f"Sub_Category IN ({', '.join([f'\"{sc}\"' for sc in selected_sub_category])})")
if selected_region:
    filters.append(f"Region IN ({', '.join([f'\"{r}\"' for r in selected_region])})")
if selected_year:
    filters.append(f"YEAR(Order_Date) IN ({', '.join([str(y) for y in selected_year])})")

where_clause = " AND ".join(filters)
if where_clause:
    where_clause = "WHERE " + where_clause

# -----------------------------
# 1️⃣ Total Sales by Category
# -----------------------------
st.header("1️⃣ Total Sales by Category")
query1 = f"""
SELECT Category, SUM(Sales) AS Total_Sales
FROM superstore
{where_clause}
GROUP BY Category;
"""
df_cat = pd.read_sql(query1, engine)

fig1, ax1 = plt.subplots(figsize=(8, 5))
sns.barplot(x="Category", y="Total_Sales", hue="Category", data=df_cat, palette="viridis", legend=False, ax=ax1)
ax1.set_title("Total Sales by Category")
st.pyplot(fig1)

# -----------------------------
# 2️⃣ Yearly Sales Trend
# -----------------------------
st.header("2️⃣ Yearly Sales Trend")
query2 = f"""
SELECT YEAR(Order_Date) AS Year, SUM(Sales) AS Total_Sales
FROM superstore
{where_clause}
GROUP BY Year
ORDER BY Year;
"""
df_year = pd.read_sql(query2, engine)

fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.lineplot(x="Year", y="Total_Sales", data=df_year, marker="o", ax=ax2)
ax2.set_title("Yearly Sales Trend")
st.pyplot(fig2)

# -----------------------------
# 3️⃣ Top 10 Sub-Categories by Profit
# -----------------------------
st.header("3️⃣ Top 10 Sub-Categories by Profit")
query3 = f"""
SELECT Sub_Category, SUM(Profit) AS Total_Profit
FROM superstore
{where_clause}
GROUP BY Sub_Category
ORDER BY Total_Profit DESC
LIMIT 10;
"""
df_sub = pd.read_sql(query3, engine)

fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(x="Total_Profit", y="Sub_Category", hue="Sub_Category", data=df_sub, palette="coolwarm", legend=False, ax=ax3)
ax3.set_title("Top 10 Sub-Categories by Profit")
st.pyplot(fig3)

# -----------------------------
# 4️⃣ Profit Heatmap: Region vs Category
# -----------------------------
st.header("4️⃣ Profit Heatmap by Region & Category")
query4 = f"""
SELECT Region, Category, SUM(Profit) AS Total_Profit
FROM superstore
{where_clause}
GROUP BY Region, Category;
"""
df_heat = pd.read_sql(query4, engine)
pivot_heat = df_heat.pivot(index="Region", columns="Category", values="Total_Profit")

fig4, ax4 = plt.subplots(figsize=(8, 6))
sns.heatmap(pivot_heat, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax4)
ax4.set_title("Profit Heatmap by Region & Category")
st.pyplot(fig4)

# -----------------------------
# 5️⃣ Discount vs Profit Scatterplot
# -----------------------------
st.header("5️⃣ Discount vs Profit")
query5 = f"SELECT Discount, Profit FROM superstore {where_clause};"
df_scatter = pd.read_sql(query5, engine)

fig5, ax5 = plt.subplots(figsize=(8, 6))
sns.scatterplot(x="Discount", y="Profit", data=df_scatter, alpha=0.5, ax=ax5)
ax5.set_title("Discount vs Profit")
st.pyplot(fig5)

# -----------------------------
# 6️⃣ Regional Sales Trend Over Time
# -----------------------------
st.header("6️⃣ Regional Sales Trend Over Time")
query6 = f"""
SELECT YEAR(Order_Date) AS Year, Region, SUM(Sales) AS Total_Sales
FROM superstore
{where_clause}
GROUP BY Year, Region
ORDER BY Year, Region;
"""
df_region = pd.read_sql(query6, engine)

fig6, ax6 = plt.subplots(figsize=(10, 6))
sns.lineplot(x="Year", y="Total_Sales", hue="Region", data=df_region, marker="o", ax=ax6)
ax6.set_title("Regional Sales Trend Over Time")
st.pyplot(fig6)

# -----------------------------
# 7️⃣ Pairplot: Sales, Profit, Discount
# -----------------------------
st.header("7️⃣ Pairplot: Sales, Profit, Discount")
query7 = f"SELECT Sales, Profit, Discount FROM superstore {where_clause};"
df_pair = pd.read_sql(query7, engine)

st.write("Pairplot showing relationships between Sales, Profit, and Discount")
sns.set(style="ticks")
pairplot_fig = sns.pairplot(df_pair, diag_kind="kde", plot_kws={"alpha": 0.5})
st.pyplot(pairplot_fig)