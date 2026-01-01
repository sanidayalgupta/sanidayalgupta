# API Documentation

## 📚 API Documentation in DRF

### What is API Documentation?

**Definition:** API documentation describes your API endpoints, parameters, and responses, making it easy for developers to use your API.

**Real-life example:**
Like a user manual for your API - shows what endpoints exist, what they do, and how to use them.

### Browsable API

**Definition:** Browsable API is DRF's built-in HTML interface for exploring and testing APIs.

**How to Access:**
```python
# Already enabled by default in DRF
# Visit: http://localhost:8000/api/endpoint/

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # Enable browsable API
    ],
}
```

**Features:**
- Interactive API exploration
- Form-based testing
- Request/response examples
- Authentication support

### OpenAPI Schema

**Definition:** OpenAPI (formerly Swagger) is a standard format for describing REST APIs.

**Generate Schema:**
```python
# Using drf-spectacular
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import AutoSchema

# settings.py
INSTALLED_APPS = [
    'drf_spectacular',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'My API',
    'DESCRIPTION': 'API documentation',
    'VERSION': '1.0.0',
}

# urls.py
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
```

### Swagger Integration

**Definition:** Swagger provides interactive API documentation with a UI for testing endpoints.

**Using drf-spectacular (Recommended):**
```bash
pip install drf-spectacular
```

```python
# settings.py
INSTALLED_APPS = [
    'drf_spectacular',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'My API',
    'DESCRIPTION': 'Complete API documentation',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
}

# urls.py
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
```

**Annotating Endpoints:**
```python
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

class StudentViewSet(viewsets.ModelViewSet):
    @extend_schema(
        summary='List students',
        description='Retrieve a list of all students',
        parameters=[
            OpenApiParameter(
                name='age',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Filter by age',
            ),
        ],
        responses={200: StudentSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary='Create student',
        request=StudentSerializer,
        responses={201: StudentSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
```

### drf-yasg (Alternative)

**Definition:** drf-yasg is another package for generating Swagger/OpenAPI documentation.

**Setup:**
```bash
pip install drf-yasg
```

```python
# settings.py
INSTALLED_APPS = [
    'drf_yasg',
]

# urls.py
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
```

### drf-spectacular (Recommended)

**Why drf-spectacular:**
- Modern and actively maintained
- Better OpenAPI 3.0 support
- More features and customization
- Better performance

**Advanced Configuration:**
```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'My API',
    'DESCRIPTION': 'Complete API documentation',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'COMPONENT_NO_READ_ONLY_REQUIRED': True,
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'displayOperationId': True,
    },
    'SERVERS': [
        {'url': 'https://api.example.com', 'description': 'Production'},
        {'url': 'https://staging-api.example.com', 'description': 'Staging'},
    ],
}
```

### Versioned Docs

**Definition:** Versioned documentation shows different API versions in separate documentation.

**Setup:**
```python
# Multiple schema views for different versions
from drf_spectacular.views import SpectacularAPIView

class SchemaV1View(SpectacularAPIView):
    schema_generator = SchemaGenerator(patterns=v1_urls, api_version='v1')

class SchemaV2View(SpectacularAPIView):
    schema_generator = SchemaGenerator(patterns=v2_urls, api_version='v2')

# urls.py
urlpatterns = [
    path('api/v1/schema/', SchemaV1View.as_view(), name='schema-v1'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema-v1'), name='swagger-v1'),
    path('api/v2/schema/', SchemaV2View.as_view(), name='schema-v2'),
    path('api/v2/docs/', SpectacularSwaggerView.as_view(url_name='schema-v2'), name='swagger-v2'),
]
```

**Using Namespaces:**
```python
# Include versioned URLs
urlpatterns = [
    path('api/v1/', include('api.v1.urls', namespace='v1')),
    path('api/v2/', include('api.v2.urls', namespace='v2')),
]

# Generate versioned schemas
SPECTACULAR_SETTINGS = {
    'SCHEMA_PATH_PREFIX': '/api/v[0-9]',
}
```

### Complete Example

**Full Setup:**
```python
# settings.py
INSTALLED_APPS = [
    'drf_spectacular',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Student Management API',
    'DESCRIPTION': 'Complete API for managing students',
    'VERSION': '1.0.0',
    'CONTACT': {
        'name': 'API Support',
        'email': 'support@example.com',
    },
    'LICENSE': {
        'name': 'MIT License',
    },
    'TAGS': [
        {'name': 'students', 'description': 'Student operations'},
        {'name': 'courses', 'description': 'Course operations'},
    ],
}

# urls.py
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # API endpoints
    path('api/', include('api.urls')),
    
    # Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# views.py
from drf_spectacular.utils import extend_schema, OpenApiResponse

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    @extend_schema(
        tags=['students'],
        summary='List all students',
        description='Retrieve a paginated list of all students',
        responses={200: StudentSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        tags=['students'],
        summary='Create a new student',
        request=StudentSerializer,
        responses={
            201: OpenApiResponse(response=StudentSerializer, description='Student created'),
            400: OpenApiResponse(description='Validation error'),
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
```

### Best Practices

1. **Keep documentation up to date:** Update when API changes
2. **Provide examples:** Show request/response examples
3. **Describe parameters:** Explain what each parameter does
4. **Use tags:** Organize endpoints into logical groups
5. **Include error responses:** Document possible errors
6. **Add authentication info:** Explain how to authenticate
7. **Version your docs:** Match API versions
8. **Test your docs:** Make sure examples work

