# Aggregate Functions & Grouping

## 📊 Aggregate Functions

### What are Aggregate Functions?

**Definition:** Aggregate functions perform calculations on a set of rows and return a single value.

**Real-life example:**
Like calculating class average - you take all student scores, add them up, divide by count, and get one average score.

**Common Aggregate Functions:**
- COUNT: Count rows
- SUM: Sum of values
- AVG: Average of values
- MIN: Minimum value
- MAX: Maximum value

---

## 🔢 Basic Aggregate Functions

### COUNT

**Definition:** COUNT returns the number of rows.

**Syntax:**
```sql
-- Count all rows
SELECT COUNT(*) FROM students;

-- Count non-NULL values in column
SELECT COUNT(email) FROM students;  -- Excludes NULL emails

-- Count distinct values
SELECT COUNT(DISTINCT department) FROM employees;

-- Count with conditions
SELECT COUNT(*) FROM orders WHERE total > 100;
```

**Use Cases:**
- Total number of records
- Count of non-NULL values
- Count of unique values
- Conditional counting

**Examples:**
```sql
-- Count orders per customer
SELECT 
    customer_id,
    COUNT(*) AS order_count
FROM orders
GROUP BY customer_id;

-- Count with multiple conditions
SELECT 
    COUNT(*) AS total_orders,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) AS completed_orders,
    COUNT(CASE WHEN status = 'pending' THEN 1 END) AS pending_orders
FROM orders;
```

### SUM

**Definition:** SUM returns the sum of numeric values.

**Syntax:**
```sql
-- Sum all values
SELECT SUM(total) FROM orders;

-- Sum with conditions
SELECT SUM(total) FROM orders WHERE status = 'completed';

-- Sum with GROUP BY
SELECT 
    customer_id,
    SUM(total) AS total_spent
FROM orders
GROUP BY customer_id;
```

**Use Cases:**
- Total sales
- Total quantities
- Financial calculations
- Summing grouped data

**Examples:**
```sql
-- Total revenue by product
SELECT 
    p.name,
    SUM(oi.quantity * oi.price) AS total_revenue
FROM products p
INNER JOIN order_items oi ON p.id = oi.product_id
GROUP BY p.id, p.name;

-- Sum with NULL handling
SELECT 
    SUM(COALESCE(amount, 0)) AS total_amount
FROM transactions;
```

### AVG

**Definition:** AVG returns the average of numeric values.

**Syntax:**
```sql
-- Average of all values
SELECT AVG(price) FROM products;

-- Average excluding NULLs
SELECT AVG(salary) FROM employees WHERE department = 'Sales';

-- Average with GROUP BY
SELECT 
    department,
    AVG(salary) AS avg_salary
FROM employees
GROUP BY department;
```

**Use Cases:**
- Average prices
- Average salaries
- Performance metrics
- Statistical analysis

**Examples:**
```sql
-- Average order value by customer
SELECT 
    c.name,
    AVG(o.total) AS avg_order_value
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name;

-- Average with precision
SELECT 
    ROUND(AVG(price), 2) AS avg_price
FROM products;
```

### MIN and MAX

**Definition:** MIN returns the minimum value, MAX returns the maximum value.

**Syntax:**
```sql
-- Minimum value
SELECT MIN(price) FROM products;

-- Maximum value
SELECT MAX(price) FROM products;

-- Both together
SELECT 
    MIN(price) AS lowest_price,
    MAX(price) AS highest_price,
    AVG(price) AS avg_price
FROM products;

-- With GROUP BY
SELECT 
    category,
    MIN(price) AS min_price,
    MAX(price) AS max_price
FROM products
GROUP BY category;
```

**Use Cases:**
- Finding extremes
- Range calculations
- Price analysis
- Date ranges

**Examples:**
```sql
-- Price range by category
SELECT 
    category,
    MIN(price) AS cheapest,
    MAX(price) AS most_expensive,
    MAX(price) - MIN(price) AS price_range
FROM products
GROUP BY category;

-- Latest and earliest orders
SELECT 
    customer_id,
    MIN(order_date) AS first_order,
    MAX(order_date) AS last_order
FROM orders
GROUP BY customer_id;
```

---

## 📦 GROUP BY

### What is GROUP BY?

**Definition:** GROUP BY groups rows that have the same values in specified columns.

**Real-life example:**
Like organizing students by class - you group all students in Class A together, Class B together, etc., then calculate statistics for each group.

**Syntax:**
```sql
-- Basic GROUP BY
SELECT 
    department,
    COUNT(*) AS employee_count,
    AVG(salary) AS avg_salary
FROM employees
GROUP BY department;

-- Multiple columns
SELECT 
    department,
    position,
    COUNT(*) AS count,
    AVG(salary) AS avg_salary
FROM employees
GROUP BY department, position;

-- With WHERE (filters before grouping)
SELECT 
    department,
    AVG(salary) AS avg_salary
FROM employees
WHERE hire_date > '2020-01-01'
GROUP BY department;
```

**Rules:**
- All non-aggregated columns must be in GROUP BY
- Can group by multiple columns
- WHERE filters before grouping
- HAVING filters after grouping

**Examples:**
```sql
-- Sales by month
SELECT 
    YEAR(order_date) AS year,
    MONTH(order_date) AS month,
    SUM(total) AS monthly_sales,
    COUNT(*) AS order_count
FROM orders
GROUP BY YEAR(order_date), MONTH(order_date)
ORDER BY year, month;

-- Top customers by revenue
SELECT 
    c.name,
    COUNT(o.id) AS order_count,
    SUM(o.total) AS total_revenue
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name
ORDER BY total_revenue DESC
LIMIT 10;
```

---

## 🔍 HAVING Clause

### What is HAVING?

**Definition:** HAVING filters groups after GROUP BY (similar to WHERE but for groups).

**Real-life example:**
Like filtering classes - WHERE filters students before grouping, HAVING filters classes after grouping (e.g., "show only classes with average score > 80").

**Syntax:**
```sql
-- HAVING filters groups
SELECT 
    department,
    AVG(salary) AS avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 50000;

-- HAVING with multiple conditions
SELECT 
    customer_id,
    COUNT(*) AS order_count,
    SUM(total) AS total_spent
FROM orders
GROUP BY customer_id
HAVING COUNT(*) >= 5 AND SUM(total) > 1000;
```

**WHERE vs HAVING:**
```sql
-- WHERE: Filters rows before grouping
SELECT 
    department,
    AVG(salary) AS avg_salary
FROM employees
WHERE salary > 30000  -- Filters individual employees
GROUP BY department;

-- HAVING: Filters groups after grouping
SELECT 
    department,
    AVG(salary) AS avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 50000;  -- Filters departments
```

**Use Cases:**
- Filter groups by aggregate values
- Find groups meeting criteria
- Top N per group scenarios

**Examples:**
```sql
-- Departments with more than 10 employees
SELECT 
    department,
    COUNT(*) AS employee_count
FROM employees
GROUP BY department
HAVING COUNT(*) > 10;

-- Products with average rating above 4.0
SELECT 
    product_id,
    AVG(rating) AS avg_rating,
    COUNT(*) AS review_count
FROM reviews
GROUP BY product_id
HAVING AVG(rating) >= 4.0 AND COUNT(*) >= 10;
```

---

## 🎯 Advanced Aggregation

### Conditional Aggregation

**Definition:** Using CASE statements within aggregate functions.

**Syntax:**
```sql
-- Count with conditions
SELECT 
    COUNT(*) AS total,
    COUNT(CASE WHEN status = 'active' THEN 1 END) AS active_count,
    COUNT(CASE WHEN status = 'inactive' THEN 1 END) AS inactive_count
FROM users;

-- Sum with conditions
SELECT 
    SUM(CASE WHEN status = 'completed' THEN total ELSE 0 END) AS completed_revenue,
    SUM(CASE WHEN status = 'pending' THEN total ELSE 0 END) AS pending_revenue
FROM orders;

-- Multiple conditions
SELECT 
    category,
    SUM(CASE WHEN price < 50 THEN 1 ELSE 0 END) AS budget_count,
    SUM(CASE WHEN price BETWEEN 50 AND 200 THEN 1 ELSE 0 END) AS mid_range_count,
    SUM(CASE WHEN price > 200 THEN 1 ELSE 0 END) AS premium_count
FROM products
GROUP BY category;
```

**Use Cases:**
- Pivot-like operations
- Multiple metrics in one query
- Conditional counting/summing
- Complex reporting

### Aggregate with DISTINCT

**Definition:** Using DISTINCT within aggregate functions.

**Syntax:**
```sql
-- Count distinct values
SELECT COUNT(DISTINCT customer_id) FROM orders;

-- Average of distinct values
SELECT AVG(DISTINCT price) FROM products;

-- Sum distinct (less common)
SELECT SUM(DISTINCT amount) FROM transactions;
```

**Use Cases:**
- Unique customer counts
- Average of unique values
- Removing duplicates in aggregation

### Nested Aggregates

**Definition:** Using aggregate functions with GROUP BY results.

**Syntax:**
```sql
-- Average of group averages
SELECT 
    AVG(avg_salary) AS overall_avg
FROM (
    SELECT 
        department,
        AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department
) AS dept_avgs;

-- Maximum group count
SELECT 
    MAX(order_count) AS max_orders
FROM (
    SELECT 
        customer_id,
        COUNT(*) AS order_count
    FROM orders
    GROUP BY customer_id
) AS customer_orders;
```

---

## ⚡ Performance & Efficiency

### Indexing for Aggregation

**Index columns used in:**
- GROUP BY clauses
- WHERE clauses (filter before grouping)
- JOIN conditions

```sql
-- Create indexes for efficient grouping
CREATE INDEX idx_employees_department ON employees(department);
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
```

### Efficient Aggregation Patterns

**1. Filter Early (WHERE before GROUP BY):**
```sql
-- Efficient: Filter before grouping
SELECT 
    department,
    AVG(salary)
FROM employees
WHERE hire_date > '2020-01-01'  -- Filter first
GROUP BY department;

-- Less efficient: Filter after grouping
SELECT 
    department,
    AVG(salary)
FROM employees
GROUP BY department
HAVING AVG(salary) > 50000;  -- Calculate for all, then filter
```

**2. Use Appropriate Aggregates:**
```sql
-- Use COUNT(*) for counting rows (faster)
SELECT COUNT(*) FROM orders;

-- Use COUNT(column) only when you need to exclude NULLs
SELECT COUNT(email) FROM users;  -- Excludes NULL emails
```

**3. Limit Grouping Columns:**
```sql
-- Group by necessary columns only
-- More columns = more groups = slower
SELECT 
    department,  -- Only group by what you need
    AVG(salary)
FROM employees
GROUP BY department;
```

---

## 🔍 Interview Questions (4 Years Experience)

### Common Questions:

**1. What's the difference between WHERE and HAVING?**
- WHERE: Filters rows before grouping
- HAVING: Filters groups after grouping
- WHERE can't use aggregate functions
- HAVING can use aggregate functions

**2. Can you use aggregate functions in WHERE clause?**
- No, use HAVING instead
- WHERE filters individual rows
- HAVING filters groups

**3. What happens if you SELECT a column not in GROUP BY?**
- Error in most databases (MySQL 5.7+ strict mode)
- Must include all non-aggregated columns in GROUP BY
- Or use aggregate function on that column

**4. How do you find the top N in each group?**
```sql
-- Using window functions (modern approach)
SELECT * FROM (
    SELECT 
        *,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rn
    FROM employees
) ranked
WHERE rn <= 3;

-- Using correlated subquery (older approach)
SELECT e1.* FROM employees e1
WHERE (
    SELECT COUNT(*) FROM employees e2
    WHERE e2.department = e1.department AND e2.salary > e1.salary
) < 3;
```

**5. How do you calculate running totals?**
```sql
-- Using window functions
SELECT 
    order_date,
    total,
    SUM(total) OVER (ORDER BY order_date) AS running_total
FROM orders;
```

**6. What's the difference between COUNT(*) and COUNT(column)?**
- COUNT(*): Counts all rows including NULLs
- COUNT(column): Counts non-NULL values in column
- COUNT(*) is usually faster

