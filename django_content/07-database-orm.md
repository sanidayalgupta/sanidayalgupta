# Database & ORM

## 🗄️ ORM Queries in APIs

### Basic ORM Queries

**Definition:** Django ORM (Object-Relational Mapping) lets you query the database using Python code instead of SQL.

**Real-life example:**
Like asking questions in plain language instead of database language.

**Basic Queries:**
```python
# .objects: Manager instance (provides database access methods)
# .all(): Returns QuerySet containing all objects (lazy - not executed until evaluated)
# Lazy evaluation: SQL not executed until you iterate or call list()
students = Student.objects.all()
# SQL equivalent: SELECT * FROM students;
# Alternative: Student.objects.filter() (more specific)
# Difference: all() gets everything, filter() gets subset

# .get(): Returns single object (raises DoesNotExist if not found, MultipleObjectsReturned if multiple)
# Use when you expect exactly one result
# Alternative: .filter().first() (returns None if not found, doesn't raise exception)
student = Student.objects.get(id=1)
# SQL equivalent: SELECT * FROM students WHERE id = 1;
# Difference: get() raises exception, filter().first() returns None

# .filter(): Returns QuerySet matching conditions (lazy)
# age__gt: Field lookup (greater than) - double underscore syntax
# Lookups: gt (>), gte (>=), lt (<), lte (<=), exact (=), iexact (case-insensitive)
students = Student.objects.filter(age__gt=18)  # age > 18
# SQL equivalent: SELECT * FROM students WHERE age > 18;
# Alternative: .exclude() (opposite condition)
# Difference: filter() includes matches, exclude() excludes matches

# .exclude(): Returns QuerySet NOT matching conditions
students = Student.objects.exclude(active=False)
# SQL equivalent: SELECT * FROM students WHERE NOT (active = False);
# Alternative: .filter(active=True) (same result in this case)
# Difference: exclude() is explicit negation, filter() is inclusion

# .order_by(): Orders QuerySet by field(s)
# '-' prefix: Descending order (newest first)
# Without '-': Ascending order (oldest first)
students = Student.objects.order_by('-created_at')  # newest first
# SQL equivalent: SELECT * FROM students ORDER BY created_at DESC;
# Alternative: .order_by('created_at') (ascending)
# Multiple fields: .order_by('grade', '-created_at') (order by grade, then by created_at desc)

# Slicing: Limits QuerySet results
# [:10]: First 10 results (Python list slicing syntax)
# Lazy: SQL includes LIMIT clause
students = Student.objects.all()[:10]  # First 10
# SQL equivalent: SELECT * FROM students LIMIT 10;
# Alternative: .order_by('id')[:10] (with ordering)
# Difference: Slicing is efficient (SQL LIMIT), converting to list loads all
```

### select_related()

**Definition:** `select_related()` performs SQL JOIN to fetch related ForeignKey/OneToOne objects in a single query.

**Real-life example:**
Like getting the book AND its author in one trip instead of two.

**Example:**
```python
# Without select_related (N+1 problem)
books = Book.objects.all()  # 1 query
for book in books:
    print(book.author.name)  # 1 query per book = N queries
# Total: 1 + N queries

# With select_related (efficient)
books = Book.objects.select_related('author').all()  # 1 query with JOIN
for book in books:
    print(book.author.name)  # No additional queries
# Total: 1 query

# In ViewSet
class BookViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Book.objects.select_related('author', 'publisher').all()
```

**When to use:**
- ForeignKey relationships
- OneToOne relationships
- When you know you'll access the related object

### prefetch_related()

**Definition:** `prefetch_related()` performs separate queries but optimizes ManyToMany and reverse ForeignKey relationships.

**Real-life example:**
Like getting all books and their tags in 2 optimized queries instead of N+1 queries.

**Example:**
```python
# Without prefetch_related (N+1 problem)
books = Book.objects.all()  # 1 query
for book in books:
    print(book.tags.all())  # 1 query per book = N queries
# Total: 1 + N queries

# With prefetch_related (efficient)
books = Book.objects.prefetch_related('tags').all()  # 2 queries
for book in books:
    print(book.tags.all())  # Uses cached data, no queries
# Total: 2 queries

# In ViewSet
class BookViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Book.objects.prefetch_related('tags', 'reviews').all()
```

**When to use:**
- ManyToMany relationships
- Reverse ForeignKey relationships (related_name)
- When you need to access multiple related objects

### Combining select_related and prefetch_related

**Example:**
```python
# Book has author (ForeignKey) and tags (ManyToMany)
books = Book.objects.select_related('author').prefetch_related('tags').all()

# In ViewSet
class BookViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Book.objects.select_related(
            'author',
            'publisher'
        ).prefetch_related(
            'tags',
            'reviews',
            'reviews__user'  # Nested prefetch
        ).all()
```

### N+1 Query Problems

**Definition:** N+1 query problem occurs when you make 1 query to get objects, then N additional queries to get related data.

**Real-life example:**
Like going to the store 100 times for 100 items instead of getting them all in one trip.

**Problem Example:**
```python
# BAD: N+1 queries
books = Book.objects.all()  # 1 query
for book in books:  # 100 books
    print(book.author.name)  # 1 query per book = 100 queries
# Total: 101 queries!

# GOOD: Optimized
books = Book.objects.select_related('author').all()  # 1 query with JOIN
for book in books:
    print(book.author.name)  # No additional queries
# Total: 1 query
```

**Identifying N+1 Problems:**
```python
# Enable query logging in settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
        },
    },
}

# Or use django-debug-toolbar
```

### Query Optimization

**Definition:** Query optimization improves performance by reducing database queries and using efficient queries.

**Optimization Techniques:**

1. **Use select_related for ForeignKey**
```python
# Instead of
books = Book.objects.all()

# Use
books = Book.objects.select_related('author').all()
```

2. **Use prefetch_related for ManyToMany**
```python
# Instead of
books = Book.objects.all()

# Use
books = Book.objects.prefetch_related('tags').all()
```

3. **Use only() to limit fields**
```python
# Only fetch needed fields
students = Student.objects.only('name', 'email').all()
```

4. **Use defer() to exclude heavy fields**
```python
# Exclude heavy fields
students = Student.objects.defer('biography').all()
```

5. **Use values() for dictionaries**
```python
# Return dictionaries instead of objects
students = Student.objects.values('name', 'email').all()
```

6. **Use count() efficiently**
```python
# Instead of len(queryset)
count = Student.objects.count()  # Single COUNT query
```

7. **Use exists() to check existence**
```python
# Instead of bool(queryset)
if Student.objects.filter(email=email).exists():  # Single EXISTS query
    pass
```

### Atomic Transactions

**Definition:** Atomic transactions ensure all database operations succeed or all fail together.

**Real-life example:**
Like transferring money - both accounts must update or neither does.

### @transaction.atomic

**Definition:** `@transaction.atomic` decorator ensures database operations are atomic (all succeed or all fail).

**Example:**
```python
from django.db import transaction

@transaction.atomic
def transfer_money(from_account, to_account, amount):
    from_account.balance -= amount
    from_account.save()
    
    to_account.balance += amount
    to_account.save()
    # If anything fails, both changes are rolled back

# Or as context manager
def transfer_money(from_account, to_account, amount):
    with transaction.atomic():
        from_account.balance -= amount
        from_account.save()
        
        to_account.balance += amount
        to_account.save()
```

**In API Views:**
```python
from django.db import transaction

class OrderViewSet(viewsets.ModelViewSet):
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # All database operations here are atomic
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        # If anything fails, everything rolls back
        return Response(serializer.data, status=201)
```

**Real Project Example:**
```python
class PaymentViewSet(viewsets.ModelViewSet):
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create payment
        payment = serializer.save()
        
        # Update order status
        payment.order.status = 'paid'
        payment.order.save()
        
        # Create transaction record
        Transaction.objects.create(
            payment=payment,
            amount=payment.amount
        )
        
        # If any step fails, everything rolls back
        return Response(serializer.data, status=201)
```

### Multi-Database Support

**Definition:** Multi-database support allows using multiple databases in the same Django project.

**Real-life example:**
Like having separate filing cabinets for different types of documents.

**Setup:**
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'primary_db',
        ...
    },
    'read_replica': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'replica_db',
        ...
    },
    'analytics': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'analytics_db',
        ...
    }
}
```

**Using Multiple Databases:**
```python
# Specify database in queries
Book.objects.using('read_replica').all()
Student.objects.using('analytics').create(name='John')

# In serializers
def create(self, validated_data):
    return Student.objects.using('analytics').create(**validated_data)
```

**Database Router:**
```python
# database_router.py
class DatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'analytics':
            return 'analytics'
        return 'read_replica'  # Use replica for reads
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'analytics':
            return 'analytics'
        return 'default'  # Use primary for writes

# settings.py
DATABASE_ROUTERS = ['myapp.database_router.DatabaseRouter']
```

**In DRF:**
```python
class AnalyticsViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        # Use analytics database
        return AnalyticsEvent.objects.using('analytics').all()
```

---

## 🎓 Advanced Interview Topics (4+ Years Experience)

### Advanced Query Optimization

**1. Using `select_for_update()` for Locking:**
```python
# Pessimistic locking - prevents concurrent modifications
from django.db import transaction

@transaction.atomic
def update_student_balance(student_id, amount):
    # Lock row until transaction completes
    student = Student.objects.select_for_update().get(id=student_id)
    student.balance += amount
    student.save()
    # Other transactions wait until this completes
```

**2. Bulk Operations:**
```python
# Bulk create (more efficient than loop)
students = [Student(name=f'Student {i}') for i in range(1000)]
Student.objects.bulk_create(students)  # Single INSERT with multiple VALUES

# Bulk update (more efficient than loop)
Student.objects.filter(grade='A').update(status='honor_roll')

# Bulk update with different values
students = Student.objects.filter(grade='A')
for student in students:
    student.status = 'honor_roll'
Student.objects.bulk_update(students, ['status'])  # Single UPDATE
```

**3. Raw SQL When Needed:**
```python
# Use raw SQL for complex queries
from django.db import connection

def complex_analytics():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                DATE(created_at) as date,
                COUNT(*) as count,
                AVG(score) as avg_score
            FROM students
            WHERE created_at > %s
            GROUP BY DATE(created_at)
            ORDER BY date DESC
        """, [timezone.now() - timedelta(days=30)])
        
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
```

### Database Indexing Strategies

**1. Model Indexes:**
```python
class Student(models.Model):
    name = models.CharField(max_length=100, db_index=True)  # Single field index
    email = models.EmailField(unique=True)  # Unique index
    age = models.IntegerField()
    
    class Meta:
        # Composite index (multiple fields)
        indexes = [
            models.Index(fields=['age', 'grade']),  # For queries filtering both
            models.Index(fields=['-created_at'], name='created_at_desc'),  # Descending
        ]
        # Unique together
        unique_together = [['email', 'school']]
```

**2. Query Performance Analysis:**
```python
# Enable query logging
from django.db import connection
from django.test.utils import override_settings

# Count queries
def test_query_count():
    with override_settings(DEBUG=True):
        initial_queries = len(connection.queries)
        students = Student.objects.select_related('school').all()
        list(students)  # Force evaluation
        queries_executed = len(connection.queries) - initial_queries
        print(f"Queries executed: {queries_executed}")

# Use django-debug-toolbar for production analysis
```

### Transaction Management

**1. Nested Transactions:**
```python
from django.db import transaction

@transaction.atomic
def create_order_with_items(order_data, items_data):
    # Outer transaction
    order = Order.objects.create(**order_data)
    
    try:
        with transaction.atomic():
            # Inner transaction (savepoint)
            for item_data in items_data:
                OrderItem.objects.create(order=order, **item_data)
    except ValidationError:
        # Rollback inner transaction only
        pass
    # Outer transaction continues
```

**2. Optimistic Locking:**
```python
class Student(models.Model):
    version = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        # Check version hasn't changed
        if self.pk:
            current = Student.objects.get(pk=self.pk)
            if current.version != self.version:
                raise ValueError("Object was modified by another user")
            self.version += 1
        super().save(*args, **kwargs)
```

### Read Replicas

**1. Using Read Replicas:**
```python
# settings.py
DATABASES = {
    'default': {
        # Primary database (writes)
    },
    'read_replica': {
        # Read replica (reads)
    },
}

# Database router
class ReadReplicaRouter:
    def db_for_read(self, model, **hints):
        return 'read_replica'
    
    def db_for_write(self, model, **hints):
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        return True

# Manual selection
students = Student.objects.using('read_replica').all()  # Read from replica
student.save(using='default')  # Write to primary
```

### QuerySet Caching

**1. Understanding QuerySet Evaluation:**
```python
# QuerySet is lazy - not evaluated until:
# 1. Iteration: for student in students:
# 2. Conversion: list(students)
# 3. Slicing: students[0]
# 4. Methods: students.count(), students.exists()

queryset = Student.objects.all()  # No SQL yet
print(queryset)  # Still no SQL (just representation)
list(queryset)  # NOW SQL executes

# QuerySet is cached after first evaluation
queryset = Student.objects.all()
list(queryset)  # SQL executes
list(queryset)  # Uses cache, no SQL
```

**2. Avoiding QuerySet Re-evaluation:**
```python
# ❌ BAD: Multiple evaluations
def get_students():
    students = Student.objects.all()
    count = students.count()  # SQL query 1
    first = students.first()  # SQL query 2
    return list(students)  # SQL query 3

# ✅ GOOD: Single evaluation
def get_students():
    students = list(Student.objects.all())  # Single SQL query
    count = len(students)  # Python count
    first = students[0] if students else None
    return students
```

### Database Connection Pooling

**1. Connection Pooling:**
```python
# Use connection pooling for high-traffic APIs
# Install: pip install django-db-connection-pool

# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'dj_db_conn_pool.backends.postgresql',
        # Pool settings
        'POOL_OPTIONS': {
            'POOL_SIZE': 10,
            'MAX_OVERFLOW': 20,
        }
    }
}
```

### ORM vs Raw SQL

**When to Use ORM:**
- ✅ Standard CRUD operations
- ✅ Cross-database compatibility needed
- ✅ Model relationships
- ✅ Security (SQL injection protection)

**When to Use Raw SQL:**
- ✅ Complex aggregations
- ✅ Performance-critical queries
- ✅ Database-specific features
- ✅ Reporting/analytics queries

**Example:**
```python
# ORM (readable, secure)
students = Student.objects.filter(
    age__gte=18,
    grade__in=['A', 'B']
).select_related('school')

# Raw SQL (complex, but powerful)
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT s.*, sc.name as school_name
        FROM students s
        JOIN schools sc ON s.school_id = sc.id
        WHERE s.age >= %s AND s.grade IN %s
    """, [18, ('A', 'B')])
```

---

*This guide covers essential and advanced ORM patterns. Master these for senior Django REST Framework positions.*

