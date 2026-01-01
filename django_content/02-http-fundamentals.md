# HTTP Fundamentals

## 🌍 HTTP Request-Response Lifecycle

### HTTP Request-Response Lifecycle

**Definition:** The HTTP lifecycle is the journey of a request from client to server and back.

**Real-life example:**
Like sending a letter:
1. You write a letter (client creates request)
2. You mail it (request sent over network)
3. Post office delivers (routing to server)
4. Recipient reads and responds (server processes)
5. Response letter arrives (response sent back)
6. You read the response (client receives)

**Lifecycle Steps:**
```
1. Client creates HTTP request
   ↓
2. Request sent over network (HTTP/HTTPS)
   ↓
3. Django receives request
   ↓
4. URL routing (urls.py) finds the right view
   ↓
5. Middleware processes request
   ↓
6. View executes (business logic)
   ↓
7. Serializer converts data
   ↓
8. Response created
   ↓
9. Middleware processes response
   ↓
10. Response sent to client
```

**Example in DRF:**
```python
# 1. Client sends: GET /api/students/
# 2. Django receives request
# 3. urls.py routes to StudentViewSet
# 4. ViewSet.list() method executes
# 5. Queries database: Student.objects.all()
# 6. Serializer converts to JSON
# 7. Response sent: [{"id": 1, "name": "John"}, ...]
```

### HTTP Methods

**Definition:** HTTP methods indicate what action you want to perform on a resource.

**Real-life example:**
Like library operations:
- **GET** = "Show me" (read)
- **POST** = "Add new" (create)
- **PUT** = "Replace entirely" (full update)
- **PATCH** = "Update partially" (partial update)
- **DELETE** = "Remove" (delete)

#### GET
**What it does:** Retrieves data without modifying anything
**Example:**
```python
GET /api/students/1/
# Response: {"id": 1, "name": "John", "age": 20}
```

#### POST
**What it does:** Creates a new resource
**Example:**
```python
POST /api/students/
Body: {"name": "Jane", "age": 22}
# Response: {"id": 2, "name": "Jane", "age": 22}
```

#### PUT
**What it does:** Replaces entire resource (all fields required)
**Example:**
```python
PUT /api/students/1/
Body: {"name": "John Updated", "age": 21, "grade": "A"}
# Replaces entire student record
```

#### PATCH
**What it does:** Updates only provided fields (partial update)
**Example:**
```python
PATCH /api/students/1/
Body: {"age": 21}  # Only update age
# Other fields remain unchanged
```

#### DELETE
**What it does:** Removes a resource
**Example:**
```python
DELETE /api/students/1/
# Response: 204 No Content (empty)
```

### HTTP Status Codes

**Definition:** Status codes tell you if the request succeeded or failed, and why.

**Real-life example:**
Like traffic lights:
- **Green (2xx)** = Go ahead, success
- **Yellow (3xx)** = Redirect, go somewhere else
- **Red (4xx)** = Stop, you made a mistake
- **Red (5xx)** = Stop, server has a problem

**Common Status Codes:**

#### 2xx Success
- **200 OK** - Request succeeded
- **201 Created** - Resource created successfully
- **204 No Content** - Success but no content to return (DELETE)
- **202 Accepted** - Request accepted for processing (async)

#### 3xx Redirection
- **301 Moved Permanently** - Resource moved permanently
- **302 Found** - Temporary redirect
- **304 Not Modified** - Resource not changed (caching)

#### 4xx Client Error
- **400 Bad Request** - Invalid request data
- **401 Unauthorized** - Authentication required
- **403 Forbidden** - Permission denied
- **404 Not Found** - Resource doesn't exist
- **405 Method Not Allowed** - HTTP method not allowed
- **409 Conflict** - Resource conflict (e.g., duplicate)
- **422 Unprocessable Entity** - Validation error
- **429 Too Many Requests** - Rate limit exceeded

#### 5xx Server Error
- **500 Internal Server Error** - Server error
- **502 Bad Gateway** - Gateway error
- **503 Service Unavailable** - Service temporarily unavailable

**Example:**
```python
# Import status codes from DRF
# status: Module containing HTTP status code constants
from rest_framework import status
# Import Response class for API responses
from rest_framework.response import Response

# Success response (201 Created)
# Response(): Creates HTTP response object
# data: Response body (dict/list - automatically serialized to JSON)
# status: HTTP status code (201 = resource created)
# Alternative: HttpResponse (Django's response, but doesn't auto-serialize)
# Difference: Response auto-serializes to JSON, HttpResponse requires manual serialization
return Response(data, status=status.HTTP_201_CREATED)  # 201

# Error response (404 Not Found)
# {'error': 'Not found'}: Error message in response body
# status.HTTP_404_NOT_FOUND: Constant for 404 status code
# Alternative: raise NotFound() exception (DRF handles response automatically)
# Difference: Response() gives full control, exceptions are cleaner but less flexible
return Response({'error': 'Not found'}, 
                status=status.HTTP_404_NOT_FOUND)  # 404

# Validation error (400 Bad Request)
# serializer.errors: Dictionary of validation errors from serializer
# status.HTTP_400_BAD_REQUEST: Constant for 400 status code
# Alternative: raise ValidationError() (DRF handles automatically)
# Difference: Response() for custom format, ValidationError for standard format
return Response(serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST)  # 400

# Other common status codes:
# status.HTTP_200_OK (200) - Success
# status.HTTP_204_NO_CONTENT (204) - Success, no content (DELETE)
# status.HTTP_401_UNAUTHORIZED (401) - Not authenticated
# status.HTTP_403_FORBIDDEN (403) - Authenticated but no permission
# status.HTTP_500_INTERNAL_SERVER_ERROR (500) - Server error
```

### Request Object

**Definition:** The request object contains all information about the incoming HTTP request.

**Real-life example:**
Like a package delivery - the request object contains:
- Who sent it (user)
- What they want (data)
- How they sent it (method)
- Additional info (headers, query params)

**Request Properties:**
```python
# request: DRF Request object (extends Django's HttpRequest)
# Wraps Django's HttpRequest with additional DRF functionality

# request.method: HTTP method as string
# Values: 'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD'
# Alternative: request.META.get('REQUEST_METHOD') (Django's way)
# Difference: request.method is cleaner, META is lower-level
request.method        # 'GET', 'POST', etc.

# request.data: Parsed request body (dict/list)
# - Automatically parses JSON, form data, multipart
# - Works for POST, PUT, PATCH
# - Empty dict for GET/DELETE
# Alternative: request.POST (form data only), request.body (raw bytes)
# Difference: data is parsed and works with all content types, POST is form-only
request.data          # Request body (POST/PUT data)

# request.query_params: URL query parameters (?page=2&search=test)
# - Dictionary-like object
# - Case-insensitive keys
# - Multiple values supported
# Alternative: request.GET (Django's way, same functionality)
# Difference: query_params is DRF naming, GET is Django naming (both work)
request.query_params  # URL parameters (?page=2)

# request.user: Authenticated user
# - Set by authentication classes
# - AnonymousUser if not authenticated
# - User object if authenticated
# Alternative: request.META.get('REMOTE_USER') (if using basic auth)
# Difference: user is set by DRF auth, META is raw HTTP
request.user          # Authenticated user

# request.headers: HTTP headers (case-insensitive dict)
# - Access headers easily
# - request.headers.get('Authorization')
# Alternative: request.META (prefixed with HTTP_, uppercase, underscores)
# Difference: headers is cleaner (Authorization), META is HTTP_AUTHORIZATION
request.headers       # HTTP headers

# request.META: All request metadata (Django's HttpRequest.META)
# - Contains headers, server info, etc.
# - Headers prefixed with HTTP_ and uppercased
# - Use when you need low-level access
request.META          # All metadata

# request.path: URL path without query string
# - Example: '/api/students/1/'
# Alternative: request.get_full_path() (includes query string)
# Difference: path is just path, get_full_path() includes ?page=2
request.path          # URL path

# request.body: Raw request body as bytes
# - Unparsed bytes
# - Use for custom parsing or binary data
# Alternative: request.data (parsed, recommended)
# Difference: body is raw bytes, data is parsed dict/list
request.body          # Raw request body
```

**Example:**
```python
from rest_framework.views import APIView
from rest_framework.response import Response

class MyView(APIView):
    def get(self, request):
        # Get HTTP method
        method = request.method  # 'GET'
        
        # Get query parameters
        page = request.query_params.get('page', 1)
        search = request.query_params.get('search', '')
        
        # Get authenticated user
        user = request.user
        
        # Get headers
        content_type = request.headers.get('Content-Type')
        
        return Response({
            'method': method,
            'page': page,
            'user': user.username if user.is_authenticated else None
        })
    
    def post(self, request):
        # Get request body data
        name = request.data.get('name')
        age = request.data.get('age')
        
        # Validate and process
        return Response({'message': 'Created'}, status=201)
```

### Response Object

**Definition:** The response object is what you send back to the client.

**Real-life example:**
Like a reply letter - contains the answer and status.

**Response Creation:**
```python
from rest_framework.response import Response
from rest_framework import status

# Simple response
return Response({'message': 'Success'})

# With status code
return Response(data, status=status.HTTP_201_CREATED)

# With headers
return Response(data, headers={'X-Custom': 'value'})

# With both
return Response(
    {'data': data},
    status=status.HTTP_200_OK,
    headers={'X-Total-Count': str(count)}
)
```

**Example in View:**
```python
class StudentViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
```

### Content Negotiation

**Definition:** Content negotiation determines the format of the response (JSON, XML, etc.) based on client preferences.

**Real-life example:**
Like a restaurant asking "English or Spanish menu?" - the server provides the format the client prefers.

**How it works:**
```python
# Client sends: Accept: application/json
# Server responds in JSON

# Client sends: Accept: application/xml
# Server responds in XML
```

**DRF Configuration:**
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
}
```

**Example:**
```python
# Client request with Accept header
GET /api/students/
Headers: Accept: application/json

# Server responds with JSON
Response: {"id": 1, "name": "John"}

# Client can also request HTML (Browsable API)
Headers: Accept: text/html
# Server responds with HTML interface
```

### Headers Handling

**Definition:** HTTP headers provide metadata about the request/response.

**Real-life example:**
Like envelope information on a letter - sender, recipient, special instructions.

**Common Headers:**
```python
# Authentication
headers = {'Authorization': 'Token abc123'}

# Content type
headers = {'Content-Type': 'application/json'}

# Custom headers
headers = {'X-API-Version': '1.0'}

# CORS headers
headers = {'Access-Control-Allow-Origin': '*'}
```

**Reading Headers in View:**
```python
class MyView(APIView):
    def get(self, request):
        # Read custom header
        api_version = request.headers.get('X-API-Version', '1.0')
        
        # Read authorization header
        auth_header = request.headers.get('Authorization', '')
        
        # Read content type
        content_type = request.headers.get('Content-Type', '')
        
        return Response({'version': api_version})
```

**Setting Headers in Response:**
```python
class MyView(APIView):
    def get(self, request):
        data = {'message': 'Success'}
        
        return Response(
            data,
            headers={
                'X-Custom-Header': 'value',
                'X-Request-ID': str(uuid.uuid4()),
                'Cache-Control': 'no-cache'
            }
        )
```

### Query Params vs Body Params

**Definition:**
- **Query Params** - In URL after `?` (for GET requests)
- **Body Params** - In request body (for POST/PUT requests)

**Real-life example:**
- **Query params** = Like asking "Show me red shirts" (filtering)
- **Body params** = Like filling out a form (creating/updating)

**Example:**
```python
# Query params (GET)
GET /api/students/?age=20&grade=A&page=2
# request.query_params = {'age': '20', 'grade': 'A', 'page': '2'}

# Body params (POST)
POST /api/students/
Body: {"name": "John", "age": 20}
# request.data = {'name': 'John', 'age': 20}
```

**Using Query Params:**
```python
class StudentViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Student.objects.all()
        
        # Get query params
        age = self.request.query_params.get('age')
        grade = self.request.query_params.get('grade')
        
        # Filter based on query params
        if age:
            queryset = queryset.filter(age=age)
        if grade:
            queryset = queryset.filter(grade=grade)
        
        return queryset
```

**Using Body Params:**
```python
class StudentViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        # Body params are in request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(serializer.data, status=201)
```

**When to Use Which:**
- **Query Params**: Filtering, searching, pagination, sorting (GET requests)
- **Body Params**: Creating, updating resources (POST, PUT, PATCH requests)

---

## 🎓 Advanced Interview Topics (4+ Years Experience)

### HTTP/2 and HTTP/3

**HTTP/2 Benefits:**
- Multiplexing (multiple requests over single connection)
- Header compression
- Server push
- Better performance

**HTTP/3 (QUIC):**
- Built on UDP instead of TCP
- Faster connection establishment
- Better for mobile networks

**Django Support:**
```python
# Django supports HTTP/2 via ASGI
# Use Daphne or Uvicorn as ASGI server
# settings.py
ASGI_APPLICATION = 'myproject.asgi.application'

# Install: pip install daphne
# Run: daphne -p 8000 myproject.asgi:application
```

### Content Negotiation Deep Dive

**1. Custom Renderers:**
```python
from rest_framework.renderers import BaseRenderer

class XMLRenderer(BaseRenderer):
    media_type = 'application/xml'
    format = 'xml'
    
    def render(self, data, media_type=None, renderer_context=None):
        # Convert data to XML
        return xml_serialize(data)

# In settings.py
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'myapp.renderers.XMLRenderer',
    ],
}
```

**2. Version-Based Content Negotiation:**
```python
class VersionedRenderer(BaseRenderer):
    def render(self, data, media_type=None, renderer_context=None):
        request = renderer_context['request']
        version = request.version
        
        if version == 'v2':
            # Different format for v2
            return self.render_v2(data)
        return self.render_v1(data)
```

### HTTP Caching Strategies

**1. ETag Support:**
```python
from django.utils.http import http_date
from django.views.decorators.http import condition

def etag_func(request, *args, **kwargs):
    # Generate ETag from resource
    student = get_object_or_404(Student, pk=kwargs['pk'])
    return str(hash(student.updated_at))

@condition(etag_func=etag_func)
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return Response(StudentSerializer(student).data)
```

**2. Cache-Control Headers:**
```python
class StudentViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # Add cache headers
        response['Cache-Control'] = 'public, max-age=3600'  # 1 hour
        response['ETag'] = self.generate_etag()
        return response
```

### Request/Response Middleware

**1. Custom Request Processing:**
```python
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Log request
        logger.info(f"{request.method} {request.path}")
        
        # Add custom attribute
        request.custom_data = {'processed_at': timezone.now()}
        
        response = self.get_response(request)
        
        # Log response
        logger.info(f"Response: {response.status_code}")
        
        return response
```

**2. Response Transformation:**
```python
class ResponseEnvelopeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Wrap API responses in envelope
        if request.path.startswith('/api/'):
            if hasattr(response, 'data'):
                response.data = {
                    'success': response.status_code < 400,
                    'data': response.data,
                    'timestamp': timezone.now().isoformat()
                }
        
        return response
```

### HTTP Security Headers

**1. Security Headers:**
```python
# django-cors-headers for CORS
INSTALLED_APPS = ['corsheaders']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware']

CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://www.example.com",
]

# Security headers middleware
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

**2. Custom Security Headers:**
```python
class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response
```

### HTTP Compression

**1. GZIP Compression:**
```python
# Django's GZipMiddleware
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    # ... other middleware
]

# Compresses responses > 200 bytes
# Saves bandwidth, improves performance
```

**2. Custom Compression:**
```python
class SelectiveCompressionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Only compress JSON responses
        if (response.get('Content-Type', '').startswith('application/json') and
            len(response.content) > 1024):  # > 1KB
            response = self.compress_response(response)
        
        return response
```

### HTTP/2 Server Push

**1. Preloading Resources:**
```python
class ResourcePreloadMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Add Link header for HTTP/2 push
        if request.path == '/api/students/':
            response['Link'] = '</api/students/?page=2>; rel=prefetch'
        
        return response
```

### Request Validation

**1. Size Limits:**
```python
class RequestSizeMiddleware:
    MAX_REQUEST_SIZE = 10 * 1024 * 1024  # 10MB
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.method in ['POST', 'PUT', 'PATCH']:
            content_length = request.META.get('CONTENT_LENGTH', 0)
            if int(content_length) > self.MAX_REQUEST_SIZE:
                return JsonResponse(
                    {'error': 'Request too large'},
                    status=413
                )
        
        return self.get_response(request)
```

### HTTP Status Code Best Practices

**When to Use Each Status Code:**

| Status | Use Case | Example |
|--------|----------|---------|
| 200 | Successful GET, PUT, PATCH | Resource retrieved/updated |
| 201 | Resource created | POST creates new resource |
| 202 | Accepted for processing | Async task started |
| 204 | Success, no content | DELETE successful |
| 400 | Bad request (client error) | Invalid data format |
| 401 | Not authenticated | Missing/invalid token |
| 403 | Forbidden | Authenticated but no permission |
| 404 | Not found | Resource doesn't exist |
| 409 | Conflict | Duplicate resource |
| 422 | Unprocessable entity | Validation failed |
| 429 | Too many requests | Rate limit exceeded |
| 500 | Server error | Unexpected error |
| 503 | Service unavailable | Maintenance mode |

---

*This guide covers essential and advanced HTTP concepts. Master these for senior Django REST Framework positions.*

