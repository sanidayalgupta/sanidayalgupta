# Advanced SQL Topics

## ❓ NULL Handling

### What is NULL?

**Definition:** NULL represents the absence of a value - it's not zero, not empty string, not false. It's unknown/missing.

**Real-life example:**
Like an unanswered question - you don't know the answer, it's not "no", it's just unknown.

**Important:**
- NULL ≠ NULL (NULL != NULL is TRUE)
- Use IS NULL / IS NOT NULL to check
- NULL in calculations results in NULL
- NULL in aggregations is ignored (except COUNT)

### NULL Operations

**Checking for NULL:**
```sql
-- Correct way
SELECT * FROM customers WHERE email IS NULL;
SELECT * FROM customers WHERE email IS NOT NULL;

-- Wrong way (doesn't work!)
SELECT * FROM customers WHERE email = NULL;  -- Always FALSE
SELECT * FROM customers WHERE email != NULL;  -- Always FALSE
```

**NULL in Calculations:**
```sql
-- NULL in arithmetic = NULL
SELECT 10 + NULL;  -- Returns NULL
SELECT 10 * NULL;  -- Returns NULL

-- NULL in comparisons
SELECT * FROM products WHERE price > 100;  -- Excludes NULL prices
```

**NULL in Aggregations:**
```sql
-- COUNT(*) counts all rows including NULLs
SELECT COUNT(*) FROM customers;  -- Counts all rows

-- COUNT(column) excludes NULLs
SELECT COUNT(email) FROM customers;  -- Excludes NULL emails

-- Other aggregates ignore NULLs
SELECT AVG(price) FROM products;  -- NULL prices ignored
SELECT SUM(quantity) FROM order_items;  -- NULL quantities ignored
```

### COALESCE

**Definition:** COALESCE returns the first non-NULL value.

```sql
-- Return first non-NULL value
SELECT COALESCE(middle_name, '') AS middle_name FROM users;
SELECT COALESCE(phone, email, 'No contact') AS contact FROM customers;

-- Default value
SELECT 
    name,
    COALESCE(discount, 0) AS discount
FROM products;
```

**Use Cases:**
- Provide default values
- Handle missing data
- Simplify NULL checks

### NULLIF

**Definition:** NULLIF returns NULL if two values are equal.

```sql
-- Returns NULL if values match
SELECT NULLIF(price, 0) AS price FROM products;
-- If price is 0, returns NULL instead

-- Useful for avoiding division by zero
SELECT 
    total,
    quantity,
    total / NULLIF(quantity, 0) AS unit_price
FROM order_items;
```

### IFNULL / ISNULL

**Definition:** Database-specific functions for NULL handling.

```sql
-- MySQL: IFNULL
SELECT IFNULL(discount, 0) AS discount FROM products;

-- SQL Server: ISNULL
SELECT ISNULL(discount, 0) AS discount FROM products;

-- Standard: COALESCE (works everywhere)
SELECT COALESCE(discount, 0) AS discount FROM products;
```

---

## 📄 Pagination

### What is Pagination?

**Definition:** Pagination splits large result sets into smaller pages.

**Real-life example:**
Like book pages - instead of showing all 1000 results, show 20 per page.

### LIMIT and OFFSET

**Basic Pagination:**
```sql
-- First page (rows 1-20)
SELECT * FROM products ORDER BY id LIMIT 20 OFFSET 0;

-- Second page (rows 21-40)
SELECT * FROM products ORDER BY id LIMIT 20 OFFSET 20;

-- Third page (rows 41-60)
SELECT * FROM products ORDER BY id LIMIT 20 OFFSET 40;

-- General formula: LIMIT page_size OFFSET (page - 1) * page_size
```

**Efficient Pagination:**
```sql
-- Cursor-based pagination (more efficient for large datasets)
-- First page
SELECT * FROM products WHERE id > 0 ORDER BY id LIMIT 20;
-- Remember last id: 20

-- Next page
SELECT * FROM products WHERE id > 20 ORDER BY id LIMIT 20;
-- Remember last id: 40

-- Next page
SELECT * FROM products WHERE id > 40 ORDER BY id LIMIT 20;
```

**Why Cursor-Based is Better:**
- OFFSET becomes slow for large offsets (must skip many rows)
- Cursor-based uses index efficiently
- Consistent results (no issues with new data)

**Total Count:**
```sql
-- Get total count for pagination
SELECT COUNT(*) AS total FROM products;

-- Then paginate
SELECT * FROM products ORDER BY id LIMIT 20 OFFSET 0;
```

---

## 📋 Temporary Tables

### What are Temporary Tables?

**Definition:** Temporary tables exist only for the current session and are automatically dropped.

**Real-life example:**
Like a scratch pad - you write temporary notes, use them, then they're automatically thrown away.

### Creating Temporary Tables

**Basic Temporary Table:**
```sql
-- Create temporary table
CREATE TEMPORARY TABLE temp_orders AS
SELECT * FROM orders WHERE order_date > '2024-01-01';

-- Use temporary table
SELECT * FROM temp_orders;

-- Automatically dropped when session ends
```

**Temporary Table with Structure:**
```sql
-- Create structure
CREATE TEMPORARY TABLE temp_results (
    id INT,
    name VARCHAR(100),
    total DECIMAL(10, 2)
);

-- Insert data
INSERT INTO temp_results VALUES (1, 'Order 1', 100.00);

-- Use in queries
SELECT * FROM temp_results;
```

**Use Cases:**
- Complex calculations
- Staging data
- Temporary aggregations
- Testing queries

**Best Practices:**
- Use for session-specific data
- Clean up explicitly if needed
- Don't use for permanent data
- Consider CTEs for simpler cases

---

## 🔍 Interview Questions (4 Years Experience)

### Common Questions:

**1. How do you handle NULL values?**
- Use IS NULL / IS NOT NULL to check
- Use COALESCE for default values
- NULL in calculations = NULL
- Aggregates ignore NULL (except COUNT)

**2. What's the difference between COUNT(*) and COUNT(column)?**
- COUNT(*): Counts all rows including NULLs
- COUNT(column): Counts non-NULL values in column
- COUNT(*) is usually faster

**3. How do you implement pagination efficiently?**
- Use LIMIT and OFFSET for small datasets
- Use cursor-based pagination for large datasets
- Cursor-based is faster (uses index, no OFFSET scan)

**4. When would you use a temporary table?**
- Complex multi-step calculations
- Staging data for processing
- Session-specific data
- Testing queries

**5. What's the performance difference between OFFSET and cursor-based pagination?**
- OFFSET: Must skip rows (slow for large offsets)
- Cursor-based: Uses index efficiently (faster)
- Cursor-based is better for large datasets

**6. How do you handle NULL in aggregations?**
- Most aggregates ignore NULL automatically
- COUNT(column) excludes NULLs
- Use COALESCE if you need to treat NULL as 0

