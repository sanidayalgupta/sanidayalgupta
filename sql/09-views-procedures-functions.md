# Views, Stored Procedures & Functions

## 👁️ Views

### What are Views?

**Definition:** Views are virtual tables based on the result of a SQL query. They don't store data, they display data from underlying tables.

**Real-life example:**
Like a window - you see a filtered/transformed view of what's inside, but the actual data remains in the original location.

**Types:**
- Simple View: Based on single table
- Complex View: Based on multiple tables, aggregations
- Materialized View: Stores results (some databases)

### Creating Views

**Basic View:**
```sql
-- Simple view
CREATE VIEW active_customers AS
SELECT id, name, email
FROM customers
WHERE status = 'active';

-- Use view like a table
SELECT * FROM active_customers;
```

**Complex View:**
```sql
-- View with JOINs and aggregations
CREATE VIEW customer_summary AS
SELECT 
    c.id,
    c.name,
    COUNT(o.id) AS order_count,
    SUM(o.total) AS total_spent,
    MAX(o.order_date) AS last_order_date
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name;

-- Query the view
SELECT * FROM customer_summary WHERE total_spent > 1000;
```

**Updatable Views:**
```sql
-- Simple updatable view
CREATE VIEW customer_emails AS
SELECT id, name, email
FROM customers;

-- Can INSERT/UPDATE/DELETE (if view is simple enough)
INSERT INTO customer_emails (name, email) VALUES ('John', 'john@example.com');
UPDATE customer_emails SET email = 'new@example.com' WHERE id = 1;
```

**View Limitations:**
- Can't always UPDATE/INSERT/DELETE (depends on complexity)
- Performance: Views execute underlying query each time
- Some databases support materialized views (store results)

---

## 🔧 Stored Procedures

### What are Stored Procedures?

**Definition:** Stored procedures are precompiled SQL code stored in the database that can be executed with parameters.

**Real-life example:**
Like a function in programming - you define it once, then call it multiple times with different parameters.

**Advantages:**
- Reusable code
- Better performance (precompiled)
- Security (can control access)
- Business logic in database

### Creating Stored Procedures

**Basic Procedure:**
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE GetCustomerOrders(IN customer_id INT)
BEGIN
    SELECT * FROM orders WHERE customer_id = customer_id;
END //
DELIMITER ;

-- Call procedure
CALL GetCustomerOrders(1);
```

**Procedure with Parameters:**
```sql
-- IN, OUT, INOUT parameters
DELIMITER //
CREATE PROCEDURE CalculateOrderTotal(
    IN order_id INT,
    OUT total DECIMAL(10, 2)
)
BEGIN
    SELECT SUM(price * quantity) INTO total
    FROM order_items
    WHERE order_id = order_id;
END //
DELIMITER ;

-- Call
CALL CalculateOrderTotal(1, @total);
SELECT @total;
```

**Procedure with Logic:**
```sql
DELIMITER //
CREATE PROCEDURE ProcessOrder(
    IN p_order_id INT,
    OUT p_status VARCHAR(20)
)
BEGIN
    DECLARE v_stock INT;
    DECLARE v_quantity INT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_status = 'ERROR';
    END;
    
    START TRANSACTION;
    
    -- Check stock
    SELECT stock INTO v_stock FROM products WHERE id = 1;
    SELECT quantity INTO v_quantity FROM order_items WHERE order_id = p_order_id;
    
    IF v_stock >= v_quantity THEN
        -- Update stock
        UPDATE products SET stock = stock - v_quantity WHERE id = 1;
        -- Update order status
        UPDATE orders SET status = 'processed' WHERE id = p_order_id;
        SET p_status = 'SUCCESS';
        COMMIT;
    ELSE
        SET p_status = 'INSUFFICIENT_STOCK';
        ROLLBACK;
    END IF;
END //
DELIMITER ;
```

**Use Cases:**
- Complex business logic
- Data validation
- Batch operations
- Security (hide implementation)

---

## ⚙️ Functions

### What are Functions?

**Definition:** Functions return a single value and can be used in SQL expressions.

**Types:**
- Scalar Functions: Return single value
- Table-Valued Functions: Return table (some databases)

### Scalar Functions

**Creating Functions:**
```sql
-- MySQL
DELIMITER //
CREATE FUNCTION CalculateDiscount(
    price DECIMAL(10, 2),
    discount_percent DECIMAL(5, 2)
)
RETURNS DECIMAL(10, 2)
DETERMINISTIC
READS SQL DATA
BEGIN
    RETURN price * (1 - discount_percent / 100);
END //
DELIMITER ;

-- Use function
SELECT 
    name,
    price,
    CalculateDiscount(price, 10) AS discounted_price
FROM products;
```

**Built-in Functions:**
```sql
-- String functions
SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM users;
SELECT UPPER(name) FROM products;
SELECT SUBSTRING(email, 1, 5) FROM users;

-- Date functions
SELECT DATE_ADD(order_date, INTERVAL 30 DAY) FROM orders;
SELECT DATEDIFF('2024-12-31', '2024-01-01') AS days;
SELECT YEAR(order_date), MONTH(order_date) FROM orders;

-- Math functions
SELECT ROUND(price, 2) FROM products;
SELECT CEIL(price), FLOOR(price) FROM products;
SELECT ABS(price - 100) AS difference FROM products;

-- Aggregate functions (covered earlier)
SELECT COUNT(*), SUM(total), AVG(total) FROM orders;
```

---

## ⚡ Triggers

### What are Triggers?

**Definition:** Triggers are procedures that automatically execute when certain events occur (INSERT, UPDATE, DELETE).

**Real-life example:**
Like an automatic response - when you insert a new order, a trigger can automatically update inventory.

**Types:**
- BEFORE: Execute before the event
- AFTER: Execute after the event
- INSTEAD OF: Replace the event (some databases)

### Creating Triggers

**BEFORE Trigger:**
```sql
-- Validate before insert
DELIMITER //
CREATE TRIGGER validate_order_before_insert
BEFORE INSERT ON orders
FOR EACH ROW
BEGIN
    IF NEW.total < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Total cannot be negative';
    END IF;
END //
DELIMITER ;
```

**AFTER Trigger:**
```sql
-- Update inventory after order
DELIMITER //
CREATE TRIGGER update_inventory_after_order
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
    UPDATE products
    SET stock = stock - NEW.quantity
    WHERE id = NEW.product_id;
END //
DELIMITER ;
```

**Audit Trigger:**
```sql
-- Log changes
DELIMITER //
CREATE TRIGGER audit_customer_changes
AFTER UPDATE ON customers
FOR EACH ROW
BEGIN
    INSERT INTO customer_audit (
        customer_id,
        old_email,
        new_email,
        changed_at
    ) VALUES (
        NEW.id,
        OLD.email,
        NEW.email,
        NOW()
    );
END //
DELIMITER ;
```

**Use Cases:**
- Data validation
- Automatic calculations
- Audit logging
- Maintaining denormalized data
- Enforcing business rules

**Best Practices:**
- Keep triggers simple
- Avoid triggers that call other triggers
- Document trigger behavior
- Test thoroughly

---

## 🎯 Use Cases & Efficiency

### When to Use Views

**Use Views For:**
- Simplifying complex queries
- Security (hide sensitive columns)
- Consistent business logic
- Reporting

**Example:**
```sql
-- Complex query as view
CREATE VIEW monthly_sales_report AS
SELECT 
    YEAR(order_date) AS year,
    MONTH(order_date) AS month,
    COUNT(*) AS order_count,
    SUM(total) AS total_sales,
    AVG(total) AS avg_order_value
FROM orders
GROUP BY YEAR(order_date), MONTH(order_date);

-- Simple query
SELECT * FROM monthly_sales_report WHERE year = 2024;
```

### When to Use Stored Procedures

**Use Procedures For:**
- Complex business logic
- Batch operations
- Security (control access)
- Performance (precompiled)

**Example:**
```sql
-- Batch processing
CREATE PROCEDURE ProcessDailyOrders()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_order_id INT;
    DECLARE cur CURSOR FOR SELECT id FROM orders WHERE status = 'pending';
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN cur;
    read_loop: LOOP
        FETCH cur INTO v_order_id;
        IF done THEN LEAVE read_loop; END IF;
        
        -- Process each order
        CALL ProcessOrder(v_order_id, @status);
    END LOOP;
    CLOSE cur;
END;
```

### Performance Considerations

**Views:**
- Execute underlying query each time
- No performance benefit (just convenience)
- Consider materialized views for expensive queries

**Stored Procedures:**
- Precompiled (faster)
- Reduce network traffic
- Can cache execution plans

**Triggers:**
- Add overhead to INSERT/UPDATE/DELETE
- Keep triggers fast
- Avoid complex logic in triggers

---

## 🔍 Interview Questions (4 Years Experience)

### Common Questions:

**1. What's the difference between a view and a table?**
- View: Virtual table, no data storage, executes query each time
- Table: Physical storage, stores data
- Views are for convenience and security

**2. When would you use a stored procedure vs a function?**
- Procedure: Multiple operations, no return value, can have side effects
- Function: Returns single value, used in expressions
- Use procedures for complex operations, functions for calculations

**3. What are triggers used for?**
- Automatic data validation
- Maintaining denormalized data
- Audit logging
- Enforcing business rules

**4. Can you update a view?**
- Depends on view complexity
- Simple views (single table, no aggregations) can be updated
- Complex views usually cannot be updated

**5. What's the performance impact of triggers?**
- Triggers add overhead to DML operations
- Keep triggers simple and fast
- Avoid triggers that call other triggers

**6. How do you handle errors in stored procedures?**
- Use DECLARE HANDLER
- Rollback transactions on error
- Return error codes/messages
- Log errors appropriately

