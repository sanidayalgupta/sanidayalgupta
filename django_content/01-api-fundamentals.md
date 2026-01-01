# API & REST API Fundamentals

## 🌐 API & REST API Fundamentals

### What is an API?

**Definition:** API (Application Programming Interface) is a set of rules and protocols that allows different software applications to communicate with each other.

**Real-life example:**
Like a restaurant menu - it's a list of dishes (endpoints) you can order (requests), and the kitchen (server) prepares and serves them (responses). You don't need to know how the kitchen works, just what you can order.

**Example:**
```python
# API endpoint: GET /api/students/
# Request: "Give me all students"
# Response: List of students in JSON format
```

### What is REST API?

**Definition:** REST (Representational State Transfer) is an architectural style for designing web services. REST APIs use HTTP methods (GET, POST, PUT, DELETE) to perform operations on resources.

**Real-life example:**
Like a library system:
- GET = "Show me the book" (read)
- POST = "Add a new book" (create)
- PUT = "Replace the entire book" (update)
- PATCH = "Update just the title" (partial update)
- DELETE = "Remove the book" (delete)

**REST Principles:**
1. **Stateless** - Each request contains all information needed
2. **Resource-based** - Everything is a resource (students, books, etc.)
3. **HTTP methods** - Use proper HTTP verbs
4. **Uniform interface** - Consistent URL patterns

**Example:**
```
GET    /api/students/        → List all students
POST   /api/students/        → Create a student
GET    /api/students/1/      → Get student with ID 1
PUT    /api/students/1/      → Update student 1 (full)
PATCH  /api/students/1/      → Update student 1 (partial)
DELETE /api/students/1/     → Delete student 1
```

### RESTful Naming Conventions

**Definition:** RESTful naming follows conventions for URL structure that make APIs intuitive and predictable.

**Real-life example:**
Like street addresses - clear, consistent naming helps you find places easily.

**Rules:**
1. Use nouns, not verbs (resources, not actions)
2. Use plural nouns for collections
3. Use lowercase with hyphens or underscores
4. Keep URLs hierarchical

**Examples:**
```
✅ Good:
GET    /api/students/           # List students
POST   /api/students/           # Create student
GET    /api/students/1/         # Get student
PUT    /api/students/1/         # Update student
DELETE /api/students/1/         # Delete student

❌ Bad:
GET    /api/getStudents         # Verb in URL
POST   /api/student             # Singular for collection
GET    /api/student/update/1    # Action in URL
```

### Idempotent APIs

**Definition:** An idempotent API means making the same request multiple times produces the same result as making it once.

**Real-life example:**
Like a light switch - pressing it twice is the same as once (GET, PUT, DELETE are idempotent). POST is like adding ingredients - doing it twice adds twice!

**Idempotent Methods:**
- **GET** - Always returns same result
- **PUT** - Replaces resource (same result if called multiple times)
- **DELETE** - Deletes resource (same result if called multiple times)
- **PATCH** - Usually idempotent (should be designed to be)

**Non-idempotent:**
- **POST** - Creates new resource each time

**Example:**
```python
# Idempotent: PUT /api/students/1/
# First call: Updates student
# Second call: Updates student to same state (idempotent)

# Non-idempotent: POST /api/students/
# First call: Creates student with ID 1
# Second call: Creates student with ID 2 (different result)
```

### Idempotency Keys

**Definition:** Idempotency keys are unique identifiers sent with requests to ensure a request is processed only once, even if sent multiple times.

**Real-life example:**
Like a receipt number - if you pay twice with the same receipt number, only one payment goes through.

**How it works:**
1. Client generates unique key (UUID)
2. Sends key with request
3. Server checks if key was used
4. If used, returns previous response
5. If new, processes request and stores key

**Example:**
```python
# Client sends:
POST /api/payments/
Headers: {"Idempotency-Key": "abc-123-def-456"}
Body: {"amount": 100}

# Server:
# First time: Processes payment, stores key, returns result
# Second time (same key): Returns cached result without processing
```

**Implementation:**
```python
# Import Django's cache framework - provides caching functionality
# cache: Django's caching framework, supports multiple backends (Redis, Memcached, etc.)
from django.core.cache import cache
# Import APIView - base class for class-based views in DRF
# APIView: Provides methods (get, post, put, delete) and handles HTTP requests
from rest_framework.views import APIView
# Import Response - DRF's response class for API responses
from rest_framework.response import Response

class PaymentView(APIView):
    """
    APIView: Base class for DRF views
    - Provides HTTP method handlers (get, post, put, delete, patch)
    - Handles request parsing and response rendering
    - Integrates with authentication, permissions, throttling
    
    Alternative: Use ViewSet for multiple related operations
    Difference: APIView is for single endpoints, ViewSet for resource-based CRUD
    """
    
    def post(self, request):
        """
        post(): Handles POST HTTP requests
        request: DRF's Request object containing:
            - request.data: Parsed request body (dict/list)
            - request.query_params: URL query parameters
            - request.headers: HTTP headers
            - request.user: Authenticated user (if authenticated)
        
        Alternative method names: get(), put(), patch(), delete()
        """
        # request.headers.get(): Gets HTTP header value, returns None if not found
        # 'Idempotency-Key': Custom header name (can be any string)
        idempotency_key = request.headers.get('Idempotency-Key')
        
        # Check if idempotency key provided (defensive programming)
        if idempotency_key:
            # cache.get(): Retrieves value from cache
            # f'idempotency:{idempotency_key}': Cache key (f-string for formatting)
            # Returns None if key doesn't exist
            cached_response = cache.get(f'idempotency:{idempotency_key}')
            
            # If we've seen this key before, return cached response
            if cached_response:
                # Response(): Creates HTTP response with status 200 by default
                # Returns cached response without processing (idempotent behavior)
                return Response(cached_response)
        
        # Process payment (actual business logic)
        # request.data: Contains parsed JSON/form data from request body
        result = process_payment(request.data)
        
        # Cache the result for future duplicate requests
        if idempotency_key:
            # cache.set(): Stores value in cache
            # timeout=3600: Cache expires in 3600 seconds (1 hour)
            # Alternatives: timeout=None (never expire), or use cache backend defaults
            cache.set(f'idempotency:{idempotency_key}', result, timeout=3600)
        
        # Return successful response (status 200 by default)
        # Response() automatically serializes Python dict/list to JSON
        return Response(result)

# Alternative Implementation: Using Database Instead of Cache
# from django.db import models
# class IdempotencyKey(models.Model):
#     key = models.CharField(max_length=255, unique=True)
#     response_data = models.JSONField()
#     created_at = models.DateTimeField(auto_now_add=True)
# 
# # In view:
# idempotency_key = request.headers.get('Idempotency-Key')
# if idempotency_key:
#     try:
#         cached = IdempotencyKey.objects.get(key=idempotency_key)
#         return Response(cached.response_data)
#     except IdempotencyKey.DoesNotExist:
#         pass
# 
# result = process_payment(request.data)
# if idempotency_key:
#     IdempotencyKey.objects.create(key=idempotency_key, response_data=result)
# return Response(result)
# 
# Difference: Cache is faster but temporary, Database is persistent but slower
# Use cache for: High-frequency APIs, temporary data
# Use database for: Important transactions, audit trail needed
```

---

## 🏗️ Django Project Structure

### What is Django Project Structure?

**Definition:** Django organizes code into projects (the entire application) and apps (modular components). Think of a project as a building and apps as rooms in that building.

**Real-life example:**
Like a shopping mall (project) with different stores (apps):
- Each store (app) has its own purpose
- All stores share common facilities (Django framework)
- The mall management (project) coordinates everything

**Structure:**
```
drf_tutorial/              # Project (the mall)
├── drf_tutorial/          # Project settings (mall management)
│   ├── settings.py        # Configuration
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # Server interface
├── basics/                # App 1 (store)
│   ├── models.py          # Data structure
│   ├── views.py           # Business logic
│   ├── serializers.py     # Data conversion
│   └── urls.py            # App URLs
├── intermediate/          # App 2 (another store)
└── manage.py             # Management commands
```

### Django Settings for REST APIs

**Definition:** Django settings configure how your application behaves, including DRF-specific settings.

**Real-life example:**
Like a control panel - you adjust settings to make your API work correctly.

**Common DRF Settings:**
```python
# settings.py
# INSTALLED_APPS: List of Django apps enabled in this project
# Order matters: Apps earlier in list have precedence in conflicts
INSTALLED_APPS = [
    # Django built-in apps (must be in this order for dependencies)
    'django.contrib.admin',           # Admin interface (requires: auth, contenttypes, sessions)
    'django.contrib.auth',            # Authentication system (user, groups, permissions)
    'django.contrib.contenttypes',    # Content types framework (generic relations)
    'django.contrib.sessions',        # Session framework (user session management)
    'django.contrib.messages',        # Messaging framework (flash messages)
    'django.contrib.staticfiles',     # Static file management (CSS, JS, images)
    
    # DRF (Django REST Framework) apps
    'rest_framework',                 # Core DRF framework (views, serializers, etc.)
    # Alternative: Use 'rest_framework' alone if not using token auth
    'rest_framework.authtoken',       # Token authentication (creates Token model)
    # Alternative: 'rest_framework_simplejwt' for JWT tokens
    # Difference: Token is simple (1 token per user), JWT is stateless (can be revoked/refreshed)
    
    # Your custom apps (order doesn't matter, but group them logically)
    'myapp',                          # Your application
]

# REST_FRAMEWORK: Dictionary of DRF configuration settings
# These are defaults - can be overridden per-view using view attributes
REST_FRAMEWORK = {
    # DEFAULT_AUTHENTICATION_CLASSES: Authentication methods tried in order
    # DRF tries each class until one succeeds (returns user, token tuple)
    # First successful authentication sets request.user and request.auth
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # SessionAuthentication: Uses Django's session framework (cookie-based)
        # - Good for: Web apps, browser-based clients
        # - Bad for: Mobile apps, API-only services
        'rest_framework.authentication.SessionAuthentication',
        
        # TokenAuthentication: Simple token-based auth (Token model)
        # - Header format: Authorization: Token <token_string>
        # - Good for: Simple APIs, internal services
        # - Bad for: High-security requirements, stateless services
        'rest_framework.authentication.TokenAuthentication',
        
        # Alternative authentication classes:
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT (better for stateless)
        # 'rest_framework.authentication.BasicAuthentication',  # Basic auth (username:password, not recommended)
    ],
    
    # DEFAULT_PERMISSION_CLASSES: Permission checks applied to all views
    # Executed after authentication, checks if user has permission
    'DEFAULT_PERMISSION_CLASSES': [
        # IsAuthenticated: User must be authenticated (logged in)
        # - Returns 401 Unauthorized if not authenticated
        # - Alternative: 'rest_framework.permissions.AllowAny' (no auth required)
        # - Alternative: 'rest_framework.permissions.IsAdminUser' (admin only)
        # - Alternative: 'rest_framework.permissions.IsAuthenticatedOrReadOnly' (read without auth, write requires auth)
        'rest_framework.permissions.IsAuthenticated',
    ],
    
    # DEFAULT_PAGINATION_CLASS: Pagination class for list views
    # Automatically paginates queryset results
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # Alternatives:
    # - 'rest_framework.pagination.LimitOffsetPagination' (limit/offset style)
    # - 'rest_framework.pagination.CursorPagination' (cursor-based, for large datasets)
    # Difference: PageNumber uses page numbers (?page=2), LimitOffset uses (?limit=10&offset=20)
    
    # PAGE_SIZE: Default number of items per page (for PageNumberPagination)
    'PAGE_SIZE': 20,
    # Can be overridden per-view: pagination_class = MyPagination(page_size=50)
    
    # DEFAULT_FILTER_BACKENDS: Filter backends applied to all viewsets
    # Allows filtering, searching, ordering via query parameters
    'DEFAULT_FILTER_BACKENDS': [
        # DjangoFilterBackend: Field-based filtering (requires django-filter package)
        # - Usage: ?age=20&grade=A
        # - Install: pip install django-filter
        'django_filters.rest_framework.DjangoFilterBackend',
        
        # SearchFilter: Full-text search across multiple fields
        # - Usage: ?search=john (searches in specified fields)
        # - Configure in view: search_fields = ['name', 'email']
        'rest_framework.filters.SearchFilter',
        
        # OrderingFilter: Order results by fields
        # - Usage: ?ordering=name (ascending), ?ordering=-created_at (descending)
        # - Configure in view: ordering_fields = ['name', 'created_at']
        'rest_framework.filters.OrderingFilter',
    ],
    
    # Other useful settings (not shown above):
    # 'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],  # Response format
    # 'DEFAULT_PARSER_CLASSES': ['rest_framework.parsers.JSONParser'],  # Request format
    # 'DEFAULT_THROTTLE_CLASSES': [...],  # Rate limiting
    # 'EXCEPTION_HANDLER': 'myapp.exceptions.custom_exception_handler',  # Custom error handling
}
```

### Installed Apps & Middleware

**Definition:** 
- **Installed Apps** - Django apps that are active in your project
- **Middleware** - Code that runs on every request/response

**Real-life example:**
- **Apps** = Tools in your toolbox (what you can use)
- **Middleware** = Security guards checking everyone entering/exiting

**Installed Apps:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',           # Admin interface
    'django.contrib.auth',            # Authentication
    'django.contrib.contenttypes',    # Content types
    'django.contrib.sessions',        # Sessions
    'rest_framework',                 # DRF framework
    'rest_framework.authtoken',       # Token auth
    'myapp',                          # Your app
]
```

**Middleware:**
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',     # Security headers
    'django.contrib.sessions.middleware.SessionMiddleware',  # Sessions
    'django.middleware.common.CommonMiddleware',         # Common tasks
    'django.middleware.csrf.CsrfViewMiddleware',        # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Auth
    'django.contrib.messages.middleware.MessageMiddleware',     # Messages
]
```

**How Middleware Works:**
```
Request → Middleware 1 → Middleware 2 → ... → View → ... → Middleware 2 → Middleware 1 → Response
```

### URL Routing Basics

**Definition:** URL routing maps URLs to views that handle requests.

**Real-life example:**
Like a receptionist directing visitors to the right department based on what they're asking for.

**Basic Routing:**
```python
# project/urls.py (main URLs)
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('myapp.urls')),  # Include app URLs
]

# myapp/urls.py (app URLs)
from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.StudentList.as_view()),      # List
    path('students/<int:pk>/', views.StudentDetail.as_view()),  # Detail
]
```

**Router-based Routing (DRF):**
```python
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
# Automatically creates all CRUD URLs
```

---

## 🎭 MVT vs MVC

### What is MVT?

**Definition:** MVT (Model-View-Template) is Django's pattern:
- **Model** - Data structure (database)
- **View** - Business logic (what happens)
- **Template** - Presentation (HTML)

### What is MVC?

**Definition:** MVC (Model-View-Controller) is a general pattern:
- **Model** - Data
- **View** - Presentation
- **Controller** - Logic

### Difference:

- **MVC:** Controller handles logic, View displays
- **MVT:** View handles logic, Template displays (Django's "View" = MVC's "Controller")

**Real-life example:**
- **MVC:** Like a restaurant - Chef (Controller) prepares, Waiter (View) serves
- **MVT:** Like a restaurant - Chef-Waiter (View) does both, Menu (Template) shows

**In Django Web:**
```python
# Model - Data structure
class Student(models.Model):
    name = models.CharField(max_length=100)

# View - Business logic (Django View = MVC Controller)
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students.html', {'students': students})

# Template - Presentation (HTML)
# students.html: {% for student in students %}...{% endfor %}
```

**In DRF (APIs):**
```python
# Model - Data structure
class Student(models.Model):
    name = models.CharField(max_length=100)

# View - Business logic (DRF View = Controller in MVC)
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

# Template - Not used in APIs (JSON instead)
# Response is JSON, not HTML template
```

---

## 📊 Important SQL Queries

### Basic SQL Operations

**Real-life example:**
SQL is like asking questions to a librarian about books in a library.

**Common SQL Queries:**

#### SELECT (Read)
```sql
-- Get all students
SELECT * FROM students;

-- Get specific columns
SELECT name, age FROM students;

-- Get with condition
SELECT * FROM students WHERE age > 18;

-- Get with ordering
SELECT * FROM students ORDER BY name ASC;
```

#### INSERT (Create)
```sql
-- Insert one record
INSERT INTO students (name, age, email) 
VALUES ('John', 20, 'john@example.com');

-- Insert multiple
INSERT INTO students (name, age) VALUES
('John', 20),
('Jane', 22);
```

#### UPDATE (Update)
```sql
-- Update one record
UPDATE students 
SET age = 21 
WHERE id = 1;

-- Update multiple
UPDATE students 
SET age = age + 1 
WHERE grade = 'A';
```

#### DELETE (Delete)
```sql
-- Delete one record
DELETE FROM students WHERE id = 1;

-- Delete multiple
DELETE FROM students WHERE age < 18;
```

### Django ORM Equivalents

**Django ORM translates Python code to SQL:**

```python
# SELECT * FROM students
Student.objects.all()

# SELECT name, age FROM students WHERE age > 18
Student.objects.filter(age__gt=18).values('name', 'age')

# INSERT INTO students (name, age) VALUES ('John', 20)
Student.objects.create(name='John', age=20)

# UPDATE students SET age = 21 WHERE id = 1
Student.objects.filter(id=1).update(age=21)

# DELETE FROM students WHERE id = 1
Student.objects.filter(id=1).delete()
```

**In API Views:**
```python
# viewsets.ModelViewSet: DRF viewset that provides full CRUD operations
# - Automatically creates: list, create, retrieve, update, partial_update, destroy
# - Alternative: viewsets.ReadOnlyModelViewSet (only read operations)
# - Alternative: GenericViewSet + Mixins (more control, more code)
class StudentViewSet(viewsets.ModelViewSet):
    # queryset: Base queryset for this viewset (used if get_queryset not overridden)
    # .objects.all(): Manager method - returns QuerySet (lazy, not executed until evaluated)
    # Equivalent SQL: SELECT * FROM students
    queryset = Student.objects.all()
    
    def get_queryset(self):
        """
        get_queryset(): Override to customize queryset based on request
        - Called by DRF to get queryset for list/retrieve operations
        - Can filter based on user, query params, etc.
        - Returns QuerySet (lazy evaluation - SQL not executed until serializer accesses data)
        """
        # self.request: DRF Request object (wraps Django's HttpRequest)
        # .query_params: Dictionary-like object containing URL query parameters
        # .get(): Returns value or None if key doesn't exist
        # Alternative: .query_params['age'] (raises KeyError if missing)
        age = self.request.query_params.get('age')
        
        # Type check and filter if age provided
        if age:
            # .filter(): QuerySet method - adds WHERE clause to SQL
            # age=age: Field lookup (exact match)
            # Alternative lookups: age__gt=20 (greater than), age__lt=30 (less than)
            # Returns new QuerySet (doesn't modify original)
            return Student.objects.filter(age=age)  # SQL: WHERE age = ?
        
        # Return default queryset if no filter
        return Student.objects.all()

# Alternative: Using Q objects for complex queries
# from django.db.models import Q
# def get_queryset(self):
#     queryset = Student.objects.all()
#     age = self.request.query_params.get('age')
#     grade = self.request.query_params.get('grade')
#     if age or grade:
#         query = Q()
#         if age:
#             query &= Q(age=age)  # AND condition
#         if grade:
#             query |= Q(grade=grade)  # OR condition
#         queryset = queryset.filter(query)
#     return queryset
```

---

## 🎓 Advanced Interview Topics (4+ Years Experience)

### API Versioning Strategies

**Definition:** API versioning allows you to evolve your API without breaking existing clients.

**Strategies:**

**1. URL Path Versioning:**
```python
# URLs: /api/v1/students/, /api/v2/students/
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
}
# urls.py
urlpatterns = [
    path('api/v1/', include('v1.urls')),
    path('api/v2/', include('v2.urls')),
]
# Pros: Clear, cacheable, simple
# Cons: URL pollution, harder to maintain
```

**2. Header Versioning:**
```python
# Header: Accept: application/vnd.api+json;version=1
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
}
# Pros: Clean URLs, RESTful
# Cons: Less visible, harder to test
```

**3. Namespace Versioning:**
```python
# Use Django URL namespaces
urlpatterns = [
    path('api/', include(('v1.urls', 'api'), namespace='v1')),
    path('api/', include(('v2.urls', 'api'), namespace='v2')),
]
# Pros: Clean separation, easy to test
# Cons: More complex setup
```

**Best Practice:** Use URL path versioning for public APIs (clear and cacheable).

### HATEOAS (Hypermedia as the Engine of Application State)

**Definition:** Include links in API responses to guide clients through the API.

**Implementation:**
```python
from rest_framework import serializers
from rest_framework.reverse import reverse

class StudentSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = ['id', 'name', 'links']
    
    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('student-detail', kwargs={'pk': obj.pk}, request=request),
            'update': reverse('student-detail', kwargs={'pk': obj.pk}, request=request),
            'delete': reverse('student-detail', kwargs={'pk': obj.pk}, request=request),
        }
```

### API Gateway Pattern

**Definition:** Single entry point that routes requests to appropriate microservices.

**Benefits:**
- Centralized authentication
- Rate limiting
- Request/response transformation
- Load balancing
- API versioning

**Implementation with Django:**
```python
# Gateway service
class APIGatewayView(APIView):
    SERVICE_MAP = {
        'students': 'http://students-service:8001',
        'courses': 'http://courses-service:8002',
    }
    
    def dispatch(self, request, *args, **kwargs):
        service_name = self.get_service_name(request.path)
        service_url = self.SERVICE_MAP.get(service_name)
        
        if not service_url:
            return Response({'error': 'Service not found'}, status=404)
        
        # Forward request to microservice
        response = requests.request(
            method=request.method,
            url=f"{service_url}{request.path}",
            headers=self.filter_headers(request.headers),
            data=request.body,
            params=request.query_params,
        )
        return Response(response.json(), status=response.status_code)
```

### GraphQL vs REST

**Differences:**

| Aspect | REST | GraphQL |
|--------|------|---------|
| Data Fetching | Multiple requests | Single request |
| Over-fetching | Yes (gets all fields) | No (client specifies fields) |
| Under-fetching | Yes (need multiple endpoints) | No (can get related data) |
| Caching | Easy (HTTP caching) | Complex (custom caching) |
| Learning Curve | Low | Higher |
| Tooling | Mature | Growing |

**When to Use REST:**
- Simple CRUD operations
- Need HTTP caching
- Existing REST infrastructure
- Mobile apps (better HTTP caching)

**When to Use GraphQL:**
- Complex data relationships
- Multiple client types (mobile, web, etc.)
- Need to reduce over-fetching
- Real-time subscriptions needed

### API Rate Limiting Strategies

**1. Token Bucket:**
```python
# Allows bursts up to bucket size, refills at constant rate
from rest_framework.throttling import UserRateThrottle

class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'
    rate = '100/hour'  # 100 requests per hour
```

**2. Sliding Window:**
```python
# More accurate, prevents bursts
from rest_framework.throttling import AnonRateThrottle

class SustainedRateThrottle(AnonRateThrottle):
    scope = 'sustained'
    rate = '1000/day'  # 1000 requests per day
```

**3. Distributed Rate Limiting (Redis):**
```python
# For multiple servers
from django.core.cache import cache
from rest_framework.throttling import BaseThrottle

class RedisRateThrottle(BaseThrottle):
    def allow_request(self, request, view):
        key = f"throttle:{request.user.id}"
        count = cache.get(key, 0)
        if count >= 100:
            return False
        cache.set(key, count + 1, 3600)  # 1 hour
        return True
```

### API Documentation Best Practices

**1. OpenAPI/Swagger:**
```python
# Install: pip install drf-yasg or drf-spectacular
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Student API",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
)
```

**2. Include Examples:**
- Request/response examples
- Error responses
- Authentication methods
- Rate limits

**3. Version Documentation:**
- Document all versions
- Deprecation notices
- Migration guides

### API Testing Strategies

**1. Contract Testing:**
- Ensure API matches documentation
- Test request/response schemas
- Use tools: Pact, Dredd

**2. Integration Testing:**
```python
from rest_framework.test import APITestCase

class StudentAPITestCase(APITestCase):
    def setUp(self):
        # Create test data
        self.student = Student.objects.create(name='Test')
    
    def test_list_students(self):
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
```

**3. Load Testing:**
- Use tools: Locust, Apache JMeter
- Test rate limits
- Test concurrent requests
- Monitor response times

### Microservices Communication Patterns

**1. Synchronous (HTTP/REST):**
- Simple, familiar
- Can cause cascading failures
- Use circuit breakers

**2. Asynchronous (Message Queue):**
- Decoupled services
- Better resilience
- Eventual consistency

**3. gRPC:**
- High performance
- Type-safe
- Streaming support
- Better for internal services

### API Security Best Practices

**1. Authentication:**
- Use OAuth2/JWT for stateless auth
- Implement token refresh
- Use HTTPS only

**2. Authorization:**
- Principle of least privilege
- Role-based access control (RBAC)
- Resource-level permissions

**3. Input Validation:**
- Validate all inputs
- Sanitize user data
- Use serializer validation

**4. Output Encoding:**
- Prevent XSS attacks
- Use JSON serialization
- Avoid exposing sensitive data

**5. Rate Limiting:**
- Prevent abuse
- DDoS protection
- Fair usage policies

### Performance Optimization

**1. Database Optimization:**
```python
# Use select_related for ForeignKey
students = Student.objects.select_related('school').all()

# Use prefetch_related for ManyToMany
students = Student.objects.prefetch_related('courses').all()

# Use only() to limit fields
students = Student.objects.only('id', 'name').all()

# Use defer() to exclude heavy fields
students = Student.objects.defer('description').all()
```

**2. Caching:**
```python
# View-level caching
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 15 minutes
def student_list(request):
    ...

# Query caching
from django.core.cache import cache

def get_students():
    cache_key = 'students_list'
    students = cache.get(cache_key)
    if students is None:
        students = list(Student.objects.all())
        cache.set(cache_key, students, 3600)
    return students
```

**3. Pagination:**
- Always paginate large datasets
- Use cursor pagination for large datasets
- Set reasonable page sizes

**4. Compression:**
```python
# Enable GZIP compression
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    ...
]
```

### Monitoring and Observability

**1. Logging:**
```python
import logging
logger = logging.getLogger(__name__)

class StudentViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        logger.info(f"Creating student: {request.data}")
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error creating student: {e}", exc_info=True)
            raise
```

**2. Metrics:**
- Request rate
- Response times
- Error rates
- Use: Prometheus, Datadog, New Relic

**3. Tracing:**
- Distributed tracing for microservices
- Track requests across services
- Use: OpenTelemetry, Jaeger

---

*This guide covers essential and advanced API concepts. Master these topics for senior-level Django REST Framework positions.*

