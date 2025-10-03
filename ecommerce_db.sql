CREATE DATABASE ecommerce_sales;
USE ecommerce_sales;

CREATE TABLE superstore (
    Row_ID INT,
    Order_ID VARCHAR(20),
    Order_Date DATE,
    Ship_Date DATE,
    Ship_Mode VARCHAR(50),
    Customer_ID VARCHAR(20),
    Customer_Name VARCHAR(100),
    Segment VARCHAR(50),
    Country VARCHAR(50),
    City VARCHAR(100),
    State VARCHAR(100),
    Postal_Code VARCHAR(20),
    Region VARCHAR(50),
    Product_ID VARCHAR(50),
    Category VARCHAR(50),
    Sub_Category VARCHAR(50),
    Product_Name VARCHAR(255),
    Sales DECIMAL(10,2),
    Quantity INT,
    Discount DECIMAL(5,2),
    Profit DECIMAL(10,2)
);

-- 1. Preview first 10 rows
SELECT * FROM superstore LIMIT 10;

-- 2. Count total number of rows
SELECT COUNT(*) AS total_rows FROM superstore;

-- 3. Total sales and profit
SELECT SUM(Sales) AS total_sales, SUM(Profit) AS total_profit FROM superstore;

-- 4. Sales by category
SELECT Category, SUM(Sales) AS total_sales
FROM superstore
GROUP BY Category
ORDER BY total_sales DESC;

-- 5. Profit by sub-category
SELECT Sub_Category, SUM(Profit) AS total_profit
FROM superstore
GROUP BY Sub_Category
ORDER BY total_profit DESC;

-- 6. Top 5 most profitable products
SELECT Product_Name, SUM(Profit) AS total_profit
FROM superstore
GROUP BY Product_Name
ORDER BY total_profit DESC
LIMIT 5;

-- 7. Sales trend by year
SELECT YEAR(Order_Date) AS year, SUM(Sales) AS total_sales
FROM superstore
GROUP BY YEAR(Order_Date)
ORDER BY year;
