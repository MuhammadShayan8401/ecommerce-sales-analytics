import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os

# -----------------------------
# Database connection (SQLAlchemy)
# -----------------------------
username = "root"
password = "ssuet+3452836744"   # replace with your MySQL password
host = "localhost"
database = "ecommerce_sales"

engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@{host}/{database}")

# -----------------------------
# Create visuals folder if not exists
# -----------------------------
os.makedirs("visuals", exist_ok=True)

# -----------------------------
# 1. Sales by Category
# -----------------------------
query1 = "SELECT Category, SUM(Sales) AS Total_Sales FROM superstore GROUP BY Category;"
df_cat = pd.read_sql(query1, engine)

plt.figure(figsize=(8, 5))
sns.barplot(x="Category", y="Total_Sales", hue="Category", data=df_cat, palette="viridis", legend=False)
plt.title("Total Sales by Category")
plt.savefig("visuals/sales_by_category.png", dpi=300, bbox_inches="tight")
plt.close()

# -----------------------------
# 2. Yearly Sales Trend
# -----------------------------
query2 = """
SELECT YEAR(Order_Date) AS Year, SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY Year
ORDER BY Year;
"""
df_year = pd.read_sql(query2, engine)

plt.figure(figsize=(8, 5))
sns.lineplot(x="Year", y="Total_Sales", data=df_year, marker="o")
plt.title("Yearly Sales Trend")
plt.savefig("visuals/yearly_sales_trend.png", dpi=300, bbox_inches="tight")
plt.close()

# -----------------------------
# 3. Profit by Sub-Category (Top 10)
# -----------------------------
query3 = """
SELECT Sub_Category, SUM(Profit) AS Total_Profit
FROM superstore
GROUP BY Sub_Category
ORDER BY Total_Profit DESC
LIMIT 10;
"""
df_sub = pd.read_sql(query3, engine)

plt.figure(figsize=(10, 6))
sns.barplot(x="Total_Profit", y="Sub_Category", hue="Sub_Category", data=df_sub, palette="coolwarm", legend=False)
plt.title("Top 10 Sub-Categories by Profit")
plt.savefig("visuals/top10_subcategories_profit.png", dpi=300, bbox_inches="tight")
plt.close()

# -----------------------------
# 4. Heatmap: Profit by Region & Category
# -----------------------------
query4 = """
SELECT Region, Category, SUM(Profit) AS Total_Profit
FROM superstore
GROUP BY Region, Category;
"""
df_heat = pd.read_sql(query4, engine)
pivot_heat = df_heat.pivot(index="Region", columns="Category", values="Total_Profit")

plt.figure(figsize=(8, 6))
sns.heatmap(pivot_heat, annot=True, fmt=".0f", cmap="YlGnBu")
plt.title("Profit Heatmap by Region & Category")
plt.savefig("visuals/heatmap_region_category.png", dpi=300, bbox_inches="tight")
plt.close()

# -----------------------------
# 5. Scatterplot: Discount vs Profit
# -----------------------------
query5 = "SELECT Discount, Profit FROM superstore;"
df_scatter = pd.read_sql(query5, engine)

plt.figure(figsize=(8, 6))
sns.scatterplot(x="Discount", y="Profit", data=df_scatter, alpha=0.5)
plt.title("Discount vs Profit")
plt.savefig("visuals/discount_vs_profit.png", dpi=300, bbox_inches="tight")
plt.close()

# -----------------------------
# 6. Regional Sales Trend (Advanced)
# -----------------------------
query6 = """
SELECT YEAR(Order_Date) AS Year, Region, SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY Year, Region
ORDER BY Year, Region;
"""
df_region = pd.read_sql(query6, engine)

plt.figure(figsize=(10, 6))
sns.lineplot(x="Year", y="Total_Sales", hue="Region", data=df_region, marker="o")
plt.title("Regional Sales Trend Over Time")
plt.savefig("visuals/regional_sales_trend.png", dpi=300, bbox_inches="tight")
plt.close()

# -----------------------------
# 7. Pairplot: Sales, Profit, Discount (Advanced)
# -----------------------------
query7 = "SELECT Sales, Profit, Discount FROM superstore;"
df_pair = pd.read_sql(query7, engine)

sns.pairplot(df_pair, diag_kind="kde", plot_kws={"alpha": 0.5})
plt.suptitle("Pairplot of Sales, Profit, and Discount", y=1.02)
plt.savefig("visuals/pairplot_sales_profit_discount.png", dpi=300, bbox_inches="tight")
plt.close()

print("✅ All visualizations (basic + advanced) saved in 'visuals/' folder as PNGs.")
