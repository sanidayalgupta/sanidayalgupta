# Versioning

## 🔄 API Versioning

### What is API Versioning?

**Definition:** API versioning allows you to maintain multiple versions of your API simultaneously, enabling changes without breaking existing clients.

**Real-life example:**
Like phone operating system versions - iOS 15 and iOS 16 coexist, so old apps still work while new features are available.

### URL Versioning

**Definition:** URL versioning includes the version number in the URL path.

**Example:**
```python
# urls.py
urlpatterns = [
    path('api/v1/students/', StudentViewSetV1.as_view()),
    path('api/v2/students/', StudentViewSetV2.as_view()),
]
```

**Using DRF's URLVersioning:**
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
    'DEFAULT_VERSION': 'v1',
}

# urls.py
urlpatterns = [
    path('api/<version>/students/', StudentViewSet.as_view()),
]
```

**In ViewSet:**
```python
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    def get_serializer_class(self):
        """Use different serializer based on version"""
        if self.request.version == 'v2':
            return StudentSerializerV2
        return StudentSerializer
```

### Header Versioning

**Definition:** Header versioning uses HTTP headers to specify the API version.

**Example:**
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
    'DEFAULT_VERSION': 'v1',
}

# Client sends:
# Accept: application/json; version=v2
```

**Usage:**
```python
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    def get_serializer_class(self):
        version = self.request.version
        if version == 'v2':
            return StudentSerializerV2
        return StudentSerializer
```

### Namespace Versioning

**Definition:** Namespace versioning uses URL namespaces to separate versions.

**Example:**
```python
# urls.py
urlpatterns = [
    path('api/v1/', include('api.v1.urls', namespace='v1')),
    path('api/v2/', include('api.v2.urls', namespace='v2')),
]

# api/v1/urls.py
app_name = 'v1'
urlpatterns = [
    path('students/', StudentViewSet.as_view()),
]

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
}
```

### Versioned Serializers & Views

**Definition:** Using different serializers and views for different API versions.

**Serializer Versioning:**
```python
class StudentSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'email']

class StudentSerializerV2(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    contact_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = ['id', 'full_name', 'contact_info', 'metadata']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    def get_contact_info(self, obj):
        return {
            'email': obj.email,
            'phone': obj.phone
        }

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    
    def get_serializer_class(self):
        version = self.request.version
        
        if version == 'v2':
            return StudentSerializerV2
        elif version == 'v1':
            return StudentSerializerV1
        
        return StudentSerializerV1
```

**ViewSet Versioning:**
```python
# api/v1/views.py
class StudentViewSetV1(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializerV1

# api/v2/views.py
class StudentViewSetV2(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializerV2
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """New endpoint in v2"""
        student = self.get_object()
        return Response({
            'total_orders': student.orders.count(),
            'total_spent': student.orders.aggregate(Sum('total'))['total__sum']
        })
```

### Backward Compatibility

**Definition:** Backward compatibility ensures old API versions continue to work when new versions are released.

**Strategy 1: Keep Old Endpoints**
```python
# Keep v1 endpoint working
class StudentViewSetV1(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializerV1

# Add v2 with new features
class StudentViewSetV2(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializerV2
```

**Strategy 2: Deprecation Warnings**
```python
from rest_framework.response import Response
from rest_framework import status

class StudentViewSetV1(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializerV1
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # Add deprecation warning
        response['X-API-Deprecated'] = 'true'
        response['X-API-Deprecation-Date'] = '2024-12-31'
        response['X-API-Sunset-Date'] = '2025-12-31'
        response['X-API-Replacement'] = '/api/v2/students/'
        return response
```

**Strategy 3: Feature Flags**
```python
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    
    def get_serializer_class(self):
        version = self.request.version
        
        # v2 has new fields
        if version == 'v2':
            return StudentSerializerV2
        
        # v1 keeps old format
        return StudentSerializerV1
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # v2 has new filtering
        if self.request.version == 'v2':
            return queryset.filter(is_active=True)
        
        return queryset
```

**Strategy 4: Adapter Pattern**
```python
class VersionAdapter:
    """Adapt v1 requests to work with v2 models"""
    
    @staticmethod
    def adapt_request_data_v1_to_v2(data):
        """Convert v1 request format to v2"""
        adapted = data.copy()
        if 'name' in adapted:
            # Split name into first_name and last_name for v2
            parts = adapted.pop('name').split(' ', 1)
            adapted['first_name'] = parts[0]
            adapted['last_name'] = parts[1] if len(parts) > 1 else ''
        return adapted

class StudentViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        # Adapt v1 format to v2 if needed
        if request.version == 'v1':
            request.data._mutable = True
            request.data.update(
                VersionAdapter.adapt_request_data_v1_to_v2(request.data)
            )
            request.data._mutable = False
        
        return super().create(request, *args, **kwargs)
```

### Complete Example

**Real Project Example:**
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
    'DEFAULT_VERSION': 'v1',
    'VERSION_PARAM': 'version',
}

# urls.py
urlpatterns = [
    path('api/<version>/students/', StudentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('api/<version>/students/<int:pk>/', StudentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
]

# serializers.py
class StudentSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'age']

class StudentSerializerV2(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    contact = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = ['id', 'full_name', 'contact', 'age', 'metadata']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    def get_contact(self, obj):
        return {
            'email': obj.email,
            'phone': obj.phone,
            'address': obj.address
        }

# views.py
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    
    def get_serializer_class(self):
        version = self.request.version
        if version == 'v2':
            return StudentSerializerV2
        return StudentSerializerV1
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        # Add version info and deprecation warning for v1
        if request.version == 'v1':
            response['X-API-Version'] = 'v1'
            response['X-API-Deprecated'] = 'true'
            response['X-API-Sunset-Date'] = '2025-12-31'
        
        return response
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """New endpoint only in v2"""
        if request.version != 'v2':
            return Response(
                {'error': 'This endpoint is only available in v2'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        student = self.get_object()
        return Response({
            'total_courses': student.courses.count(),
            'average_grade': student.courses.aggregate(Avg('grade'))['grade__avg']
        })
```

### Best Practices

1. **Plan versioning strategy early:** Decide on versioning approach from start
2. **Document version differences:** Clearly document what changed
3. **Set deprecation timelines:** Give clients time to migrate
4. **Maintain backward compatibility:** Don't break existing clients
5. **Use semantic versioning:** Follow v1, v2, v3 pattern
6. **Limit number of versions:** Don't maintain too many versions
7. **Provide migration guides:** Help clients upgrade
8. **Monitor version usage:** Track which versions are still in use

