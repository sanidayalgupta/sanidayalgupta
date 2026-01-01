# Joins & Subqueries

## 🔗 Joins

### What are Joins?

**Definition:** JOINs combine rows from two or more tables based on related columns.

**Real-life example:**
Like merging two spreadsheets - you match rows based on a common column (like customer ID) to combine related information.

**Why Use Joins?**
- Normalized data (avoid duplication)
- Combine related data from multiple tables
- Efficient data retrieval
- Maintain data integrity

---

## 📊 Types of Joins

### INNER JOIN

**Definition:** INNER JOIN returns only rows that have matching values in both tables.

**Syntax:**
```sql
-- Basic INNER JOIN
SELECT 
    orders.id,
    orders.total,
    customers.name AS customer_name
FROM orders
INNER JOIN customers ON orders.customer_id = customers.id;

-- Using WHERE (old syntax, still works)
SELECT 
    orders.id,
    orders.total,
    customers.name
FROM orders, customers
WHERE orders.customer_id = customers.id;

-- Multiple INNER JOINs
SELECT 
    o.id AS order_id,
    o.total,
    c.name AS customer_name,
    p.name AS product_name,
    oi.quantity
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id;
```

**Use Cases:**
- Get related data from multiple tables
- Filter based on related table data
- Most common join type

**Example:**
```sql
-- Find all orders with customer information
SELECT 
    o.id,
    o.order_date,
    o.total,
    c.name,
    c.email
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
WHERE o.total > 100;
```

### LEFT JOIN (LEFT OUTER JOIN)

**Definition:** LEFT JOIN returns all rows from the left table and matching rows from the right table. If no match, NULL values are returned.

**Syntax:**
```sql
-- LEFT JOIN
SELECT 
    customers.id,
    customers.name,
    orders.id AS order_id,
    orders.total
FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id;

-- Find customers with no orders
SELECT 
    customers.id,
    customers.name
FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id
WHERE orders.id IS NULL;
```

**Use Cases:**
- Include all records from left table
- Find records without matches
- Optional relationships

**Example:**
```sql
-- Get all products and their order counts (including products never ordered)
SELECT 
    p.id,
    p.name,
    COUNT(o.id) AS order_count
FROM products p
LEFT JOIN order_items oi ON p.id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.id
GROUP BY p.id, p.name;
```

### RIGHT JOIN (RIGHT OUTER JOIN)

**Definition:** RIGHT JOIN returns all rows from the right table and matching rows from the left table.

**Syntax:**
```sql
-- RIGHT JOIN (less common, usually use LEFT JOIN instead)
SELECT 
    orders.id,
    orders.total,
    customers.name
FROM orders
RIGHT JOIN customers ON orders.customer_id = customers.id;

-- Equivalent to LEFT JOIN (swapped tables)
SELECT 
    orders.id,
    orders.total,
    customers.name
FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id;
```

**Best Practice:** Use LEFT JOIN instead of RIGHT JOIN for better readability.

### FULL OUTER JOIN

**Definition:** FULL OUTER JOIN returns all rows from both tables, with NULLs where no match exists.

**Syntax:**
```sql
-- FULL OUTER JOIN (MySQL doesn't support, use UNION)
SELECT 
    customers.id,
    customers.name,
    orders.id AS order_id
FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id
UNION
SELECT 
    customers.id,
    customers.name,
    orders.id
FROM customers
RIGHT JOIN orders ON customers.id = orders.customer_id;
```

**Use Cases:**
- Need all records from both tables
- Find unmatched records in both directions
- Data comparison

### CROSS JOIN

**Definition:** CROSS JOIN returns the Cartesian product (all combinations) of rows from both tables.

**Syntax:**
```sql
-- CROSS JOIN
SELECT 
    sizes.size,
    colors.color
FROM sizes
CROSS JOIN colors;

-- Equivalent to (old syntax)
SELECT 
    sizes.size,
    colors.color
FROM sizes, colors;
```

**Use Cases:**
- Generate all combinations
- Testing scenarios
- Rarely used in production

**Warning:** Can produce very large result sets!

### Self JOIN

**Definition:** Self JOIN joins a table to itself.

**Syntax:**
```sql
-- Find employees and their managers
SELECT 
    e.id AS employee_id,
    e.name AS employee_name,
    m.name AS manager_name
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;

-- Find all pairs of employees in same department
SELECT 
    e1.name AS employee1,
    e2.name AS employee2,
    e1.department
FROM employees e1
INNER JOIN employees e2 ON e1.department = e2.department
WHERE e1.id < e2.id;  -- Avoid duplicates and self-pairs
```

**Use Cases:**
- Hierarchical data (employees-managers)
- Finding relationships within same table
- Comparing rows in same table

---

## 🔍 Subqueries

### What are Subqueries?

**Definition:** Subqueries are queries nested inside another query.

**Real-life example:**
Like asking "Who ordered the most expensive item?" - you first find the most expensive item, then find who ordered it.

**Types:**
- Scalar subquery (returns single value)
- Row subquery (returns single row)
- Column subquery (returns single column)
- Table subquery (returns table)

### Scalar Subquery

**Definition:** Returns a single value (one row, one column).

**Syntax:**
```sql
-- In SELECT clause
SELECT 
    name,
    salary,
    (SELECT AVG(salary) FROM employees) AS avg_salary,
    salary - (SELECT AVG(salary) FROM employees) AS difference
FROM employees;

-- In WHERE clause
SELECT * FROM products
WHERE price > (SELECT AVG(price) FROM products);

-- In HAVING clause
SELECT department, AVG(salary) AS avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > (SELECT AVG(salary) FROM employees);
```

**Use Cases:**
- Compare with aggregate values
- Calculate differences
- Filter based on calculated values

### Column Subquery

**Definition:** Returns a single column (multiple rows).

**Syntax:**
```sql
-- With IN
SELECT * FROM orders
WHERE customer_id IN (
    SELECT id FROM customers WHERE status = 'active'
);

-- With NOT IN
SELECT * FROM products
WHERE id NOT IN (
    SELECT product_id FROM order_items
);

-- With ANY/SOME
SELECT * FROM products
WHERE price > ANY (
    SELECT price FROM products WHERE category = 'premium'
);

-- With ALL
SELECT * FROM products
WHERE price > ALL (
    SELECT price FROM products WHERE category = 'budget'
);
```

**Use Cases:**
- Filter based on list of values
- Exclude based on related data
- Compare with multiple values

### Row Subquery

**Definition:** Returns a single row (multiple columns).

**Syntax:**
```sql
-- Compare multiple columns
SELECT * FROM employees
WHERE (department, salary) = (
    SELECT department, MAX(salary)
    FROM employees
    GROUP BY department
    LIMIT 1
);
```

### Table Subquery (Derived Table)

**Definition:** Returns a table (used in FROM clause).

**Syntax:**
```sql
-- In FROM clause
SELECT 
    sub.category,
    AVG(sub.total_sales) AS avg_sales
FROM (
    SELECT 
        category,
        SUM(amount) AS total_sales
    FROM sales
    GROUP BY category
) AS sub
GROUP BY sub.category;

-- With JOIN
SELECT 
    c.name,
    o.order_count
FROM customers c
LEFT JOIN (
    SELECT 
        customer_id,
        COUNT(*) AS order_count
    FROM orders
    GROUP BY customer_id
) o ON c.id = o.customer_id;
```

**Use Cases:**
- Complex aggregations
- Pre-filtering data
- Creating temporary result sets

### Correlated Subquery

**Definition:** Correlated subquery references columns from the outer query.

**Syntax:**
```sql
-- Find employees earning more than their department average
SELECT 
    e1.name,
    e1.salary,
    e1.department
FROM employees e1
WHERE e1.salary > (
    SELECT AVG(e2.salary)
    FROM employees e2
    WHERE e2.department = e1.department  -- References outer query
);

-- Find latest order for each customer
SELECT 
    o1.customer_id,
    o1.id AS order_id,
    o1.order_date
FROM orders o1
WHERE o1.order_date = (
    SELECT MAX(o2.order_date)
    FROM orders o2
    WHERE o2.customer_id = o1.customer_id
);
```

**Use Cases:**
- Compare with related aggregates
- Find top N per group
- Complex filtering

**Performance Note:** Correlated subqueries can be slow - consider JOINs or window functions.

---

## ⚡ JOIN vs Subquery

### When to Use JOIN

**Advantages:**
- Usually faster
- More readable for simple relationships
- Better for combining multiple tables

**Example:**
```sql
-- JOIN (preferred)
SELECT 
    c.name,
    o.total
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id;
```

### When to Use Subquery

**Advantages:**
- More intuitive for complex logic
- Better for existence checks
- Easier for correlated comparisons

**Example:**
```sql
-- Subquery (when checking existence)
SELECT * FROM customers
WHERE EXISTS (
    SELECT 1 FROM orders 
    WHERE orders.customer_id = customers.id
);
```

### Converting Between JOIN and Subquery

**INNER JOIN ↔ IN/EXISTS:**
```sql
-- These are equivalent:
SELECT * FROM customers c
INNER JOIN orders o ON c.id = o.customer_id;

SELECT * FROM customers
WHERE id IN (SELECT customer_id FROM orders);

SELECT * FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
```

**LEFT JOIN ↔ NOT IN/NOT EXISTS:**
```sql
-- Find customers with no orders
SELECT c.* FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;

SELECT * FROM customers
WHERE id NOT IN (SELECT customer_id FROM orders WHERE customer_id IS NOT NULL);

SELECT * FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
```

---

## 🎯 Use Cases & Efficiency

### Efficient JOIN Patterns

**1. Index Foreign Keys:**
```sql
-- Index foreign keys for faster JOINs
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);
```

**2. Join Order Matters:**
```sql
-- Join smaller tables first when possible
-- Database optimizer usually handles this, but be aware
SELECT ...
FROM small_table s
INNER JOIN large_table l ON s.id = l.small_id;
```

**3. Use Appropriate JOIN Type:**
```sql
-- Use INNER JOIN when you only need matches
-- Use LEFT JOIN when you need all from left table
-- Avoid unnecessary OUTER JOINs
```

### Subquery Optimization

**1. Avoid Correlated Subqueries When Possible:**
```sql
-- Slow: Correlated subquery
SELECT 
    e1.name,
    (SELECT AVG(e2.salary) FROM employees e2 
     WHERE e2.department = e1.department) AS avg_salary
FROM employees e1;

-- Fast: JOIN with aggregation
SELECT 
    e.name,
    d.avg_salary
FROM employees e
INNER JOIN (
    SELECT department, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department
) d ON e.department = d.department;
```

**2. Use EXISTS for Existence Checks:**
```sql
-- EXISTS is usually faster than IN for large datasets
SELECT * FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.id
);
```

**3. Limit Subquery Results:**
```sql
-- Use LIMIT in subqueries when appropriate
SELECT * FROM products
WHERE price > (
    SELECT price FROM products 
    ORDER BY price DESC 
    LIMIT 1 OFFSET 9  -- 10th highest price
);
```

---

## 🔍 Interview Questions (4 Years Experience)

### Common Questions:

**1. What's the difference between INNER JOIN and LEFT JOIN?**
- INNER JOIN: Only matching rows from both tables
- LEFT JOIN: All rows from left table + matching rows from right (NULLs for no match)

**2. When would you use a subquery vs a JOIN?**
- JOIN: Combining related data, usually faster
- Subquery: Complex logic, existence checks, correlated comparisons

**3. What's a correlated subquery?**
- Subquery that references columns from outer query
- Executed once per row (can be slow)
- Example: Finding employees earning more than department average

**4. How do you optimize slow JOINs?**
- Index foreign key columns
- Index columns used in JOIN conditions
- Use appropriate JOIN types
- Consider query execution plan

**5. What's the difference between EXISTS and IN?**
- EXISTS: Returns true/false, stops on first match (usually faster)
- IN: Returns matching values, processes all values
- Use EXISTS for existence checks, IN for value lists

**6. How do you find records that don't have matches?**
```sql
-- Using LEFT JOIN
SELECT c.* FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;

-- Using NOT EXISTS (often faster)
SELECT * FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.id
);
```

