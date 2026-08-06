-- ============================================================
-- SQL Assignment Project: E-Commerce Management System
-- Database Engine: MySQL / PostgreSQL compatible
-- File Name: ecommerce.sql
-- ============================================================

-- ============================================================
-- PART 1: DATABASE & TABLE CREATION
-- ============================================================

CREATE DATABASE IF NOT EXISTS ecommerce_db;
USE ecommerce_db;

-- 1. Create Customers Table
CREATE TABLE Customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    city VARCHAR(50)
);

-- 2. Create Categories Table
CREATE TABLE Categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL
);

-- 3. Create Products Table
CREATE TABLE Products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
        ON DELETE SET NULL 
        ON UPDATE CASCADE
);

-- 4. Create Orders Table
CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

-- ============================================================
-- PART 2: INSERT SAMPLE DATA
-- ============================================================

-- Insert 5 Categories
INSERT INTO Categories (category_id, category_name) VALUES
(1, 'Electronics'),
(2, 'Fashion'),
(3, 'Grocery'),
(4, 'Home Appliances'),
(5, 'Books');

-- Insert 5 Customers
INSERT INTO Customers (customer_id, name, email, phone, city) VALUES
(1, 'Anik Rahman', 'anik@example.com', '01711000001', 'Dhaka'),
(2, 'Ayesha Siddiqua', 'ayesha@example.com', '01811000002', 'Chittagong'),
(3, 'Babul Hossain', 'babul@example.com', '01911000003', 'Dhaka'),
(4, 'Farhana Ahmed', 'farhana@example.com', '01511000004', 'Sylhet'),
(5, 'Tanvir Chowdhury', 'tanvir@example.com', '01611000005', 'Rajshahi');

-- Insert 10 Products
INSERT INTO Products (product_id, product_name, price, stock, category_id) VALUES
(101, 'Smartphone X', 25000.00, 15, 1),
(102, 'Laptop Pro', 85000.00, 8, 1),
(103, 'Bluetooth Headphone', 1500.00, 25, 1),
(104, 'Men Denim Jacket', 2800.00, 50, 2),
(105, 'Women Silk Dress', 3500.00, 4, 2),
(106, 'Organic Soyabean Oil 5L', 850.00, 100, 3),
(107, 'Basmati Rice 5kg', 650.00, 6, 3),
(108, 'Smart LED TV 43"', 38000.00, 12, 4),
(109, 'SQL Database Design Book', 450.00, 30, 5),
(110, 'Feature Phone', 1200.00, 3, 1);

-- Insert 8 Orders
INSERT INTO Orders (order_id, customer_id, order_date, total_amount) VALUES
(1001, 1, '2026-03-01', 85000.00),
(1002, 2, '2026-03-02', 2800.00),
(1003, 1, '2026-03-05', 1500.00),
(1004, 3, '2026-03-10', 38000.00),
(1005, 4, '2026-03-12', 650.00),
(1006, 2, '2026-03-15', 3500.00),
(1007, 5, '2026-03-18', 25000.00),
(1008, 3, '2026-03-20', 850.00);

-- ============================================================
-- PART 3: UPDATE OPERATIONS
-- ============================================================

-- Update Laptop price
UPDATE Products
SET price = 82000.00
WHERE product_name = 'Laptop Pro';

-- Update Customer city
UPDATE Customers
SET city = 'Dhaka'
WHERE customer_id = 2;

-- Update Product stock after selling
UPDATE Products
SET stock = stock - 2
WHERE product_id = 101;

-- ============================================================
-- PART 4: DELETE OPERATIONS
-- ============================================================

-- Delete One product
DELETE FROM Products
WHERE product_id = 110;

-- Delete One customer (will cascade delete or disassociate based on FK setup)
DELETE FROM Customers
WHERE customer_id = 5;

-- ============================================================
-- PART 5: BASIC QUERIES
-- ============================================================

-- 1. Show all customers
SELECT * FROM Customers;

-- 2. Show all products
SELECT * FROM Products;

-- 3. Show products whose price is greater than 1000
SELECT * FROM Products
WHERE price > 1000;

-- 4. Show products whose stock is less than 10
SELECT * FROM Products
WHERE stock < 10;

-- 5. Show customers from Dhaka
SELECT * FROM Customers
WHERE city = 'Dhaka';

-- 6. Sort products by price (Highest to Lowest)
SELECT * FROM Products
ORDER BY price DESC;

-- 7. Sort customers alphabetically
SELECT * FROM Customers
ORDER BY name ASC;

-- 8. Show the first 5 products
SELECT * FROM Products
LIMIT 5;

-- 9. Count total customers
SELECT COUNT(*) AS total_customers 
FROM Customers;

-- 10. Calculate the average product price
SELECT AVG(price) AS average_price 
FROM Products;

-- ============================================================
-- PART 6: AGGREGATE FUNCTIONS
-- ============================================================

SELECT 
    MAX(price) AS max_product_price,
    MIN(price) AS min_product_price,
    SUM(stock) AS total_stock,
    AVG(stock) AS average_stock
FROM Products;

SELECT COUNT(*) AS total_orders 
FROM Orders;

-- ============================================================
-- PART 7: JOIN QUERIES
-- ============================================================

-- 1. Show customer name and their orders
SELECT 
    c.name AS customer_name, 
    o.order_id, 
    o.order_date, 
    o.total_amount
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id;

-- 2. Show product name with category name
SELECT 
    p.product_name, 
    cat.category_name
FROM Products p
LEFT JOIN Categories cat ON p.category_id = cat.category_id;

-- 3. Show order details with customer name
SELECT 
    o.order_id, 
    c.name AS customer_name, 
    c.email, 
    o.order_date, 
    o.total_amount
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id;

-- ============================================================
-- PART 8: SEARCH QUERIES
-- ============================================================

-- Find products containing the word "Phone"
SELECT * FROM Products
WHERE product_name LIKE '%Phone%';

-- Find customers whose name starts with "A"
SELECT * FROM Customers
WHERE name LIKE 'A%';

-- Find products priced between 500 and 3000
SELECT * FROM Products
WHERE price BETWEEN 500 AND 3000;

-- ============================================================
-- PART 9: BONUS CHALLENGE
-- ============================================================

-- 1. Which product has the highest price?
SELECT product_id, product_name, price 
FROM Products
WHERE price = (SELECT MAX(price) FROM Products);

-- 2. Which customer placed the largest order?
SELECT 
    c.customer_id, 
    c.name, 
    o.order_id, 
    o.total_amount
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
WHERE o.total_amount = (SELECT MAX(total_amount) FROM Orders);

-- 3. How many products belong to each category?
SELECT 
    c.category_name, 
    COUNT(p.product_id) AS total_products
FROM Categories c
LEFT JOIN Products p ON c.category_id = p.category_id
GROUP BY c.category_id, c.category_name;

-- 4. Which category has the most products?
SELECT 
    c.category_name, 
    COUNT(p.product_id) AS product_count
FROM Categories c
JOIN Products p ON c.category_id = p.category_id
GROUP BY c.category_id, c.category_name
ORDER BY product_count DESC
LIMIT 1;

-- 5. List all customers who have placed at least one order
SELECT DISTINCT 
    c.customer_id, 
    c.name, 
    c.email
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id;