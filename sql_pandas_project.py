import pandas as pd
import mysql.connector

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your password",
    database="RetailShopDB"
)

# SQL query (STRING me honi chahiye)
query = """
SELECT 
    s.sale_date,
    p.category,
    p.product_name,
    s.quantity,
    p.selling_price,
    c.city
FROM Sales s
JOIN Products p ON s.product_id = p.product_id
JOIN Customers c ON s.customer_id = c.customer_id
"""

# Load SQL data into Pandas
df = pd.read_sql(query, conn)

buying_price_dict = {
    "Ceiling Fan": 1200,
    "Mixer Grinder": 1850,
    "Gas Stove": 1375,
    "Water Geyser": 2800,
    "Steel Cooker": 1000
}
# add buying price using map()
df["buying_price"] = df["product_name"].map(buying_price_dict)
print(df)

#Total Cost
df["Total Cost"] = df["quantity"] * df["buying_price"]
print(df)

# total sales
df["Total Sales"] = df["quantity"] * df["selling_price"]
print(df)

#Profit
df["Profit"] = df["Total Sales"] - df["Total Cost"] 

#print(df.head())
# date_ time
df["sale_date"] = pd.to_datetime(df["sale_date"])

# column extra spaces, title (clean data)
df["category"] = df["category"].str.strip()
df["category"] = df["category"].str.title()
df["product_name"] = df["product_name"].str.strip()
df["product_name"] = df["product_name"].str.title()
print(df.head())
df.info()

total_revenue = df["Total Sales"].sum()
total_profit = df["Profit"].sum()
total_quantity = df["quantity"].sum()

print("Total Revenue:", total_revenue)
print("Total Profit:", total_profit)
print("Total Quantity Sold:", total_quantity)

category_analysis = df.groupby("category").agg(
    Total_Sales = ("Total Sales", "sum"),
    Total_Profit = ("Profit", "sum"),
    Total_Quantity = ("quantity", "sum")
).reset_index()
print(category_analysis)

product_analysis = df.groupby("product_name").agg(
    Total_Sales=("Total Sales", "sum"),
    Profit=("Profit", "sum"),
    quantity = ("quantity", "sum")
).reset_index().sort_values("Total_Sales", ascending=False)
print(product_analysis)

city_analysis = df.groupby("city")["Total Sales"].sum().reset_index()
print(city_analysis)


df["Month"] = df["sale_date"].dt.month
df["Year"] = df["sale_date"].dt.year
monthly_sales = df.groupby("Month")["Total Sales"].sum().reset_index()
print(monthly_sales)

#city-wise total sales
import matplotlib.pyplot as plt
plt.figure()
plt.bar(city_analysis["city"], city_analysis["Total Sales"])
plt.xlabel("City")
plt.ylabel("Total Sales")
plt.title("City-wise Total Sales")
plt.show()

#Category-wise profit
plt.figure()
plt.bar(category_analysis["category"], category_analysis["Total_Profit"])
plt.xlabel("Category")
plt.ylabel("Total Profit")
plt.title("Category-wise Profit")
plt.show()

# category wise profit percentage using pie chart
plt.figure()
plt.pie(
    category_analysis["Total_Profit"],
    labels=category_analysis["category"],
    autopct="%1.1f%%"
)
plt.title("Category-wise Profit percentage")
plt.show()

#Sales vs Profit per category 
category_analysis.set_index("category")[["Total_Sales", "Total_Profit"]].plot(kind="bar",figsize=(8,5))
plt.xlabel("Category")
plt.ylabel("Amount")
plt.title("Sales vs Profit per Category")
plt.show()

print(df.shape)
print(category_analysis.shape)
print(product_analysis.shape)
print(city_analysis.shape)
print(df.describe())
print(df.head())