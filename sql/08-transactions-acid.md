# Transactions & ACID Properties

## 💼 Transactions

### What are Transactions?

**Definition:** Transactions are sequences of database operations that are executed as a single unit - all succeed or all fail.

**Real-life example:**
Like transferring money between bank accounts - both accounts must update (debit one, credit other) or neither does. You can't have one succeed and one fail.

**Transaction Properties:**
- **Atomicity**: All or nothing
- **Consistency**: Database remains valid
- **Isolation**: Concurrent transactions don't interfere
- **Durability**: Committed changes persist

---

## 🔄 Transaction Control

### BEGIN / START TRANSACTION

**Definition:** Starts a new transaction.

```sql
-- Start transaction
BEGIN;
-- or
START TRANSACTION;

-- Operations
INSERT INTO accounts (id, balance) VALUES (1, 1000);
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- Commit or Rollback
COMMIT;  -- Save changes
-- or
ROLLBACK;  -- Undo changes
```

### COMMIT

**Definition:** Saves all changes made in the transaction.

```sql
BEGIN;
INSERT INTO orders (customer_id, total) VALUES (1, 100.00);
INSERT INTO order_items (order_id, product_id, quantity) VALUES (LAST_INSERT_ID(), 1, 2);
COMMIT;  -- All changes are now permanent
```

### ROLLBACK

**Definition:** Undoes all changes made in the transaction.

```sql
BEGIN;
UPDATE accounts SET balance = balance - 1000 WHERE id = 1;
-- Oops, wrong account!
ROLLBACK;  -- Undo the change
```

### SAVEPOINT

**Definition:** Creates a point within a transaction to which you can roll back.

```sql
BEGIN;
INSERT INTO orders (customer_id, total) VALUES (1, 100.00);
SAVEPOINT after_order;

INSERT INTO order_items (order_id, product_id, quantity) VALUES (LAST_INSERT_ID(), 1, 2);
-- If this fails, rollback to savepoint
ROLLBACK TO SAVEPOINT after_order;

COMMIT;
```

---

## 🛡️ ACID Properties

### Atomicity

**Definition:** All operations in a transaction succeed or all fail.

**Example:**
```sql
BEGIN;
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
    UPDATE accounts SET balance = balance + 100 WHERE id = 2;
    -- If second update fails, first is also rolled back
COMMIT;
```

**Implementation:**
- Database logs all changes
- On failure, uses log to undo changes
- Ensures all-or-nothing execution

### Consistency

**Definition:** Database remains in a valid state before and after transaction.

**Example:**
```sql
-- Constraint: balance >= 0
BEGIN;
    UPDATE accounts SET balance = balance - 1000 WHERE id = 1;
    -- If balance becomes negative, transaction fails
    -- Database remains consistent
COMMIT;
```

**Enforced By:**
- Constraints (CHECK, FOREIGN KEY, etc.)
- Triggers
- Application logic

### Isolation

**Definition:** Concurrent transactions don't interfere with each other.

**Isolation Levels:**
```sql
-- Set isolation level
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```

**Isolation Levels Explained:**

**1. READ UNCOMMITTED (Lowest):**
- Can read uncommitted changes
- Dirty reads possible
- Fastest but least safe

**2. READ COMMITTED:**
- Only read committed changes
- No dirty reads
- Non-repeatable reads possible
- Default in PostgreSQL, SQL Server

**3. REPEATABLE READ:**
- Same read returns same result
- No dirty reads, no non-repeatable reads
- Phantom reads possible
- Default in MySQL

**4. SERIALIZABLE (Highest):**
- Transactions execute serially
- No concurrency issues
- Slowest but safest

**Problems Solved:**

**Dirty Read:**
```sql
-- Transaction 1
BEGIN;
UPDATE accounts SET balance = 1000 WHERE id = 1;
-- Not committed yet

-- Transaction 2 (READ UNCOMMITTED)
SELECT balance FROM accounts WHERE id = 1;  -- Sees 1000 (dirty read)
-- Transaction 1 rolls back
-- Transaction 2 saw data that never existed!
```

**Non-Repeatable Read:**
```sql
-- Transaction 1
SELECT balance FROM accounts WHERE id = 1;  -- Returns 500

-- Transaction 2
UPDATE accounts SET balance = 1000 WHERE id = 1;
COMMIT;

-- Transaction 1
SELECT balance FROM accounts WHERE id = 1;  -- Returns 1000 (different!)
```

**Phantom Read:**
```sql
-- Transaction 1
SELECT * FROM orders WHERE total > 100;  -- Returns 5 rows

-- Transaction 2
INSERT INTO orders (total) VALUES (200);
COMMIT;

-- Transaction 1
SELECT * FROM orders WHERE total > 100;  -- Returns 6 rows (phantom!)
```

### Durability

**Definition:** Committed changes persist even after system failure.

**Implementation:**
- Write-Ahead Logging (WAL)
- Changes written to log before commit
- Log persisted to disk
- On recovery, log is replayed

---

## 🔒 Locks & Concurrency

### What are Locks?

**Definition:** Locks prevent concurrent access to the same data.

**Types of Locks:**

**1. Shared Lock (Read Lock):**
```sql
-- Multiple transactions can read
-- No transaction can write
SELECT * FROM accounts WHERE id = 1 LOCK IN SHARE MODE;
```

**2. Exclusive Lock (Write Lock):**
```sql
-- Only one transaction can write
-- No other transaction can read or write
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;
```

**3. Table Locks:**
```sql
-- Lock entire table
LOCK TABLES accounts WRITE;
-- Do operations
UNLOCK TABLES;
```

### Deadlocks

**Definition:** Two transactions waiting for each other's locks.

**Example:**
```sql
-- Transaction 1
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- Locks account 1
UPDATE accounts SET balance = balance + 100 WHERE id = 2;  -- Waits for lock on account 2

-- Transaction 2 (concurrent)
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 2;  -- Locks account 2
UPDATE accounts SET balance = balance + 100 WHERE id = 1;  -- Waits for lock on account 1

-- Deadlock! Both waiting for each other
```

**Prevention:**
- Always lock resources in same order
- Use timeouts
- Keep transactions short
- Database automatically detects and rolls back one transaction

---

## 🎯 Transaction Best Practices

### Keep Transactions Short

```sql
-- Bad: Long transaction
BEGIN;
    -- Many operations
    -- Holds locks for long time
    -- Blocks other transactions
COMMIT;

-- Good: Short transaction
BEGIN;
    -- Only necessary operations
    -- Release locks quickly
COMMIT;
```

### Handle Errors

```sql
-- Proper error handling
BEGIN;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    -- Operations
    INSERT INTO orders ...;
    UPDATE inventory ...;
    
COMMIT;
```

### Use Appropriate Isolation Level

```sql
-- Use lowest isolation level that meets requirements
-- READ COMMITTED is usually sufficient
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

### Avoid Long-Running Transactions

```sql
-- Bad: Transaction with user interaction
BEGIN;
    INSERT INTO order ...;
    -- Wait for user input (BAD!)
    -- Transaction holds locks
COMMIT;

-- Good: Complete transaction quickly
BEGIN;
    INSERT INTO order ...;
COMMIT;
-- Then wait for user input
```

---

## 🔍 Interview Questions (4 Years Experience)

### Common Questions:

**1. What are ACID properties?**
- **Atomicity**: All or nothing
- **Consistency**: Database remains valid
- **Isolation**: Concurrent transactions don't interfere
- **Durability**: Committed changes persist

**2. What's the difference between isolation levels?**
- READ UNCOMMITTED: Can see uncommitted changes
- READ COMMITTED: Only committed changes
- REPEATABLE READ: Same read returns same result
- SERIALIZABLE: Serial execution

**3. What's a deadlock?**
- Two transactions waiting for each other's locks
- Database detects and rolls back one
- Prevent by locking resources in same order

**4. When would you use SAVEPOINT?**
- Partial rollback within transaction
- Complex transactions with multiple steps
- Error recovery scenarios

**5. How do you handle transaction errors?**
- Use error handlers
- Rollback on error
- Log errors
- Retry logic for transient errors

**6. What's the trade-off of higher isolation levels?**
- Higher isolation = better consistency
- Higher isolation = lower concurrency
- Higher isolation = slower performance
- Choose appropriate level for use case

