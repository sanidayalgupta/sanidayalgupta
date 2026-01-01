# Django Views

## 🎯 Django Views

### Function Based Views (FBV)

**Definition:** Function-based views are simple Python functions that handle HTTP requests.

**Real-life example:**
Like individual workers - each function does one specific job.

**Example:**
```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def student_list(request):
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

**When to use:**
- Simple, one-off endpoints
- Custom logic that doesn't fit standard patterns
- Learning/practice

### APIView

**Definition:** APIView is a base class for class-based views in DRF. It provides methods for each HTTP method.

**Real-life example:**
Like a multi-tool - one class handles multiple operations.

**Example:**
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class StudentListAPIView(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

**When to use:**
- Need custom logic for each method
- More structure than FBV but more control than generics
- Common base for class-based views

### GenericAPIView

**Definition:** GenericAPIView provides common functionality (queryset, serializer) that other views can use.

**Real-life example:**
Like a template - provides the structure, you fill in details.

**Example:**
```python
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin

class StudentListCreateView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```

**Key Properties:**
```python
class MyView(GenericAPIView):
    queryset = Student.objects.all()          # Default queryset
    serializer_class = StudentSerializer      # Default serializer
    
    def get_queryset(self):
        # Custom queryset logic
        return Student.objects.filter(active=True)
    
    def get_serializer_class(self):
        # Different serializer for different actions
        if self.action == 'create':
            return StudentCreateSerializer
        return StudentSerializer
```

### Mixins

**Definition:** Mixins are reusable classes that provide specific functionality. You combine multiple mixins to build a view.

**Real-life example:**
Like LEGO blocks - each mixin adds a feature, you combine them.

**Common Mixins:**
```python
ListModelMixin      # Provides list() method
CreateModelMixin    # Provides create() method
RetrieveModelMixin  # Provides retrieve() method
UpdateModelMixin    # Provides update() method
DestroyModelMixin   # Provides destroy() method
```

**Example:**
```python
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

class StudentViewSet(GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # Automatically gets: list(), create(), retrieve()
```

**What each mixin provides:**
```python
# ListModelMixin
# GET /students/ → list() method

# CreateModelMixin
# POST /students/ → create() method

# RetrieveModelMixin
# GET /students/1/ → retrieve() method

# UpdateModelMixin
# PUT /students/1/ → update() method

# DestroyModelMixin
# DELETE /students/1/ → destroy() method
```

### ViewSets

**Definition:** ViewSets combine multiple related views into a single class. They're like a complete toolkit.

**Real-life example:**
Like a Swiss Army knife - one tool with multiple functions.

**Example:**
```python
from rest_framework import viewsets

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # Automatically provides: list, create, retrieve, update, destroy
```

**Types of ViewSets:**
```python
# ReadOnlyModelViewSet - Only read operations
class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    # Provides: list(), retrieve()
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

# ModelViewSet - Full CRUD
class StudentViewSet(viewsets.ModelViewSet):
    # Provides: list(), create(), retrieve(), update(), destroy()
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

# GenericViewSet - Base for custom ViewSets
class StudentViewSet(viewsets.GenericViewSet):
    # Base class, add mixins manually
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
```

### ModelViewSet

**Definition:** ModelViewSet provides full CRUD operations for a model automatically.

**Real-life example:**
Like an automatic vending machine - you just specify what product (model), and it handles everything.

**Example:**
```python
from rest_framework import viewsets

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    
    # Gets all CRUD operations automatically:
    # GET    /students/          → list()
    # POST   /students/          → create()
    # GET    /students/{id}/     → retrieve()
    # PUT    /students/{id}/     → update()
    # PATCH  /students/{id}/     → partial_update()
    # DELETE /students/{id}/     → destroy()
```

**Customizing ModelViewSet:**
```python
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    def get_queryset(self):
        # Custom filtering
        queryset = Student.objects.all()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(active=True)
    
    def perform_create(self, serializer):
        # Custom create logic
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        # Custom update logic
        serializer.save(updated_by=self.request.user)
```

### Custom Actions (@action)

**Definition:** Custom actions are additional endpoints you can add to ViewSets beyond standard CRUD.

**Real-life example:**
Like adding custom buttons to a remote control - standard buttons (CRUD) plus your custom ones.

**Example:**
```python
from rest_framework.decorators import action
from rest_framework.response import Response

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Custom action: POST /books/{id}/like/"""
        book = self.get_object()
        book.likes_count += 1
        book.save()
        return Response({'likes_count': book.likes_count})
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Custom action: GET /books/popular/"""
        books = Book.objects.filter(likes_count__gt=100)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
```

**Action Parameters:**
```python
@action(
    detail=True,              # True = single object, False = collection
    methods=['post', 'get'],  # Allowed HTTP methods
    url_path='custom-path',   # Custom URL (default is method name)
    url_name='custom-name'    # Custom URL name
)
def my_action(self, request, pk=None):
    # detail=True → pk parameter available
    # detail=False → no pk parameter
    pass
```

**Real Project Example:**
```python
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an order: POST /orders/{id}/cancel/"""
        order = self.get_object()
        if order.status == 'cancelled':
            return Response(
                {'error': 'Order already cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        order.status = 'cancelled'
        order.save()
        return Response({'status': 'cancelled'})
    
    @action(detail=True, methods=['post'])
    def ship(self, request, pk=None):
        """Ship an order: POST /orders/{id}/ship/"""
        order = self.get_object()
        order.status = 'shipped'
        order.shipped_at = timezone.now()
        order.save()
        return Response({'status': 'shipped'})
```

### Routers

**Definition:** Routers automatically generate URL patterns for ViewSets.

**Real-life example:**
Like an automatic address system - you register a ViewSet, and it creates all the addresses (URLs).

**DefaultRouter Example:**
```python
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')

urlpatterns = router.urls

# Automatically creates:
# GET    /students/              - list
# POST   /students/              - create
# GET    /students/{id}/         - retrieve
# PUT    /students/{id}/         - update
# PATCH  /students/{id}/         - partial_update
# DELETE /students/{id}/         - destroy
```

**SimpleRouter Example:**
```python
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'students', StudentViewSet)

# Similar to DefaultRouter but without API root view
```

**Including in Main URLs:**
```python
# project/urls.py
from django.urls import path, include

urlpatterns = [
    path('api/', include('myapp.urls')),
]

# myapp/urls.py
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, BookViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'books', BookViewSet)

urlpatterns = router.urls

# Results in:
# /api/students/
# /api/students/{id}/
# /api/books/
# /api/books/{id}/
```

**Router vs Manual URLs:**
```python
# Manual URLs (more verbose)
urlpatterns = [
    path('students/', StudentList.as_view()),
    path('students/<int:pk>/', StudentDetail.as_view()),
]

# Router (cleaner, automatic)
router = DefaultRouter()
router.register(r'students', StudentViewSet)
# Automatically creates all URLs
```

### View Lifecycle (dispatch)

**Definition:** The dispatch method is called first in any view. It routes the request to the appropriate method (get, post, etc.).

**Real-life example:**
Like a receptionist - they receive all visitors (requests) and direct them to the right department (method).

**Flow:**
```
1. Request arrives
   ↓
2. dispatch() method called
   ↓
3. Checks HTTP method (GET, POST, etc.)
   ↓
4. Routes to appropriate method (get(), post(), etc.)
   ↓
5. Method executes
   ↓
6. Response returned
```

**Understanding Dispatch:**
```python
from rest_framework.views import APIView

class MyView(APIView):
    def dispatch(self, request, *args, **kwargs):
        # This runs first for every request
        print(f"Request method: {request.method}")
        print(f"Request path: {request.path}")
        
        # Call parent dispatch to route to get(), post(), etc.
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        # This runs for GET requests
        return Response({'method': 'GET'})
    
    def post(self, request):
        # This runs for POST requests
        return Response({'method': 'POST'})
```

**Custom Dispatch Example:**
```python
class LoggingView(APIView):
    def dispatch(self, request, *args, **kwargs):
        # Log request
        logger.info(f"{request.method} {request.path}")
        
        # Check authentication
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Continue with normal dispatch
        return super().dispatch(request, *args, **kwargs)
```

**Dispatch in DRF ViewSets:**
```python
class StudentViewSet(viewsets.ModelViewSet):
    def dispatch(self, request, *args, **kwargs):
        # Custom logic before routing
        if request.method in ['POST', 'PUT', 'PATCH']:
            # Validate request size
            if len(request.body) > 10000:
                return Response(
                    {'error': 'Request too large'},
                    status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
                )
        
        return super().dispatch(request, *args, **kwargs)
```

### Request Lifecycle in DRF (Detailed Flow)

**Complete Flow:**
```
1. HTTP Request arrives
   ↓
2. Django middleware (Security, Session, etc.)
   ↓
3. URL routing (urls.py)
   ↓
4. DRF ViewSet/View dispatch()
   ↓
5. Authentication (if required)
   ↓
6. Permission checks
   ↓
7. Throttle checks (rate limiting)
   ↓
8. Content negotiation (parser)
   ↓
9. Method routing (get(), post(), etc.)
   ↓
10. get_queryset() / get_object()
   ↓
11. get_serializer()
   ↓
12. Business logic execution
   ↓
13. Serialization
   ↓
14. Response creation
   ↓
15. Content negotiation (renderer)
   ↓
16. Response returned
```

**Hooking into the Lifecycle:**
```python
class StudentViewSet(viewsets.ModelViewSet):
    def initial(self, request, *args, **kwargs):
        """Called before any method"""
        super().initial(request, *args, **kwargs)
        # Custom logic here
    
    def get_queryset(self):
        """Called to get queryset"""
        return Student.objects.all()
    
    def get_object(self):
        """Called to get single object"""
        return super().get_object()
    
    def get_serializer(self, *args, **kwargs):
        """Called to get serializer"""
        return super().get_serializer(*args, **kwargs)
    
    def perform_create(self, serializer):
        """Called during create"""
        serializer.save()
    
    def finalize_response(self, request, response, *args, **kwargs):
        """
        finalize_response(): Called before returning response to client
        - Last chance to modify response
        - Can add headers, modify data, change status code
        - Always call super() to maintain DRF functionality
        """
        # super(): Calls parent class method (important for DRF functionality)
        # Maintains response structure, content negotiation, etc.
        response = super().finalize_response(request, response, *args, **kwargs)
        
        # Add custom headers (useful for API versioning, rate limits, etc.)
        # response: DRF Response object (similar to Django's HttpResponse)
        # Can be accessed like dictionary for headers
        response['X-Custom'] = 'value'
        response['X-API-Version'] = '1.0'
        
        return response

# Alternative: Using response decorators
# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page
# 
# @method_decorator(cache_page(60 * 15), name='list')
# class StudentViewSet(viewsets.ModelViewSet):
#     ...

# Difference: finalize_response() runs for all actions,
# decorators can target specific actions
```

---

## 🎓 Advanced Interview Topics (4+ Years Experience)

### View Performance Optimization

**1. QuerySet Optimization:**
```python
class StudentViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        # Bad: N+1 queries (one query per student's school)
        # return Student.objects.all()
        
        # Good: Use select_related for ForeignKey/OneToOne
        return Student.objects.select_related('school', 'classroom').all()
        
        # Good: Use prefetch_related for ManyToMany/Reverse FK
        return Student.objects.prefetch_related('courses', 'grades').all()
        
        # Best: Combine both
        return Student.objects.select_related(
            'school'
        ).prefetch_related(
            'courses',
            'grades__teacher'
        ).all()
```

**2. Pagination Optimization:**
```python
# For large datasets, use CursorPagination (more efficient)
class StudentCursorPagination(CursorPagination):
    page_size = 100
    ordering = 'id'  # Must be unique, stable ordering

# vs PageNumberPagination (simpler but less efficient for large datasets)
class StudentPagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
```

**3. Caching Strategies:**
```python
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

class StudentViewSet(viewsets.ModelViewSet):
    # Cache list view for 15 minutes
    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    # Or use per-view caching in settings
    # Or use cache framework in get_queryset()
    def get_queryset(self):
        cache_key = 'students_list'
        queryset = cache.get(cache_key)
        if queryset is None:
            queryset = Student.objects.all()
            cache.set(cache_key, queryset, 3600)
        return queryset
```

### Custom ViewSet Patterns

**1. Bulk Operations:**
```python
class StudentViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Bulk create students"""
        serializer = StudentSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        students = serializer.save()
        return Response(
            StudentSerializer(students, many=True).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['put', 'patch'])
    def bulk_update(self, request):
        """Bulk update students"""
        # Implementation for bulk updates
        pass
```

**2. Action-Level Permissions:**
```python
class StudentViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        """Return permissions based on action"""
        if self.action == 'destroy':
            # Only admins can delete
            return [IsAdminUser()]
        elif self.action in ['create', 'update', 'partial_update']:
            # Authenticated users can create/update
            return [IsAuthenticated()]
        # Default: read-only for everyone
        return [AllowAny()]
```

**3. Different Serializers for Different Actions:**
```python
class StudentViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        """Return serializer class based on action"""
        if self.action == 'create':
            return StudentCreateSerializer  # Write-only fields
        elif self.action == 'list':
            return StudentListSerializer  # Limited fields for list
        elif self.action == 'retrieve':
            return StudentDetailSerializer  # Full details
        return StudentSerializer  # Default
```

### View Testing Strategies

**1. APITestCase:**
```python
from rest_framework.test import APITestCase
from rest_framework import status

class StudentViewSetTestCase(APITestCase):
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.student = Student.objects.create(name='Test Student')
    
    def test_list_students(self):
        """Test listing students"""
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_create_student(self):
        """Test creating student"""
        data = {'name': 'New Student', 'age': 20}
        response = self.client.post('/api/students/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 2)
```

**2. Testing Permissions:**
```python
def test_unauthenticated_access(self):
    """Test that unauthenticated users cannot create"""
    self.client.force_authenticate(user=None)
    response = self.client.post('/api/students/', {'name': 'Test'})
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

def test_permission_denied(self):
    """Test that non-owners cannot delete"""
    other_user = User.objects.create_user('other', 'pass')
    self.client.force_authenticate(user=other_user)
    response = self.client.delete(f'/api/students/{self.student.id}/')
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
```

### Error Handling Patterns

**1. Custom Exception Handling:**
```python
from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    """Custom exception handler"""
    response = exception_handler(exc, context)
    
    if response is not None:
        # Customize error response
        custom_response_data = {
            'error': {
                'status_code': response.status_code,
                'message': response.data.get('detail', 'An error occurred'),
                'errors': response.data
            }
        }
        response.data = custom_response_data
    
    return response

# In settings.py
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'myapp.exceptions.custom_exception_handler',
}
```

**2. View-Level Error Handling:**
```python
class StudentViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as e:
            # Handle database integrity errors
            return Response(
                {'error': 'Student with this email already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValidationError as e:
            # Handle validation errors
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
```

### View Composition Patterns

**1. Mixin Composition:**
```python
class CreateListModelMixin:
    """Custom mixin for create and list only"""
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class StudentViewSet(
    CreateListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
```

**2. ViewSet Inheritance:**
```python
class BaseViewSet(viewsets.ModelViewSet):
    """Base viewset with common functionality"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filter by current user by default
        return super().get_queryset().filter(user=self.request.user)

class StudentViewSet(BaseViewSet):
    """Student viewset inheriting from base"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
```

### API Documentation with Views

**1. Schema Generation:**
```python
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class StudentViewSet(viewsets.ModelViewSet):
    @swagger_auto_schema(
        operation_description="List all students",
        responses={200: StudentSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Create a new student",
        request_body=StudentSerializer,
        responses={201: StudentSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
```

---

*This guide covers essential and advanced view patterns. Master these for senior Django REST Framework positions.*

