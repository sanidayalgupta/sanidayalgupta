# SQL Basics

## 📚 SQL Fundamentals

### What is SQL?

**Definition:** SQL (Structured Query Language) is a programming language designed for managing and manipulating relational databases.

**Real-life example:**
Like a universal language for talking to databases - whether it's MySQL, PostgreSQL, or SQLite, SQL lets you ask questions and give commands in the same way.

**Why SQL?**
- Standardized language across database systems
- Declarative (you say what you want, not how to get it)
- Powerful for data manipulation and retrieval
- Industry standard for database operations

---

## 🔄 CRUD Operations

### What are CRUD Operations?

**Definition:** CRUD stands for Create, Read, Update, Delete - the four basic operations for data management.

**Real-life example:**
Like a filing cabinet:
- **Create** = Adding a new file
- **Read** = Looking up a file
- **Update** = Modifying an existing file
- **Delete** = Removing a file

### CREATE (INSERT)

**Definition:** INSERT adds new rows to a table.

**Basic Syntax:**
```sql
-- Insert single row
INSERT INTO students (name, email, age) 
VALUES ('John Doe', 'john@example.com', 20);

-- Insert multiple rows
INSERT INTO students (name, email, age) 
VALUES 
    ('Jane Smith', 'jane@example.com', 22),
    ('Bob Johnson', 'bob@example.com', 21);

-- Insert with SELECT (copy from another table)
INSERT INTO students_archive (name, email, age)
SELECT name, email, age 
FROM students 
WHERE age > 25;
```

**Use Cases:**
- Adding new records
- Bulk data import
- Data migration
- Duplicating data

**Best Practices:**
- Always specify column names (don't rely on order)
- Use transactions for multiple inserts
- Validate data before inserting
- Use prepared statements to prevent SQL injection

### READ (SELECT)

**Definition:** SELECT retrieves data from one or more tables.

**Basic Syntax:**
```sql
-- Select all columns
SELECT * FROM students;

-- Select specific columns
SELECT name, email FROM students;

-- Select with WHERE clause
SELECT * FROM students WHERE age > 18;

-- Select with ORDER BY
SELECT * FROM students ORDER BY age DESC;

-- Select with LIMIT
SELECT * FROM students LIMIT 10;
```

**Advanced SELECT:**
```sql
-- Select distinct values
SELECT DISTINCT department FROM employees;

-- Select with calculations
SELECT name, salary, salary * 1.1 AS new_salary FROM employees;

-- Select with CASE statement
SELECT 
    name,
    CASE 
        WHEN age < 18 THEN 'Minor'
        WHEN age < 65 THEN 'Adult'
        ELSE 'Senior'
    END AS age_group
FROM students;
```

**Use Cases:**
- Data retrieval
- Reporting
- Data analysis
- Data validation

**Efficiency Tips:**
- Select only needed columns (avoid SELECT *)
- Use WHERE to filter early
- Use indexes on filtered columns
- Limit result sets when possible

### UPDATE

**Definition:** UPDATE modifies existing rows in a table.

**Basic Syntax:**
```sql
-- Update single row
UPDATE students 
SET age = 21 
WHERE id = 1;

-- Update multiple columns
UPDATE students 
SET age = 21, email = 'newemail@example.com' 
WHERE id = 1;

-- Update multiple rows
UPDATE students 
SET status = 'active' 
WHERE age >= 18;

-- Update with subquery
UPDATE orders 
SET total = (
    SELECT SUM(price) 
    FROM order_items 
    WHERE order_items.order_id = orders.id
);
```

**Use Cases:**
- Modifying existing data
- Bulk updates
- Status changes
- Data corrections

**Best Practices:**
- Always use WHERE clause (unless updating all rows intentionally)
- Test with SELECT first
- Use transactions for critical updates
- Backup before bulk updates

### DELETE

**Definition:** DELETE removes rows from a table.

**Basic Syntax:**
```sql
-- Delete specific row
DELETE FROM students WHERE id = 1;

-- Delete multiple rows
DELETE FROM students WHERE age < 18;

-- Delete all rows (dangerous!)
DELETE FROM students;

-- Delete with subquery
DELETE FROM orders 
WHERE customer_id IN (
    SELECT id FROM customers WHERE status = 'inactive'
);
```

**Use Cases:**
- Removing obsolete data
- Data cleanup
- Compliance (GDPR, data retention)
- Archiving preparation

**Best Practices:**
- Always use WHERE clause
- Consider soft delete (is_deleted flag) instead
- Use transactions
- Backup before deletion
- Consider TRUNCATE for deleting all rows (faster)

**DELETE vs TRUNCATE:**
```sql
-- DELETE: Removes rows one by one, can be rolled back, slower
DELETE FROM students;

-- TRUNCATE: Removes all rows instantly, cannot be rolled back, faster
TRUNCATE TABLE students;
```

---

## 📊 Data Types

### What are Data Types?

**Definition:** Data types define what kind of data can be stored in a column.

**Real-life example:**
Like different containers - you can't put liquid in a box meant for solids. Each data type has specific uses.

### Numeric Types

**Integer Types:**
```sql
-- TINYINT: -128 to 127 (or 0 to 255 unsigned)
age TINYINT UNSIGNED

-- SMALLINT: -32,768 to 32,767
quantity SMALLINT

-- INT/INTEGER: -2,147,483,648 to 2,147,483,647
id INT PRIMARY KEY

-- BIGINT: Very large integers
user_id BIGINT

-- Example
CREATE TABLE products (
    id INT PRIMARY KEY,
    quantity SMALLINT,
    views_count BIGINT
);
```

**Decimal Types:**
```sql
-- DECIMAL(precision, scale): Exact decimal
-- DECIMAL(10, 2) = 10 digits total, 2 after decimal
price DECIMAL(10, 2)  -- Can store: 99999999.99

-- FLOAT: Approximate floating point
rating FLOAT

-- DOUBLE: Double precision floating point
scientific_value DOUBLE

-- Example
CREATE TABLE orders (
    id INT,
    total DECIMAL(10, 2),  -- For money
    discount_percentage FLOAT  -- For calculations
);
```

**When to Use:**
- **INT/BIGINT**: IDs, counts, quantities
- **DECIMAL**: Money, precise calculations
- **FLOAT/DOUBLE**: Scientific data, approximate values

### String Types

**Fixed-Length Strings:**
```sql
-- CHAR(n): Fixed length, padded with spaces
country_code CHAR(2)  -- Always 2 characters

-- Example
CREATE TABLE countries (
    code CHAR(2) PRIMARY KEY,  -- 'US', 'UK', 'IN'
    name VARCHAR(100)
);
```

**Variable-Length Strings:**
```sql
-- VARCHAR(n): Variable length up to n characters
name VARCHAR(100)  -- Can store up to 100 characters

-- TEXT: Large text (varies by database)
description TEXT

-- Example
CREATE TABLE users (
    username VARCHAR(50),
    email VARCHAR(255),
    bio TEXT  -- For long descriptions
);
```

**String Type Comparison:**
```sql
-- CHAR vs VARCHAR
-- CHAR(10) always uses 10 bytes: 'John      ' (padded)
-- VARCHAR(10) uses only needed bytes: 'John' (4 bytes)

-- Use CHAR for fixed-length data (codes, IDs)
-- Use VARCHAR for variable-length data (names, descriptions)
```

### Date and Time Types

**Date Types:**
```sql
-- DATE: Date only (YYYY-MM-DD)
birth_date DATE

-- TIME: Time only (HH:MM:SS)
start_time TIME

-- DATETIME: Date and time
created_at DATETIME

-- TIMESTAMP: Auto-updating timestamp
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

-- YEAR: Year only
graduation_year YEAR

-- Example
CREATE TABLE events (
    id INT PRIMARY KEY,
    event_date DATE,
    start_time TIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**Date Functions:**
```sql
-- Current date/time
SELECT NOW();  -- Current datetime
SELECT CURDATE();  -- Current date
SELECT CURTIME();  -- Current time

-- Date arithmetic
SELECT DATE_ADD('2024-01-01', INTERVAL 30 DAY);
SELECT DATE_SUB('2024-01-01', INTERVAL 1 MONTH);
SELECT DATEDIFF('2024-12-31', '2024-01-01');  -- Days difference

-- Extract parts
SELECT YEAR('2024-01-15');  -- 2024
SELECT MONTH('2024-01-15');  -- 1
SELECT DAY('2024-01-15');  -- 15
```

### Boolean Type

**Definition:** Boolean stores true/false values.

```sql
-- BOOLEAN or BOOL (often stored as TINYINT)
is_active BOOLEAN DEFAULT TRUE
is_deleted BOOLEAN DEFAULT FALSE

-- Example
CREATE TABLE users (
    id INT PRIMARY KEY,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE
);

-- Usage
SELECT * FROM users WHERE is_active = TRUE;
SELECT * FROM users WHERE is_active;  -- Shorthand
```

### Binary Types

**Definition:** Binary types store binary data (images, files, etc.).

```sql
-- BINARY(n): Fixed-length binary
hash BINARY(32)  -- For SHA-256 hashes

-- VARBINARY(n): Variable-length binary
image_data VARBINARY(MAX)  -- For images

-- BLOB: Binary Large Object
file_content BLOB

-- Example
CREATE TABLE documents (
    id INT PRIMARY KEY,
    file_name VARCHAR(255),
    file_content BLOB,
    file_hash BINARY(32)
);
```

**When to Use:**
- Store files in database (not recommended for large files)
- Store hashes, encrypted data
- Store binary data that needs to be queried

**Best Practice:** Store file paths in database, files on filesystem/cloud storage.

### JSON Type

**Definition:** JSON type stores JSON documents (MySQL 5.7+, PostgreSQL).

```sql
-- JSON: Store JSON data
metadata JSON

-- Example
CREATE TABLE products (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    attributes JSON  -- {"color": "red", "size": "L", "tags": ["new", "sale"]}
);

-- Query JSON
SELECT 
    id,
    name,
    JSON_EXTRACT(attributes, '$.color') AS color,
    attributes->>'$.size' AS size
FROM products
WHERE JSON_EXTRACT(attributes, '$.tags[0]') = 'new';
```

**Use Cases:**
- Flexible schema (NoSQL-like)
- Storing configuration
- API responses
- Metadata storage

---

## 🎯 Use Cases & Efficiency

### Efficient CRUD Patterns

**1. Bulk Operations:**
```sql
-- Inefficient: Multiple queries
INSERT INTO students (name, email) VALUES ('John', 'john@example.com');
INSERT INTO students (name, email) VALUES ('Jane', 'jane@example.com');
INSERT INTO students (name, email) VALUES ('Bob', 'bob@example.com');

-- Efficient: Single query
INSERT INTO students (name, email) VALUES
    ('John', 'john@example.com'),
    ('Jane', 'jane@example.com'),
    ('Bob', 'bob@example.com');
```

**2. Selective Updates:**
```sql
-- Inefficient: Update all then filter
UPDATE students SET status = 'active';
DELETE FROM students WHERE age < 18;

-- Efficient: Filter in UPDATE/DELETE
UPDATE students SET status = 'active' WHERE age >= 18;
DELETE FROM students WHERE age < 18;
```

**3. Transaction Usage:**
```sql
-- Use transactions for related operations
START TRANSACTION;
    INSERT INTO orders (customer_id, total) VALUES (1, 100.00);
    INSERT INTO order_items (order_id, product_id, quantity) VALUES (LAST_INSERT_ID(), 1, 2);
    UPDATE products SET stock = stock - 2 WHERE id = 1;
COMMIT;
```

### Data Type Selection Best Practices

**1. Choose Appropriate Sizes:**
```sql
-- Don't over-allocate
name VARCHAR(255)  -- If max name is 50, use VARCHAR(50)

-- Use smallest appropriate integer
age TINYINT UNSIGNED  -- Instead of INT (saves space)
```

**2. Use DECIMAL for Money:**
```sql
-- Never use FLOAT for money (precision issues)
price FLOAT  -- ❌ Bad: 0.1 + 0.2 = 0.30000000000000004

price DECIMAL(10, 2)  -- ✅ Good: Exact precision
```

**3. Consider Storage:**
```sql
-- CHAR vs VARCHAR
-- CHAR: Use for fixed-length (country codes, status codes)
country_code CHAR(2)  -- Always 2 characters

-- VARCHAR: Use for variable-length (names, descriptions)
name VARCHAR(100)  -- Variable length
```

---

## 🔍 Interview Questions (4 Years Experience)

### Common Questions:

**1. What's the difference between DELETE and TRUNCATE?**
- DELETE: Row-by-row deletion, can be rolled back, slower, can use WHERE
- TRUNCATE: Removes all rows instantly, cannot be rolled back, faster, resets auto-increment

**2. When would you use CHAR vs VARCHAR?**
- CHAR: Fixed-length data (codes, IDs) - faster for comparisons
- VARCHAR: Variable-length data (names, descriptions) - saves storage

**3. How do you handle bulk inserts efficiently?**
- Use single INSERT with multiple VALUES
- Use transactions
- Disable indexes temporarily for very large imports
- Use LOAD DATA INFILE for CSV imports

**4. What's the best data type for storing money?**
- DECIMAL(precision, scale) - exact precision, no floating-point errors
- Never use FLOAT/DOUBLE for money

**5. How do you update data based on another table?**
```sql
-- Using JOIN
UPDATE orders o
JOIN customers c ON o.customer_id = c.id
SET o.discount = 10
WHERE c.status = 'premium';

-- Using subquery
UPDATE orders
SET discount = 10
WHERE customer_id IN (
    SELECT id FROM customers WHERE status = 'premium'
);
```

