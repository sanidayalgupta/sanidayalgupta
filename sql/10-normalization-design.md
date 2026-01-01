# Normalization & Database Design

## 📐 Normalization

### What is Normalization?

**Definition:** Normalization is the process of organizing data to reduce redundancy and improve data integrity.

**Real-life example:**
Like organizing a filing cabinet - instead of storing customer address in every order file, you store it once in the customer file and reference it.

**Goals:**
- Eliminate data redundancy
- Reduce storage space
- Prevent update anomalies
- Improve data integrity

**Normal Forms:**
- 1NF: First Normal Form
- 2NF: Second Normal Form
- 3NF: Third Normal Form
- BCNF: Boyce-Codd Normal Form
- 4NF, 5NF: Higher normal forms

---

## 🔢 First Normal Form (1NF)

### Requirements

**Definition:** Each column contains atomic (indivisible) values, and each row is unique.

**Rules:**
- No repeating groups
- Each cell contains single value
- No duplicate rows

**Example - Before 1NF:**
```sql
-- Bad: Repeating groups
CREATE TABLE orders (
    id INT,
    customer_name VARCHAR(100),
    product1 VARCHAR(100),
    product2 VARCHAR(100),
    product3 VARCHAR(100)
);
```

**Example - After 1NF:**
```sql
-- Good: Atomic values
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE
);

CREATE TABLE order_items (
    order_id INT,
    product_id INT,
    quantity INT,
    PRIMARY KEY (order_id, product_id)
);
```

---

## 🔢 Second Normal Form (2NF)

### Requirements

**Definition:** Must be in 1NF, and all non-key attributes must depend on the entire primary key.

**Rules:**
- In 1NF
- No partial dependencies (non-key depends on part of composite key)

**Example - Before 2NF:**
```sql
-- Bad: Partial dependency
CREATE TABLE order_items (
    order_id INT,
    product_id INT,
    product_name VARCHAR(100),  -- Depends only on product_id, not order_id
    quantity INT,
    PRIMARY KEY (order_id, product_id)
);
-- product_name depends only on product_id (partial dependency)
```

**Example - After 2NF:**
```sql
-- Good: Full dependency
CREATE TABLE order_items (
    order_id INT,
    product_id INT,
    quantity INT,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE products (
    id INT PRIMARY KEY,
    name VARCHAR(100)  -- Now in separate table
);
```

---

## 🔢 Third Normal Form (3NF)

### Requirements

**Definition:** Must be in 2NF, and no transitive dependencies (non-key depends on another non-key).

**Rules:**
- In 2NF
- No transitive dependencies

**Example - Before 3NF:**
```sql
-- Bad: Transitive dependency
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    department_id INT,
    department_name VARCHAR(100),  -- Depends on department_id, not directly on id
    department_location VARCHAR(100)  -- Also depends on department_id
);
-- department_name and department_location depend on department_id (transitive)
```

**Example - After 3NF:**
```sql
-- Good: No transitive dependencies
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE departments (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    location VARCHAR(100)
);
```

---

## 🔄 Denormalization

### What is Denormalization?

**Definition:** Denormalization intentionally adds redundancy to improve query performance.

**Real-life example:**
Like keeping a summary sheet - you calculate totals and keep them in a separate place for quick access, even though you could calculate them from detailed data.

**When to Denormalize:**
- Read-heavy workloads
- Complex JOINs are slow
- Reporting requirements
- Performance critical queries

**Example:**
```sql
-- Normalized (3NF)
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT,
    total DECIMAL(10, 2)  -- Calculated from order_items
);

CREATE TABLE order_items (
    order_id INT,
    product_id INT,
    quantity INT,
    price DECIMAL(10, 2)
);

-- Denormalized (for performance)
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT,
    total DECIMAL(10, 2),  -- Stored, not calculated
    item_count INT,  -- Denormalized: count of items
    last_updated TIMESTAMP
);
-- Total is stored (redundant) but faster to query
```

**Trade-offs:**
- ✅ Faster reads
- ✅ Simpler queries
- ❌ More storage
- ❌ Update complexity (must keep in sync)
- ❌ Risk of inconsistency

**Best Practices:**
- Denormalize strategically
- Use triggers to maintain consistency
- Document denormalized fields
- Consider materialized views

---

## 🔗 Database Relationships

### One-to-One (1:1)

**Definition:** One record in Table A relates to exactly one record in Table B.

**Example:**
```sql
-- User and UserProfile (1:1)
CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100)
);

CREATE TABLE user_profiles (
    user_id INT PRIMARY KEY,  -- Also foreign key
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    bio TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Use Cases:**
- Split large tables
- Optional data
- Security (separate sensitive data)

### One-to-Many (1:N)

**Definition:** One record in Table A relates to many records in Table B.

**Example:**
```sql
-- Customer and Orders (1:N)
CREATE TABLE customers (
    id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT,  -- Foreign key
    order_date DATE,
    total DECIMAL(10, 2),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

**Use Cases:**
- Most common relationship
- Parent-child relationships
- Hierarchical data

### Many-to-Many (M:N)

**Definition:** Many records in Table A relate to many records in Table B.

**Example:**
```sql
-- Students and Courses (M:N)
CREATE TABLE students (
    id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE courses (
    id INT PRIMARY KEY,
    title VARCHAR(100)
);

-- Junction table
CREATE TABLE enrollments (
    student_id INT,
    course_id INT,
    enrollment_date DATE,
    grade CHAR(1),
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);
```

**Use Cases:**
- Many-to-many relationships
- Tags, categories
- Permissions, roles

---

## 🎨 Database Design Principles

### Design Process

**1. Requirements Analysis:**
- Understand business requirements
- Identify entities and relationships
- Document constraints

**2. Conceptual Design:**
- Entity-Relationship Diagram (ERD)
- Identify entities, attributes, relationships
- Define business rules

**3. Logical Design:**
- Convert ERD to tables
- Apply normalization
- Define keys and constraints

**4. Physical Design:**
- Choose data types
- Create indexes
- Partition tables (if needed)
- Optimize for performance

### Naming Conventions

**Tables:**
- Plural nouns: `customers`, `orders`, `products`
- Descriptive: `order_items` not `items`
- Consistent: Use same pattern throughout

**Columns:**
- Singular: `name`, `email`, `order_date`
- Descriptive: `customer_id` not `cid`
- Consistent: `created_at`, `updated_at` (not `created`, `modified`)

**Keys:**
- Primary key: `id` or `table_name_id`
- Foreign key: `referenced_table_id`
- Consistent naming

### Data Types Selection

**Choose Appropriate Types:**
```sql
-- IDs: INT or BIGINT
id INT PRIMARY KEY AUTO_INCREMENT

-- Names: VARCHAR with appropriate length
name VARCHAR(100)  -- Not VARCHAR(255) if max is 50

-- Money: DECIMAL
price DECIMAL(10, 2)  -- Never FLOAT for money

-- Dates: DATE, DATETIME, TIMESTAMP
birth_date DATE
created_at DATETIME DEFAULT CURRENT_TIMESTAMP

-- Booleans: BOOLEAN or TINYINT
is_active BOOLEAN DEFAULT TRUE

-- Text: VARCHAR for short, TEXT for long
description TEXT  -- For long text
```

---

## 🔍 Interview Questions (4 Years Experience)

### Common Questions:

**1. What is normalization and why is it important?**
- Process of organizing data to reduce redundancy
- Prevents update anomalies
- Improves data integrity
- Reduces storage space

**2. Explain 1NF, 2NF, 3NF:**
- 1NF: Atomic values, no repeating groups
- 2NF: No partial dependencies
- 3NF: No transitive dependencies

**3. When would you denormalize?**
- Read-heavy workloads
- Performance critical queries
- Complex JOINs are slow
- Reporting requirements

**4. What are the types of relationships?**
- One-to-One (1:1)
- One-to-Many (1:N)
- Many-to-Many (M:N) - requires junction table

**5. How do you design a database?**
- Requirements analysis
- Conceptual design (ERD)
- Logical design (normalization)
- Physical design (indexes, data types)

**6. What's the trade-off of normalization?**
- Normalized: Less redundancy, better integrity, but more JOINs
- Denormalized: Faster queries, but redundancy and update complexity

