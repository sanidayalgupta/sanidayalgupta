# ORM Concepts & Migrations

## 🔄 ORM Concepts

### What is ORM?

**Definition:** ORM (Object-Relational Mapping) is a technique that lets you interact with databases using object-oriented programming instead of SQL.

**Real-life example:**
Like a translator - you speak in Python objects, ORM translates to SQL, talks to database, then translates results back to Python objects.

**Advantages:**
- Write code in your programming language
- Database-agnostic (mostly)
- Type safety
- Less SQL to write

**Disadvantages:**
- Performance overhead
- Less control over SQL
- Learning curve
- Can generate inefficient queries

### ORM vs Raw SQL

**ORM Example (Django):**
```python
# ORM: Python code
students = Student.objects.filter(age__gt=18).order_by('name')

# Generated SQL:
# SELECT * FROM students WHERE age > 18 ORDER BY name
```

**Raw SQL Example:**
```python
# Raw SQL: Direct control
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM students WHERE age > %s ORDER BY name", [18])
    students = cursor.fetchall()
```

**When to Use Each:**
- **ORM**: Most cases, simpler code, database-agnostic
- **Raw SQL**: Complex queries, performance critical, database-specific features

### Common ORM Patterns

**1. Active Record Pattern:**
```python
# Model contains both data and behavior
class Student(models.Model):
    name = models.CharField(max_length=100)
    
    def get_full_name(self):
        return self.name

# Usage
student = Student.objects.get(id=1)
print(student.get_full_name())
```

**2. Data Mapper Pattern:**
```python
# Separate data and behavior
# Less common in Django, more in SQLAlchemy
```

**3. Query Builder:**
```python
# Build queries programmatically
query = Student.objects.all()
if age_filter:
    query = query.filter(age=age_filter)
if order_by:
    query = query.order_by(order_by)
results = query
```

### ORM Query Optimization

**1. select_related (JOIN):**
```python
# Fetches related object in same query
students = Student.objects.select_related('school')
# SQL: SELECT ... FROM students JOIN schools ON ...
```

**2. prefetch_related (Separate Query):**
```python
# Fetches related objects efficiently
students = Student.objects.prefetch_related('courses')
# SQL: Two queries, but optimized
```

**3. only() and defer():**
```python
# Only fetch needed columns
students = Student.objects.only('name', 'email')
# SQL: SELECT name, email FROM students

# Defer heavy columns
students = Student.objects.defer('biography')
# SQL: SELECT all columns EXCEPT biography
```

**4. values() and values_list():**
```python
# Return dictionaries
students = Student.objects.values('name', 'email')
# Returns: [{'name': 'John', 'email': 'john@example.com'}, ...]

# Return tuples
students = Student.objects.values_list('name', flat=True)
# Returns: ['John', 'Jane', ...]
```

---

## 🔄 Migrations

### What are Migrations?

**Definition:** Migrations are version control for database schema - they track and apply changes to database structure.

**Real-life example:**
Like Git for databases - you track changes, can apply them, and rollback if needed.

**Why Migrations?**
- Version control for schema
- Reproducible deployments
- Team collaboration
- Rollback capability

### Creating Migrations

**Django Example:**
```python
# 1. Create model
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

# 2. Generate migration
python manage.py makemigrations

# 3. Apply migration
python manage.py migrate
```

**Migration File:**
```python
# Generated migration
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('app', '0001_initial'),
    ]
    
    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
```

### Migration Operations

**Common Operations:**
```python
# Create table
migrations.CreateModel(...)

# Add field
migrations.AddField(
    model_name='student',
    name='age',
    field=models.IntegerField(null=True),
)

# Remove field
migrations.RemoveField(
    model_name='student',
    name='age',
)

# Alter field
migrations.AlterField(
    model_name='student',
    name='email',
    field=models.EmailField(max_length=255),
)

# Add index
migrations.AddIndex(
    model_name='student',
    index=models.Index(fields=['email'], name='student_email_idx'),
)

# Create foreign key
migrations.AddField(
    model_name='student',
    name='school',
    field=models.ForeignKey(
        on_delete=models.CASCADE,
        to='app.School',
    ),
)
```

### Data Migrations

**Definition:** Data migrations modify data, not just schema.

```python
def migrate_student_data(apps, schema_editor):
    Student = apps.get_model('app', 'Student')
    for student in Student.objects.all():
        student.email = student.email.lower()
        student.save()

class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(migrate_student_data),
    ]
```

### Migration Best Practices

**1. Keep Migrations Small:**
- One logical change per migration
- Easier to review and debug
- Safer rollbacks

**2. Test Migrations:**
- Test on development first
- Test rollback procedures
- Test with production-like data

**3. Never Edit Applied Migrations:**
- Create new migration instead
- Editing can break other environments
- Migrations are historical record

**4. Handle Production Carefully:**
- Backup before migration
- Test on staging first
- Have rollback plan
- Consider downtime for large migrations

---

## 🔍 Interview Questions (4 Years Experience)

### Common Questions:

**1. What is ORM and what are its advantages/disadvantages?**
- Object-Relational Mapping
- Advantages: Less SQL, database-agnostic, type safety
- Disadvantages: Performance overhead, less control

**2. When would you use raw SQL instead of ORM?**
- Complex queries
- Performance critical operations
- Database-specific features
- Bulk operations

**3. What are migrations and why are they important?**
- Version control for database schema
- Reproducible deployments
- Team collaboration
- Rollback capability

**4. How do you optimize ORM queries?**
- Use select_related for foreign keys
- Use prefetch_related for many-to-many
- Use only() and defer() for column selection
- Avoid N+1 queries

**5. What's the N+1 query problem?**
- 1 query for list, N queries for related data
- Solution: Use select_related or prefetch_related
- Example: Get all orders, then get customer for each order

**6. How do you handle database schema changes in production?**
- Use migrations
- Test thoroughly
- Backup first
- Plan for downtime if needed
- Have rollback strategy

