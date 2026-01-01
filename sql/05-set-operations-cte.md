# Set Operations & CTEs

## 🔄 Set Operations

### What are Set Operations?

**Definition:** Set operations combine results from multiple SELECT statements.

**Real-life example:**
Like combining two lists - UNION merges them (removing duplicates), INTERSECT finds common items, EXCEPT finds items only in first list.

**Types:**
- UNION: Combine results (remove duplicates)
- UNION ALL: Combine results (keep duplicates)
- INTERSECT: Common rows
- EXCEPT/MINUS: Rows in first but not second

---

## 📊 UNION

### UNION

**Definition:** UNION combines results from two SELECT statements and removes duplicates.

**Syntax:**
```sql
-- Basic UNION
SELECT name FROM customers
UNION
SELECT name FROM suppliers;

-- UNION with same columns
SELECT id, name, 'customer' AS type FROM customers
UNION
SELECT id, name, 'supplier' AS type FROM suppliers;

-- Multiple UNIONs
SELECT name FROM table1
UNION
SELECT name FROM table2
UNION
SELECT name FROM table3;
```

**Rules:**
- Same number of columns
- Compatible data types
- Column names from first SELECT
- Removes duplicate rows

**Use Cases:**
- Combine similar data from different tables
- Merge results from different queries
- Create unified result sets

**Example:**
```sql
-- All people (customers and employees)
SELECT 
    id,
    name,
    email,
    'customer' AS person_type
FROM customers
UNION
SELECT 
    id,
    name,
    email,
    'employee' AS person_type
FROM employees
ORDER BY name;
```

### UNION ALL

**Definition:** UNION ALL combines results and keeps all rows (including duplicates).

**Syntax:**
```sql
-- UNION ALL (faster, keeps duplicates)
SELECT name FROM customers
UNION ALL
SELECT name FROM suppliers;
```

**When to Use:**
- When duplicates are acceptable
- Better performance (no duplicate removal)
- When you know there are no duplicates

**Performance:**
```sql
-- UNION ALL is faster (no duplicate check)
SELECT * FROM table1
UNION ALL  -- Faster
SELECT * FROM table2;

-- UNION is slower (checks for duplicates)
SELECT * FROM table1
UNION  -- Slower
SELECT * FROM table2;
```

---

## 🔍 INTERSECT

### INTERSECT

**Definition:** INTERSECT returns rows that exist in both result sets.

**Syntax:**
```sql
-- Rows in both queries
SELECT product_id FROM order_items
INTERSECT
SELECT product_id FROM wishlist_items;

-- Products ordered by premium customers
SELECT product_id FROM order_items oi
INNER JOIN orders o ON oi.order_id = o.id
INNER JOIN customers c ON o.customer_id = c.id
WHERE c.status = 'premium'
INTERSECT
SELECT product_id FROM products WHERE category = 'electronics';
```

**Note:** MySQL doesn't support INTERSECT (use INNER JOIN instead).

**MySQL Alternative:**
```sql
-- Using INNER JOIN (MySQL)
SELECT DISTINCT oi1.product_id
FROM order_items oi1
INNER JOIN order_items oi2 ON oi1.product_id = oi2.product_id
WHERE oi1.order_id IN (SELECT id FROM orders WHERE customer_id = 1)
AND oi2.order_id IN (SELECT id FROM orders WHERE customer_id = 2);
```

---

## ➖ EXCEPT / MINUS

### EXCEPT

**Definition:** EXCEPT returns rows from first query that don't exist in second query.

**Syntax:**
```sql
-- Rows in first but not second
SELECT product_id FROM all_products
EXCEPT
SELECT product_id FROM discontinued_products;

-- Customers who never ordered
SELECT id FROM customers
EXCEPT
SELECT customer_id FROM orders;
```

**Note:** MySQL uses EXCEPT, Oracle uses MINUS (same operation).

**MySQL Alternative:**
```sql
-- Using NOT IN (MySQL)
SELECT id FROM customers
WHERE id NOT IN (SELECT customer_id FROM orders WHERE customer_id IS NOT NULL);

-- Using LEFT JOIN (often faster)
SELECT c.id FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;
```

---

## 📝 Common Table Expressions (CTE)

### What are CTEs?

**Definition:** CTEs (WITH clauses) create temporary named result sets that exist only for the duration of the query.

**Real-life example:**
Like creating a temporary worksheet - you calculate something once, give it a name, then use it multiple times in your main calculation.

**Syntax:**
```sql
-- Basic CTE
WITH high_salary_employees AS (
    SELECT * FROM employees WHERE salary > 100000
)
SELECT * FROM high_salary_employees;

-- Multiple CTEs
WITH 
    active_customers AS (
        SELECT * FROM customers WHERE status = 'active'
    ),
    recent_orders AS (
        SELECT * FROM orders WHERE order_date > '2024-01-01'
    )
SELECT 
    c.name,
    COUNT(o.id) AS order_count
FROM active_customers c
LEFT JOIN recent_orders o ON c.id = o.customer_id
GROUP BY c.id, c.name;
```

**Advantages:**
- Improves readability
- Reusable within query
- Can reference itself (recursive)
- Better than subqueries for complex logic

### Simple CTE Examples

**Example 1: Simplifying Complex Queries**
```sql
-- Without CTE (complex subquery)
SELECT 
    department,
    AVG(salary) AS avg_salary
FROM employees
WHERE department IN (
    SELECT department 
    FROM employees 
    GROUP BY department 
    HAVING COUNT(*) > 10
)
GROUP BY department;

-- With CTE (clearer)
WITH large_departments AS (
    SELECT department 
    FROM employees 
    GROUP BY department 
    HAVING COUNT(*) > 10
)
SELECT 
    e.department,
    AVG(e.salary) AS avg_salary
FROM employees e
INNER JOIN large_departments ld ON e.department = ld.department
GROUP BY e.department;
```

**Example 2: Reusing Calculations**
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
    sales - LAG(sales) OVER (ORDER BY year, month) AS change_from_previous,
    AVG(sales) OVER (ORDER BY year, month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg
FROM monthly_sales;
```

### Recursive CTEs

**Definition:** Recursive CTEs reference themselves, useful for hierarchical data.

**Syntax:**
```sql
-- Recursive CTE structure
WITH RECURSIVE cte_name AS (
    -- Anchor member (base case)
    SELECT ... WHERE condition
    
    UNION ALL
    
    -- Recursive member (references CTE)
    SELECT ... FROM cte_name WHERE condition
)
SELECT * FROM cte_name;
```

**Example: Employee Hierarchy**
```sql
-- Find all subordinates of a manager
WITH RECURSIVE employee_hierarchy AS (
    -- Anchor: Start with manager
    SELECT 
        id,
        name,
        manager_id,
        0 AS level
    FROM employees
    WHERE id = 1  -- Manager ID
    
    UNION ALL
    
    -- Recursive: Find subordinates
    SELECT 
        e.id,
        e.name,
        e.manager_id,
        eh.level + 1
    FROM employees e
    INNER JOIN employee_hierarchy eh ON e.manager_id = eh.id
)
SELECT * FROM employee_hierarchy;
```

**Example: Category Tree**
```sql
-- Get all subcategories
WITH RECURSIVE category_tree AS (
    -- Anchor: Root categories
    SELECT 
        id,
        name,
        parent_id,
        name AS path
    FROM categories
    WHERE parent_id IS NULL
    
    UNION ALL
    
    -- Recursive: Child categories
    SELECT 
        c.id,
        c.name,
        c.parent_id,
        CONCAT(ct.path, ' > ', c.name)
    FROM categories c
    INNER JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT * FROM category_tree;
```

**Use Cases:**
- Hierarchical data (org charts, categories)
- Tree traversal
- Generating sequences
- Path finding

---

## 🎯 Use Cases & Efficiency

### When to Use Set Operations

**UNION:**
- Combine similar data from different sources
- Merge results with same structure
- Create unified views

**INTERSECT:**
- Find common elements
- Data validation
- Finding overlaps

**EXCEPT:**
- Find differences
- Exclude specific data
- Data cleanup

### When to Use CTEs

**Use CTEs When:**
- Query is complex and hard to read
- Need to reference same subquery multiple times
- Working with hierarchical data (recursive)
- Building complex reports step-by-step

**Avoid CTEs When:**
- Simple queries (adds unnecessary complexity)
- Performance is critical (sometimes subqueries are faster)
- Database doesn't support CTEs well

### Performance Considerations

**1. UNION vs UNION ALL:**
```sql
-- Use UNION ALL when duplicates don't matter (faster)
SELECT * FROM table1
UNION ALL  -- No duplicate check
SELECT * FROM table2;

-- Use UNION only when you need to remove duplicates
SELECT * FROM table1
UNION  -- Removes duplicates (slower)
SELECT * FROM table2;
```

**2. CTE Performance:**
- CTEs are materialized in some databases (PostgreSQL)
- In MySQL, CTEs are often inlined (like subqueries)
- Test performance vs subqueries
- Consider temporary tables for very complex CTEs

**3. Indexing:**
- Index columns used in UNION/INTERSECT/EXCEPT
- Index columns used in CTE WHERE clauses
- Index columns used in recursive CTE joins

---

## 🔍 Interview Questions (4 Years Experience)

### Common Questions:

**1. What's the difference between UNION and UNION ALL?**
- UNION: Removes duplicates, slower
- UNION ALL: Keeps duplicates, faster
- Use UNION ALL when duplicates don't matter

**2. When would you use a CTE vs a subquery?**
- CTE: Complex logic, readability, recursive queries
- Subquery: Simple filtering, single-use calculations
- CTEs improve readability for complex queries

**3. How do you handle hierarchical data in SQL?**
- Use recursive CTEs
- Example: Employee-manager relationships, category trees
- Can traverse up or down the hierarchy

**4. What's the performance difference between UNION and UNION ALL?**
- UNION ALL: O(n) - just concatenates
- UNION: O(n log n) - sorts and removes duplicates
- UNION ALL is significantly faster for large datasets

**5. Can you use CTEs in UPDATE/DELETE statements?**
- Yes, in most modern databases
- Useful for complex update/delete logic
- Example: Delete based on CTE calculations

**6. How do you find rows in one table but not another?**
```sql
-- Using EXCEPT (if supported)
SELECT id FROM table1
EXCEPT
SELECT id FROM table2;

-- Using NOT IN (MySQL)
SELECT id FROM table1
WHERE id NOT IN (SELECT id FROM table2 WHERE id IS NOT NULL);

-- Using LEFT JOIN (often faster)
SELECT t1.id FROM table1 t1
LEFT JOIN table2 t2 ON t1.id = t2.id
WHERE t2.id IS NULL;
```

