# Constraints & Keys

## 🔒 Constraints

### What are Constraints?

**Definition:** Constraints are rules enforced on data columns to ensure data integrity and accuracy.

**Real-life example:**
Like rules in a form - "Age must be 18 or older" or "Email must be unique" - constraints enforce these rules at the database level.

**Why Use Constraints?**
- Data integrity
- Prevent invalid data
- Enforce business rules
- Improve data quality

---

## 📋 Types of Constraints

### NOT NULL Constraint

**Definition:** NOT NULL ensures a column cannot have NULL values.

**Syntax:**
```sql
CREATE TABLE students (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,  -- Must have a value
    email VARCHAR(255) NOT NULL,
    age INT  -- Can be NULL
);

-- Adding NOT NULL to existing column
ALTER TABLE students 
MODIFY COLUMN name VARCHAR(100) NOT NULL;

-- Removing NOT NULL
ALTER TABLE students 
MODIFY COLUMN age INT NULL;
```

**Use Cases:**
- Required fields (name, email)
- Critical data that must exist
- Foreign key columns

**Best Practices:**
- Use for required business data
- Don't overuse (allow NULL when appropriate)
- Consider default values instead

### UNIQUE Constraint

**Definition:** UNIQUE ensures all values in a column are different.

**Syntax:**
```sql
-- Single column unique
CREATE TABLE users (
    id INT PRIMARY KEY,
    email VARCHAR(255) UNIQUE,  -- Each email must be unique
    username VARCHAR(50) UNIQUE
);

-- Multiple column unique (composite)
CREATE TABLE enrollments (
    student_id INT,
    course_id INT,
    UNIQUE(student_id, course_id)  -- Same student can't enroll twice
);

-- Adding unique constraint
ALTER TABLE users 
ADD CONSTRAINT unique_email UNIQUE (email);

-- Named unique constraint
CREATE TABLE products (
    id INT PRIMARY KEY,
    sku VARCHAR(50),
    CONSTRAINT unique_sku UNIQUE (sku)
);
```

**Use Cases:**
- Email addresses
- Usernames
- Product SKUs
- Preventing duplicate combinations

**Index Behavior:**
- UNIQUE automatically creates an index
- Improves query performance
- Enforces uniqueness efficiently

### PRIMARY KEY Constraint

**Definition:** PRIMARY KEY uniquely identifies each row and cannot be NULL.

**Syntax:**
```sql
-- Single column primary key
CREATE TABLE students (
    id INT PRIMARY KEY,
    name VARCHAR(100)
);

-- Composite primary key
CREATE TABLE order_items (
    order_id INT,
    product_id INT,
    quantity INT,
    PRIMARY KEY (order_id, product_id)  -- Combination is unique
);

-- Auto-increment primary key
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100)
);

-- Adding primary key
ALTER TABLE students 
ADD PRIMARY KEY (id);
```

**Characteristics:**
- Must be UNIQUE
- Cannot be NULL
- Only one per table
- Automatically creates index
- Used for relationships

**Best Practices:**
- Use INT or BIGINT for performance
- Use AUTO_INCREMENT for surrogate keys
- Keep primary keys simple
- Don't use business data as PK (use surrogate keys)

### FOREIGN KEY Constraint

**Definition:** FOREIGN KEY maintains referential integrity between tables.

**Syntax:**
```sql
-- Basic foreign key
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT,
    total DECIMAL(10, 2),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Named foreign key with actions
CREATE TABLE order_items (
    id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    CONSTRAINT fk_order 
        FOREIGN KEY (order_id) REFERENCES orders(id)
        ON DELETE CASCADE  -- Delete items when order deleted
        ON UPDATE CASCADE,  -- Update items when order id updated
    CONSTRAINT fk_product
        FOREIGN KEY (product_id) REFERENCES products(id)
        ON DELETE RESTRICT  -- Prevent delete if items exist
        ON UPDATE CASCADE
);

-- Adding foreign key
ALTER TABLE orders
ADD CONSTRAINT fk_customer
FOREIGN KEY (customer_id) REFERENCES customers(id)
ON DELETE SET NULL;  -- Set to NULL if customer deleted
```

**Referential Actions:**
```sql
-- CASCADE: Delete/update related rows
ON DELETE CASCADE  -- If parent deleted, delete children
ON UPDATE CASCADE  -- If parent updated, update children

-- RESTRICT/NO ACTION: Prevent delete/update if children exist
ON DELETE RESTRICT  -- Cannot delete parent if children exist
ON UPDATE RESTRICT

-- SET NULL: Set foreign key to NULL
ON DELETE SET NULL  -- Set FK to NULL if parent deleted
ON UPDATE SET NULL

-- SET DEFAULT: Set to default value
ON DELETE SET DEFAULT
ON UPDATE SET DEFAULT
```

**Use Cases:**
- Maintaining relationships
- Data integrity
- Preventing orphaned records
- Enforcing business rules

**Best Practices:**
- Always define referential actions
- Use CASCADE carefully (can delete more than expected)
- Index foreign key columns (improves JOIN performance)
- Consider soft deletes instead of CASCADE

### CHECK Constraint

**Definition:** CHECK ensures values meet specific conditions.

**Syntax:**
```sql
-- Single column check
CREATE TABLE students (
    id INT PRIMARY KEY,
    age INT CHECK (age >= 18 AND age <= 100),
    email VARCHAR(255) CHECK (email LIKE '%@%.%'),
    grade CHAR(1) CHECK (grade IN ('A', 'B', 'C', 'D', 'F'))
);

-- Multiple column check
CREATE TABLE reservations (
    id INT PRIMARY KEY,
    check_in DATE,
    check_out DATE,
    CHECK (check_out > check_in)  -- Check-out must be after check-in
);

-- Named check constraint
CREATE TABLE products (
    id INT PRIMARY KEY,
    price DECIMAL(10, 2),
    discount DECIMAL(5, 2),
    CONSTRAINT check_discount 
        CHECK (discount >= 0 AND discount <= 100)
);

-- Adding check constraint
ALTER TABLE students
ADD CONSTRAINT check_age 
CHECK (age >= 18 AND age <= 100);
```

**Use Cases:**
- Range validation (age, price)
- Format validation (email pattern)
- Business rule enforcement
- Data quality assurance

**Limitations:**
- Not all databases support CHECK (MySQL 8.0.16+)
- Can't reference other tables
- Can't use subqueries

### DEFAULT Constraint

**Definition:** DEFAULT provides a default value when no value is specified.

**Syntax:**
```sql
CREATE TABLE orders (
    id INT PRIMARY KEY,
    status VARCHAR(20) DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    total DECIMAL(10, 2) DEFAULT 0.00
);

-- Adding default
ALTER TABLE orders
ALTER COLUMN status SET DEFAULT 'pending';

-- Removing default
ALTER TABLE orders
ALTER COLUMN status DROP DEFAULT;
```

**Use Cases:**
- Default status values
- Timestamps
- Initial values
- Reducing required fields

---

## 🔑 Keys

### Primary Key

**Definition:** Primary key uniquely identifies each row in a table.

**Types:**
```sql
-- Natural Key: Business data as PK
CREATE TABLE countries (
    code CHAR(2) PRIMARY KEY,  -- 'US', 'UK'
    name VARCHAR(100)
);

-- Surrogate Key: Artificial key (recommended)
CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Artificial ID
    email VARCHAR(255) UNIQUE,  -- Business identifier
    name VARCHAR(100)
);
```

**Natural vs Surrogate Keys:**
- **Natural Key**: Uses business data (email, SSN) - can change
- **Surrogate Key**: Uses artificial ID - stable, never changes

**Best Practice:** Use surrogate keys (INT AUTO_INCREMENT) for primary keys.

### Foreign Key

**Definition:** Foreign key references primary key in another table.

**Example:**
```sql
-- Parent table
CREATE TABLE customers (
    id INT PRIMARY KEY,
    name VARCHAR(100)
);

-- Child table
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

**Self-Referencing Foreign Key:**
```sql
-- Employee table with manager (self-reference)
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    manager_id INT,
    FOREIGN KEY (manager_id) REFERENCES employees(id)
);
```

### Composite Key

**Definition:** Composite key uses multiple columns as primary key.

**Example:**
```sql
CREATE TABLE enrollments (
    student_id INT,
    course_id INT,
    enrollment_date DATE,
    PRIMARY KEY (student_id, course_id)  -- Composite primary key
);

-- Composite foreign key
CREATE TABLE order_items (
    order_id INT,
    product_id INT,
    quantity INT,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

**When to Use:**
- Many-to-many relationships
- Junction tables
- When combination is unique identifier

### Unique Key

**Definition:** Unique key ensures uniqueness but allows NULL (unlike primary key).

**Example:**
```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    email VARCHAR(255) UNIQUE,  -- Can be NULL, but if set, must be unique
    username VARCHAR(50) UNIQUE,
    phone VARCHAR(20) UNIQUE
);
```

**Primary Key vs Unique Key:**
- **Primary Key**: One per table, cannot be NULL, used for relationships
- **Unique Key**: Multiple per table, can have NULL, not used for relationships

---

## 🎯 Use Cases & Efficiency

### Constraint Design Patterns

**1. Data Integrity:**
```sql
-- Ensure valid data
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    total DECIMAL(10, 2) CHECK (total >= 0),
    status VARCHAR(20) DEFAULT 'pending' 
        CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE RESTRICT
);
```

**2. Preventing Orphans:**
```sql
-- Foreign key prevents orphaned records
CREATE TABLE order_items (
    id INT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
);
-- Cannot delete product if used in orders
-- Order items deleted when order deleted
```

**3. Business Rules:**
```sql
-- Enforce business logic at database level
CREATE TABLE reservations (
    id INT PRIMARY KEY,
    room_id INT NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    guest_count INT CHECK (guest_count > 0 AND guest_count <= 4),
    CHECK (check_out > check_in),  -- Business rule
    FOREIGN KEY (room_id) REFERENCES rooms(id)
);
```

### Performance Considerations

**1. Index Creation:**
```sql
-- Primary keys automatically indexed
-- Foreign keys should be indexed
CREATE INDEX idx_order_customer ON orders(customer_id);
-- Improves JOIN performance
```

**2. Constraint Overhead:**
```sql
-- Constraints add overhead but ensure data quality
-- Worth the performance cost for data integrity
-- Can disable temporarily for bulk imports:
SET FOREIGN_KEY_CHECKS = 0;
-- Bulk insert operations
SET FOREIGN_KEY_CHECKS = 1;
```

**3. Cascade Operations:**
```sql
-- CASCADE can be expensive
-- Use carefully, test thoroughly
-- Consider soft deletes instead:
CREATE TABLE orders (
    id INT PRIMARY KEY,
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at DATETIME
);
-- Instead of ON DELETE CASCADE
```

---

## 🔍 Interview Questions (4 Years Experience)

### Common Questions:

**1. What's the difference between PRIMARY KEY and UNIQUE KEY?**
- PRIMARY KEY: One per table, cannot be NULL, used for relationships
- UNIQUE KEY: Multiple per table, can have NULL, creates index but not used for relationships

**2. When would you use a composite primary key?**
- Junction tables (many-to-many relationships)
- When combination of columns uniquely identifies a row
- Example: enrollments (student_id, course_id)

**3. What are the referential actions for foreign keys?**
- CASCADE: Delete/update related rows
- RESTRICT: Prevent if children exist
- SET NULL: Set FK to NULL
- SET DEFAULT: Set to default value
- NO ACTION: Similar to RESTRICT

**4. Should you use natural or surrogate keys?**
- **Surrogate keys** (recommended): Stable, simple, never change
- **Natural keys**: Can change, complex, but meaningful
- Best practice: Surrogate PK + Unique constraint on natural key

**5. How do you handle foreign keys in a distributed system?**
- Consider eventual consistency
- May need to relax foreign key constraints
- Use application-level validation
- Consider eventual consistency patterns

**6. What's the performance impact of constraints?**
- Constraints add overhead but ensure integrity
- Indexes on foreign keys improve JOIN performance
- CHECK constraints evaluated on every insert/update
- Worth the cost for data quality

