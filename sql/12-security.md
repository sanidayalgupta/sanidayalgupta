# SQL Security

## 🔒 SQL Security

### What is SQL Security?

**Definition:** SQL security protects databases from unauthorized access and malicious attacks.

**Real-life example:**
Like a bank vault - you need proper authorization, and the system prevents unauthorized access and tampering.

**Key Areas:**
- Authentication
- Authorization
- SQL Injection prevention
- Data encryption
- Audit logging

---

## 💉 SQL Injection

### What is SQL Injection?

**Definition:** SQL Injection is a code injection technique where malicious SQL is inserted into queries.

**Real-life example:**
Like someone adding extra instructions to your order - instead of just ordering a pizza, they add "and also give me all customer data".

**How It Works:**
```sql
-- Vulnerable code (DON'T DO THIS!)
-- User input: "'; DROP TABLE users; --"
SELECT * FROM users WHERE username = ''; DROP TABLE users; --'
-- This executes DROP TABLE!
```

### Prevention Methods

**1. Parameterized Queries (Prepared Statements):**
```python
# Python example
# Bad: String concatenation
query = f"SELECT * FROM users WHERE username = '{username}'"

# Good: Parameterized query
query = "SELECT * FROM users WHERE username = %s"
cursor.execute(query, (username,))
```

**2. Input Validation:**
```sql
-- Validate input format
-- Only allow alphanumeric for usernames
-- Reject special SQL characters
```

**3. Least Privilege:**
```sql
-- Don't use admin/root user for application
-- Create user with minimal permissions
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'password';
GRANT SELECT, INSERT, UPDATE ON myapp.* TO 'app_user'@'localhost';
-- No DROP, ALTER, etc.
```

**4. Escaping:**
```sql
-- Escape special characters
-- Use database-specific escaping functions
-- But parameterized queries are better
```

### Examples

**Vulnerable Query:**
```sql
-- DON'T DO THIS!
SELECT * FROM users WHERE username = '$username' AND password = '$password';
-- If username = "admin' OR '1'='1"
-- Query becomes: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
-- This returns all users!
```

**Safe Query:**
```sql
-- Use parameterized queries
SELECT * FROM users WHERE username = ? AND password = ?;
-- Parameters are properly escaped
```

---

## 🔐 Database Security Best Practices

### User Management

**Create Application Users:**
```sql
-- Create user for application
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'strong_password';

-- Grant minimal permissions
GRANT SELECT, INSERT, UPDATE ON myapp.orders TO 'app_user'@'localhost';
GRANT SELECT ON myapp.products TO 'app_user'@'localhost';
-- No DELETE, DROP, ALTER permissions

-- Revoke unnecessary permissions
REVOKE ALL PRIVILEGES ON *.* FROM 'app_user'@'localhost';
```

**Role-Based Access:**
```sql
-- Create roles
CREATE ROLE 'readonly';
CREATE ROLE 'readwrite';

-- Grant permissions to roles
GRANT SELECT ON myapp.* TO 'readonly';
GRANT SELECT, INSERT, UPDATE ON myapp.* TO 'readwrite';

-- Assign roles to users
GRANT 'readonly' TO 'report_user'@'localhost';
GRANT 'readwrite' TO 'app_user'@'localhost';
```

### Data Encryption

**Encryption at Rest:**
```sql
-- Enable encryption (database-specific)
-- MySQL: Use encrypted tablespaces
-- PostgreSQL: Use encrypted filesystem or pgcrypto
-- SQL Server: Transparent Data Encryption (TDE)
```

**Encryption in Transit:**
```sql
-- Use SSL/TLS for connections
-- MySQL: REQUIRE SSL
ALTER USER 'app_user'@'localhost' REQUIRE SSL;

-- Use encrypted connections in application
-- Connection string: mysql://user:pass@host/db?ssl=true
```

**Column-Level Encryption:**
```sql
-- Encrypt sensitive columns
-- Use application-level encryption
-- Or database encryption functions (varies by database)
```

### Audit Logging

**Enable Audit Logs:**
```sql
-- Log all database access
-- Track who accessed what data
-- Monitor for suspicious activity

-- Create audit table
CREATE TABLE audit_log (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_name VARCHAR(100),
    action VARCHAR(50),
    table_name VARCHAR(100),
    record_id INT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Use triggers to log changes
CREATE TRIGGER audit_customer_changes
AFTER UPDATE ON customers
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (user_name, action, table_name, record_id)
    VALUES (USER(), 'UPDATE', 'customers', NEW.id);
END;
```

---

## 🛡️ Security Checklist

### Application Level

**✅ Use Parameterized Queries:**
- Never concatenate user input into SQL
- Always use prepared statements
- Validate and sanitize input

**✅ Least Privilege:**
- Application user has minimal permissions
- Separate read and write users
- No admin privileges

**✅ Input Validation:**
- Validate data types
- Check ranges
- Reject suspicious patterns

**✅ Error Handling:**
- Don't expose database errors to users
- Log errors securely
- Return generic error messages

### Database Level

**✅ Strong Passwords:**
- Complex passwords
- Regular rotation
- No default passwords

**✅ Network Security:**
- Restrict database access
- Use firewalls
- Enable SSL/TLS

**✅ Regular Updates:**
- Keep database updated
- Apply security patches
- Monitor security advisories

**✅ Backup Security:**
- Encrypt backups
- Secure backup storage
- Test restore procedures

---

## 🔍 Interview Questions (4 Years Experience)

### Common Questions:

**1. What is SQL Injection and how do you prevent it?**
- Code injection attack
- Prevent with parameterized queries
- Input validation
- Least privilege

**2. What's the difference between authentication and authorization?**
- Authentication: Who you are (login)
- Authorization: What you can do (permissions)
- Both are needed for security

**3. How do you secure sensitive data?**
- Encryption at rest
- Encryption in transit
- Column-level encryption
- Access controls

**4. What is least privilege principle?**
- Users have minimum permissions needed
- Reduces attack surface
- Limits damage if compromised

**5. How do you audit database access?**
- Enable audit logging
- Track user actions
- Monitor for suspicious activity
- Regular review of logs

**6. What are parameterized queries?**
- Queries with placeholders for parameters
- Parameters are escaped automatically
- Prevents SQL injection
- Better performance (query plan cached)

