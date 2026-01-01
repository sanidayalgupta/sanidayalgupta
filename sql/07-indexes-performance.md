# Indexes & Performance Optimization

## 📇 Indexes

### What are Indexes?

**Definition:** Indexes are data structures that improve the speed of data retrieval operations on database tables.

**Real-life example:**
Like an index in a book - instead of reading every page to find a topic, you check the index to jump directly to the right page.

**How Indexes Work:**
- Create a separate data structure (B-tree, Hash, etc.)
- Store sorted references to table rows
- Allow fast lookups without scanning entire table

**Trade-offs:**
- ✅ Faster SELECT queries
- ✅ Faster JOINs
- ✅ Faster ORDER BY
- ❌ Slower INSERT/UPDATE/DELETE (must update index)
- ❌ Additional storage space

---

## 🔧 Types of Indexes

### Primary Key Index

**Definition:** Automatically created when you define a PRIMARY KEY.

```sql
CREATE TABLE students (
    id INT PRIMARY KEY,  -- Automatically indexed
    name VARCHAR(100)
);
```

**Characteristics:**
- Unique
- Not NULL
- Automatically indexed
- Clustered index (in most databases)

### Unique Index

**Definition:** Ensures uniqueness and improves lookup performance.

```sql
-- Create unique index
CREATE UNIQUE INDEX idx_email ON users(email);

-- Or via constraint
ALTER TABLE users ADD CONSTRAINT unique_email UNIQUE (email);
```

### Composite Index

**Definition:** Index on multiple columns.

```sql
-- Composite index
CREATE INDEX idx_name_age ON students(name, age);

-- Order matters! Leftmost prefix rule
-- This index helps:
SELECT * FROM students WHERE name = 'John';
SELECT * FROM students WHERE name = 'John' AND age = 20;
-- But NOT this:
SELECT * FROM students WHERE age = 20;  -- Can't use index efficiently
```

**Leftmost Prefix Rule:**
- Index on (A, B, C) helps queries on:
  - A
  - A, B
  - A, B, C
- But NOT on B or C alone

### Covering Index

**Definition:** Index that contains all columns needed for a query.

```sql
-- Covering index (includes all SELECT columns)
CREATE INDEX idx_covering ON orders(customer_id, order_date, total);

-- Query can use index only (no table lookup)
SELECT customer_id, order_date, total
FROM orders
WHERE customer_id = 1;
-- All data in index, no table access needed!
```

**Benefits:**
- Faster queries (index-only scans)
- Less I/O
- Better performance

---

## 🚀 Query Execution Plan

### What is Execution Plan?

**Definition:** Execution plan shows how the database will execute a query.

**Viewing Execution Plans:**
```sql
-- MySQL
EXPLAIN SELECT * FROM orders WHERE customer_id = 1;

-- PostgreSQL
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 1;

-- SQL Server
SET SHOWPLAN_ALL ON;
SELECT * FROM orders WHERE customer_id = 1;
```

**Understanding EXPLAIN Output:**
```sql
EXPLAIN SELECT * FROM orders WHERE customer_id = 1;

-- Key columns to understand:
-- type: ALL (full table scan) vs ref (index lookup)
-- key: Which index is used
-- rows: Estimated rows examined
-- Extra: Additional information
```

**Common Types:**
- **ALL**: Full table scan (bad, no index used)
- **index**: Full index scan
- **range**: Index range scan
- **ref**: Index lookup
- **eq_ref**: Unique index lookup
- **const**: Constant lookup (fastest)

---

## ⚡ Performance Optimization

### Index Selection Strategy

**1. Index Columns in WHERE Clauses:**
```sql
-- Query
SELECT * FROM orders WHERE customer_id = 1;

-- Create index
CREATE INDEX idx_orders_customer ON orders(customer_id);
```

**2. Index Columns in JOINs:**
```sql
-- Query
SELECT * FROM orders o
JOIN customers c ON o.customer_id = c.id;

-- Index foreign keys
CREATE INDEX idx_orders_customer ON orders(customer_id);
-- (customers.id is already indexed as PRIMARY KEY)
```

**3. Index Columns in ORDER BY:**
```sql
-- Query
SELECT * FROM products ORDER BY price DESC;

-- Create index
CREATE INDEX idx_products_price ON products(price);
```

**4. Composite Indexes for Multiple Conditions:**
```sql
-- Query
SELECT * FROM orders 
WHERE customer_id = 1 AND status = 'completed'
ORDER BY order_date DESC;

-- Composite index
CREATE INDEX idx_orders_customer_status_date 
ON orders(customer_id, status, order_date);
```

### Query Optimization Techniques

**1. Avoid SELECT ***
```sql
-- Bad: Fetches all columns
SELECT * FROM orders;

-- Good: Only needed columns
SELECT id, total, order_date FROM orders;
```

**2. Use LIMIT:**
```sql
-- Limit result set
SELECT * FROM orders ORDER BY order_date DESC LIMIT 10;
```

**3. Filter Early:**
```sql
-- Filter before JOIN
SELECT o.*, c.name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
WHERE o.total > 100;  -- Filter early
```

**4. Use Appropriate JOINs:**
```sql
-- Use INNER JOIN when you only need matches
-- Use LEFT JOIN only when you need all from left table
```

**5. Avoid Functions on Indexed Columns:**
```sql
-- Bad: Can't use index
SELECT * FROM orders WHERE YEAR(order_date) = 2024;

-- Good: Can use index
SELECT * FROM orders 
WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01';
```

**6. Use EXISTS Instead of IN (for large subqueries):**
```sql
-- EXISTS often faster for large datasets
SELECT * FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.id
);
```

### Index Maintenance

**1. Monitor Index Usage:**
```sql
-- MySQL: Check index usage
SHOW INDEX FROM orders;

-- Find unused indexes
SELECT 
    TABLE_NAME,
    INDEX_NAME,
    SEQ_IN_INDEX,
    COLUMN_NAME
FROM INFORMATION_SCHEMA.STATISTICS
WHERE TABLE_SCHEMA = 'your_database'
AND TABLE_NAME = 'orders';
```

**2. Rebuild Indexes:**
```sql
-- Rebuild index (MySQL)
ALTER TABLE orders DROP INDEX idx_customer;
CREATE INDEX idx_customer ON orders(customer_id);

-- Rebuild all indexes (PostgreSQL)
REINDEX TABLE orders;
```

**3. Analyze Tables:**
```sql
-- Update statistics (helps query optimizer)
ANALYZE TABLE orders;

-- MySQL
OPTIMIZE TABLE orders;
```

---

## 🎯 Performance Best Practices

### Index Design Principles

**1. Don't Over-Index:**
- Each index slows INSERT/UPDATE/DELETE
- Only index frequently queried columns
- Monitor and remove unused indexes

**2. Index Selectivity:**
```sql
-- High selectivity (good for index)
-- Many unique values
CREATE INDEX idx_email ON users(email);

-- Low selectivity (may not help much)
-- Few unique values
CREATE INDEX idx_gender ON users(gender);  -- Only 2-3 values
```

**3. Index Order Matters:**
```sql
-- For query: WHERE A = ? AND B = ? ORDER BY C
-- Best index: (A, B, C)
CREATE INDEX idx_abc ON table(A, B, C);
```

**4. Partial Indexes:**
```sql
-- Index only subset of rows (PostgreSQL)
CREATE INDEX idx_active_orders ON orders(customer_id)
WHERE status = 'active';
-- Smaller index, faster queries
```

### Query Patterns to Avoid

**1. N+1 Query Problem:**
```sql
-- Bad: N+1 queries
-- 1 query for customers, N queries for orders
SELECT * FROM customers;
-- Then for each customer:
SELECT * FROM orders WHERE customer_id = ?;

-- Good: Single query with JOIN
SELECT c.*, o.*
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id;
```

**2. Unnecessary Subqueries:**
```sql
-- Bad: Correlated subquery
SELECT 
    name,
    (SELECT AVG(salary) FROM employees e2 
     WHERE e2.department = e1.department) AS avg_salary
FROM employees e1;

-- Good: JOIN with aggregation
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

**3. Implicit Type Conversions:**
```sql
-- Bad: String comparison (can't use index)
SELECT * FROM orders WHERE customer_id = '1';

-- Good: Correct type
SELECT * FROM orders WHERE customer_id = 1;
```

---

## 🔍 Interview Questions (4 Years Experience)

### Common Questions:

**1. When should you create an index?**
- Columns in WHERE clauses
- Foreign keys (for JOINs)
- Columns in ORDER BY
- Frequently queried columns
- High selectivity columns

**2. What's the trade-off of indexes?**
- Faster SELECT queries
- Slower INSERT/UPDATE/DELETE (must update index)
- Additional storage space
- Maintenance overhead

**3. How do you know if an index is being used?**
- Use EXPLAIN to see execution plan
- Check if 'key' column shows index name
- Monitor index usage statistics
- Look for 'Using index' in Extra column

**4. What's a covering index?**
- Index that contains all columns needed for query
- Allows index-only scans (no table access)
- Significantly faster queries

**5. How do you optimize a slow query?**
- Use EXPLAIN to analyze execution plan
- Add indexes on filtered/joined columns
- Rewrite query to use indexes
- Avoid functions on indexed columns
- Use appropriate JOIN types

**6. What's the leftmost prefix rule?**
- Index on (A, B, C) helps queries on A, (A, B), or (A, B, C)
- But NOT on B or C alone
- Order of columns in composite index matters

**7. How do you handle index maintenance?**
- Monitor index usage
- Remove unused indexes
- Rebuild fragmented indexes
- Update table statistics
- Balance query performance vs write performance

