# Window Functions

## 🪟 Window Functions

### What are Window Functions?

**Definition:** Window functions perform calculations across a set of rows related to the current row, without grouping rows into a single output row.

**Real-life example:**
Like calculating a running total - you look at all previous rows plus current row, calculate the sum, but still show each individual row (unlike GROUP BY which collapses rows).

**Key Difference from Aggregate Functions:**
- **Aggregate Functions**: Collapse rows into groups
- **Window Functions**: Keep all rows, add calculated columns

**Syntax:**
```sql
function_name([arguments]) 
OVER (
    [PARTITION BY column1, column2, ...]
    [ORDER BY column1 [ASC|DESC], ...]
    [ROWS|RANGE BETWEEN start AND end]
)
```

---

## 📊 Types of Window Functions

### Ranking Functions

**ROW_NUMBER():**
```sql
-- Assigns sequential numbers to rows
SELECT 
    name,
    salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) AS rank
FROM employees;

-- Partitioned ranking
SELECT 
    department,
    name,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank
FROM employees;
```

**RANK():**
```sql
-- Ranks with gaps (ties get same rank, next rank skips)
SELECT 
    name,
    score,
    RANK() OVER (ORDER BY score DESC) AS rank
FROM students;
-- Scores: 100, 100, 95, 90
-- Ranks: 1, 1, 3, 4 (note the gap)

-- DENSE_RANK(): No gaps
SELECT 
    name,
    score,
    DENSE_RANK() OVER (ORDER BY score DESC) AS rank
FROM students;
-- Scores: 100, 100, 95, 90
-- Ranks: 1, 1, 2, 3 (no gap)
```

**Use Cases:**
- Top N per group
- Ranking employees by salary
- Finding duplicates
- Pagination

**Example: Top 3 Employees per Department**
```sql
WITH ranked_employees AS (
    SELECT 
        department,
        name,
        salary,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rn
    FROM employees
)
SELECT * FROM ranked_employees WHERE rn <= 3;
```

### Aggregate Window Functions

**SUM, AVG, COUNT, MIN, MAX:**
```sql
-- Running total
SELECT 
    order_date,
    total,
    SUM(total) OVER (ORDER BY order_date) AS running_total
FROM orders;

-- Partitioned running total
SELECT 
    customer_id,
    order_date,
    total,
    SUM(total) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) AS customer_running_total
FROM orders;

-- Average in partition
SELECT 
    department,
    name,
    salary,
    AVG(salary) OVER (PARTITION BY department) AS dept_avg_salary,
    salary - AVG(salary) OVER (PARTITION BY department) AS difference_from_avg
FROM employees;
```

**Use Cases:**
- Running totals
- Moving averages
- Comparing to group averages
- Cumulative calculations

### Value Functions

**LAG and LEAD:**
```sql
-- LAG: Previous row value
SELECT 
    order_date,
    total,
    LAG(total) OVER (ORDER BY order_date) AS previous_total,
    total - LAG(total) OVER (ORDER BY order_date) AS change
FROM orders;

-- LEAD: Next row value
SELECT 
    order_date,
    total,
    LEAD(total) OVER (ORDER BY order_date) AS next_total
FROM orders;

-- With offset and default
SELECT 
    order_date,
    total,
    LAG(total, 2, 0) OVER (ORDER BY order_date) AS two_periods_ago
FROM orders;
```

**FIRST_VALUE and LAST_VALUE:**
```sql
-- First value in window
SELECT 
    customer_id,
    order_date,
    total,
    FIRST_VALUE(total) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) AS first_order_total
FROM orders;

-- Last value in window
SELECT 
    customer_id,
    order_date,
    total,
    LAST_VALUE(total) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS last_order_total
FROM orders;
```

**Use Cases:**
- Period-over-period comparisons
- Finding first/last values
- Calculating changes
- Time series analysis

---

## 🎯 Window Frame Specification

### ROWS vs RANGE

**ROWS:**
```sql
-- Physical rows
SELECT 
    order_date,
    total,
    SUM(total) OVER (
        ORDER BY order_date
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS three_day_total
FROM orders;
-- Sums current row + 2 previous rows
```

**RANGE:**
```sql
-- Logical range (based on ORDER BY values)
SELECT 
    order_date,
    total,
    SUM(total) OVER (
        ORDER BY order_date
        RANGE BETWEEN INTERVAL 7 DAY PRECEDING AND CURRENT ROW
    ) AS seven_day_total
FROM orders;
-- Sums all rows within 7 days
```

**Frame Options:**
```sql
-- UNBOUNDED PRECEDING: From start
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW

-- UNBOUNDED FOLLOWING: To end
ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING

-- N PRECEDING: N rows before
ROWS BETWEEN 2 PRECEDING AND CURRENT ROW

-- N FOLLOWING: N rows after
ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING

-- Between N and M
ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING
```

---

## 📈 Advanced Window Function Examples

### Moving Averages
```sql
-- 7-day moving average
SELECT 
    date,
    sales,
    AVG(sales) OVER (
        ORDER BY date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS seven_day_avg
FROM daily_sales;

-- 30-day moving average
SELECT 
    date,
    sales,
    AVG(sales) OVER (
        ORDER BY date
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) AS thirty_day_avg
FROM daily_sales;
```

### Percentile Calculations
```sql
-- Percent rank (0 to 1)
SELECT 
    name,
    salary,
    PERCENT_RANK() OVER (ORDER BY salary) AS percentile_rank
FROM employees;

-- NTILE: Divide into buckets
SELECT 
    name,
    salary,
    NTILE(4) OVER (ORDER BY salary) AS quartile
FROM employees;
-- Divides into 4 equal groups
```

### Year-over-Year Comparison
```sql
WITH monthly_sales AS (
    SELECT 
        YEAR(order_date) AS year,
        MONTH(order_date) AS month,
        SUM(total) AS sales
    FROM orders
    GROUP BY YEAR(order_date), MONTH(order_date)
)
SELECT 
    year,
    month,
    sales,
    LAG(sales, 12) OVER (ORDER BY year, month) AS previous_year_sales,
    (sales - LAG(sales, 12) OVER (ORDER BY year, month)) / 
        LAG(sales, 12) OVER (ORDER BY year, month) * 100 AS yoy_change_pct
FROM monthly_sales;
```

### Finding Gaps and Islands
```sql
-- Find gaps in sequences
WITH numbered AS (
    SELECT 
        id,
        ROW_NUMBER() OVER (ORDER BY id) AS rn
    FROM numbers
)
SELECT 
    n1.id + 1 AS gap_start,
    n2.id - 1 AS gap_end
FROM numbered n1
INNER JOIN numbered n2 ON n1.rn = n2.rn - 1
WHERE n2.id - n1.id > 1;
```

---

## ⚡ Performance Considerations

### Indexing for Window Functions
```sql
-- Index columns in PARTITION BY
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- Index columns in ORDER BY
CREATE INDEX idx_employees_dept_salary ON employees(department, salary);
```

### Efficient Window Function Patterns

**1. Use Appropriate Frame:**
```sql
-- Specify frame explicitly for clarity and performance
SUM(total) OVER (
    PARTITION BY customer_id
    ORDER BY order_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
```

**2. Avoid Unnecessary PARTITION BY:**
```sql
-- Only partition when needed
-- More partitions = more overhead
```

**3. Combine with CTEs:**
```sql
-- Use CTEs to simplify complex window functions
WITH ranked AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rn
    FROM employees
)
SELECT * FROM ranked WHERE rn <= 3;
```

---

## 🔍 Interview Questions (4 Years Experience)

### Common Questions:

**1. What's the difference between ROW_NUMBER, RANK, and DENSE_RANK?**
- ROW_NUMBER: Sequential numbers, no ties
- RANK: Same rank for ties, gaps after ties
- DENSE_RANK: Same rank for ties, no gaps

**2. When would you use window functions vs GROUP BY?**
- Window functions: Keep all rows, add calculated columns
- GROUP BY: Collapse rows into groups
- Use window functions for running totals, rankings, comparisons

**3. What's the difference between ROWS and RANGE?**
- ROWS: Physical row count
- RANGE: Logical range based on ORDER BY values
- ROWS is usually faster

**4. How do you calculate a moving average?**
```sql
AVG(value) OVER (
    ORDER BY date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
)
```

**5. How do you find the top N per group?**
```sql
WITH ranked AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (PARTITION BY group_col ORDER BY value DESC) AS rn
    FROM table
)
SELECT * FROM ranked WHERE rn <= N;
```

**6. What's the performance impact of window functions?**
- Can be expensive for large datasets
- Index columns in PARTITION BY and ORDER BY
- Consider materialized views for frequently used calculations

