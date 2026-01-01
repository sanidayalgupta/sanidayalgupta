# Advanced Patterns

## 🚀 Advanced API Patterns

### Multi-Tenant APIs

**Definition:** Multi-tenant APIs serve multiple clients (tenants) from the same application instance, with data isolation.

**Real-life example:**
Like an apartment building - multiple tenants share the building but have separate apartments (data).

**Implementation:**
```python
# Middleware to identify tenant
class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Get tenant from header, subdomain, or path
        tenant_id = (
            request.headers.get('X-Tenant-ID') or
            request.GET.get('tenant_id') or
            self.get_tenant_from_subdomain(request)
        )
        
        request.tenant_id = tenant_id
        return self.get_response(request)
    
    def get_tenant_from_subdomain(self, request):
        host = request.get_host().split('.')[0]
        return host

# Model with tenant isolation
class TenantModel(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    
    class Meta:
        abstract = True

class Student(TenantModel):
    name = models.CharField(max_length=100)

# ViewSet with tenant filtering
class StudentViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        tenant_id = self.request.tenant_id
        return Student.objects.filter(tenant_id=tenant_id)
    
    def perform_create(self, serializer):
        serializer.save(tenant_id=self.request.tenant_id)
```

### API Gateway Concepts

**Definition:** API Gateway is a single entry point that routes requests to appropriate services.

**Real-life example:**
Like a reception desk - all visitors go through one point, which directs them to the right department.

**Key Functions:**
- Request routing
- Authentication/Authorization
- Rate limiting
- Request/Response transformation
- Load balancing
- API versioning

**Simple Gateway Pattern:**
```python
# Gateway service routes to microservices
class APIGatewayView(APIView):
    def dispatch(self, request, *args, **kwargs):
        service = self.get_service(request.path)
        
        if service == 'students':
            return self.forward_to_student_service(request)
        elif service == 'courses':
            return self.forward_to_course_service(request)
        
        return Response({'error': 'Service not found'}, status=404)
    
    def forward_to_student_service(self, request):
        # Forward request to student service
        response = requests.request(
            method=request.method,
            url=f'{STUDENT_SERVICE_URL}{request.path}',
            headers=dict(request.headers),
            data=request.body,
        )
        return Response(response.json(), status=response.status_code)
```

### Webhooks

**Definition:** Webhooks allow your API to notify external systems when events occur.

**Real-life example:**
Like a doorbell - when someone rings (event happens), you're notified immediately.

**Webhook Model:**
```python
class Webhook(models.Model):
    url = models.URLField()
    events = models.JSONField(default=list)  # ['order.created', 'order.updated']
    secret = models.CharField(max_length=100)  # For signature verification
    is_active = models.BooleanField(default=True)

class WebhookEvent(models.Model):
    webhook = models.ForeignKey(Webhook, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=100)
    payload = models.JSONField()
    status = models.CharField(max_length=20)  # pending, success, failed
    attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
```

**Webhook Sender:**
```python
import hmac
import hashlib
import requests
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender=Order)
def send_order_webhook(sender, instance, created, **kwargs):
    """Send webhook when order is created/updated"""
    event_type = 'order.created' if created else 'order.updated'
    
    webhooks = Webhook.objects.filter(
        events__contains=[event_type],
        is_active=True
    )
    
    for webhook in webhooks:
        send_webhook.delay(webhook.id, event_type, instance.id)

@shared_task
def send_webhook(webhook_id, event_type, object_id):
    """Send webhook in background"""
    webhook = Webhook.objects.get(id=webhook_id)
    
    # Prepare payload
    payload = {
        'event': event_type,
        'data': get_object_data(object_id),
        'timestamp': timezone.now().isoformat(),
    }
    
    # Create signature
    signature = hmac.new(
        webhook.secret.encode(),
        json.dumps(payload).encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Send webhook
    headers = {
        'X-Webhook-Signature': signature,
        'Content-Type': 'application/json',
    }
    
    try:
        response = requests.post(
            webhook.url,
            json=payload,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        
        WebhookEvent.objects.create(
            webhook=webhook,
            event_type=event_type,
            payload=payload,
            status='success',
        )
    except Exception as e:
        WebhookEvent.objects.create(
            webhook=webhook,
            event_type=event_type,
            payload=payload,
            status='failed',
            attempts=1,
        )
        raise
```

### Feature Flags

**Definition:** Feature flags allow enabling/disabling features without code deployment.

**Implementation:**
```python
# Model
class FeatureFlag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_enabled = models.BooleanField(default=False)
    enabled_for_users = models.ManyToManyField(User, blank=True)

# Decorator
def feature_flag_required(flag_name):
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            flag = FeatureFlag.objects.get(name=flag_name)
            
            if not flag.is_enabled:
                if request.user not in flag.enabled_for_users.all():
                    return Response(
                        {'error': 'Feature not available'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator

# Usage
class NewFeatureView(APIView):
    @feature_flag_required('new_feature')
    def get(self, request):
        return Response({'data': 'New feature data'})
```

### API Deprecation Strategy

**Definition:** API deprecation strategy manages the lifecycle of API versions, gradually phasing out old versions.

**Implementation:**
```python
from rest_framework.response import Response

class DeprecatedViewSet(viewsets.ModelViewSet):
    deprecation_date = '2024-12-31'
    sunset_date = '2025-12-31'
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        # Add deprecation headers
        response['X-API-Deprecated'] = 'true'
        response['X-API-Deprecation-Date'] = self.deprecation_date
        response['X-API-Sunset-Date'] = self.sunset_date
        response['X-API-Replacement'] = '/api/v2/students/'
        response['Link'] = f'</api/v2/students/>; rel="successor-version"'
        
        return response
```

### Backward Compatibility Strategy

**Definition:** Backward compatibility ensures old API versions continue working while new features are added.

**Strategies:**
1. **Additive changes only:** Add new fields, don't remove old ones
2. **Version adapters:** Convert between versions
3. **Default values:** Provide defaults for new required fields
4. **Feature detection:** Clients can check for feature availability

**Example:**
```python
class CompatibleViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        version = self.request.version
        
        if version == 'v1':
            return StudentSerializerV1
        elif version == 'v2':
            return StudentSerializerV2
        
        return StudentSerializerV1
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # v2 adds new filtering, v1 keeps old behavior
        if self.request.version == 'v2':
            return queryset.filter(is_active=True)
        
        return queryset
```

### Error Code Standards

**Definition:** Standardizing error codes ensures consistent error responses.

**Standard Format:**
```python
ERROR_CODES = {
    'VALIDATION_ERROR': 'VALIDATION_ERROR',
    'AUTHENTICATION_REQUIRED': 'AUTHENTICATION_REQUIRED',
    'PERMISSION_DENIED': 'PERMISSION_DENIED',
    'NOT_FOUND': 'NOT_FOUND',
    'INSUFFICIENT_STOCK': 'INSUFFICIENT_STOCK',
}

class StandardErrorResponse(Response):
    def __init__(self, error_code, message, details=None, status_code=400, **kwargs):
        response_data = {
            'success': False,
            'error': {
                'code': error_code,
                'message': message,
                'details': details,
            }
        }
        super().__init__(response_data, status=status_code, **kwargs)
```

### Response Consistency

**Definition:** Consistent response format across all endpoints.

**Standard Response:**
```python
class StandardResponse(Response):
    def __init__(self, data=None, message=None, status_code=200, **kwargs):
        response_data = {
            'success': status_code < 400,
            'message': message,
            'data': data,
        }
        super().__init__(response_data, status=status_code, **kwargs)

# Usage
class StudentViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return StandardResponse(
            data=response.data,
            message='Students retrieved successfully'
        )
```

### Large Dataset Streaming Responses

**Definition:** Streaming responses send large datasets in chunks instead of loading everything into memory.

**Example:**
```python
from django.http import StreamingHttpResponse
import csv
import json

class LargeDatasetView(APIView):
    def get(self, request):
        """Stream large dataset as CSV"""
        def generate_csv():
            # Header
            yield 'id,name,email\n'
            
            # Stream data in chunks
            queryset = Student.objects.all()
            batch_size = 1000
            
            for i in range(0, queryset.count(), batch_size):
                batch = queryset[i:i+batch_size]
                for student in batch:
                    yield f'{student.id},{student.name},{student.email}\n'
        
        response = StreamingHttpResponse(generate_csv(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="students.csv"'
        return response
```

### Best Practices

1. **Plan for scale:** Design with multi-tenancy in mind
2. **Use API Gateway:** Centralize common functionality
3. **Implement webhooks properly:** Include retries and signatures
4. **Use feature flags:** Gradual feature rollouts
5. **Plan deprecations:** Give clients time to migrate
6. **Maintain backward compatibility:** Don't break existing clients
7. **Standardize errors:** Consistent error format
8. **Stream large responses:** Don't load everything in memory

---

## 🎓 Advanced Interview Topics (4+ Years Experience)

### Event-Driven Architecture

**1. Django Signals for Events:**
```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Order)
def order_created_handler(sender, instance, created, **kwargs):
    if created:
        # Send to message queue
        send_to_queue('order.created', instance.id)
```

### Circuit Breaker Pattern

**1. Implementing Circuit Breaker:**
```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = 'closed'  # closed, open, half_open
    
    def call(self, func, *args, **kwargs):
        if self.state == 'open':
            if time.time() - self.last_failure_time > self.timeout:
                self.state = 'half_open'
            else:
                raise Exception("Circuit breaker is open")
        
        try:
            result = func(*args, **kwargs)
            if self.state == 'half_open':
                self.state = 'closed'
                self.failures = 0
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            if self.failures >= self.failure_threshold:
                self.state = 'open'
            raise
```

### Saga Pattern

**1. Distributed Transactions:**
```python
class OrderSaga:
    def execute(self, order_data):
        try:
            # Step 1: Create order
            order = self.create_order(order_data)
            
            # Step 2: Reserve inventory
            self.reserve_inventory(order)
            
            # Step 3: Process payment
            self.process_payment(order)
            
            return order
        except Exception as e:
            # Compensate (rollback)
            self.compensate(order)
            raise
```

---

*This guide covers essential and advanced patterns. Master these for senior Django REST Framework positions.*

