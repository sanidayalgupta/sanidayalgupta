# Monitoring & Logging

## 📊 Monitoring & Logging

### What is API Logging?

**Definition:** API logging records events, requests, and errors for debugging and monitoring.

**Real-life example:**
Like a security camera system - records what happens so you can review later.

### API Logging

**Basic Logging:**
```python
import logging

logger = logging.getLogger(__name__)

class StudentViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        logger.info(f"Creating student: {request.data}")
        response = super().create(request, *args, **kwargs)
        logger.info(f"Student created: {response.data['id']}")
        return response
```

**Structured Logging:**
```python
import logging
import json

logger = logging.getLogger(__name__)

class StudentViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        logger.info('Student creation started', extra={
            'user_id': request.user.id,
            'data': request.data,
            'ip_address': request.META.get('REMOTE_ADDR'),
        })
        
        try:
            response = super().create(request, *args, **kwargs)
            logger.info('Student created successfully', extra={
                'student_id': response.data['id'],
                'user_id': request.user.id,
            })
            return response
        except Exception as e:
            logger.error('Student creation failed', extra={
                'error': str(e),
                'user_id': request.user.id,
                'data': request.data,
            }, exc_info=True)
            raise
```

**Logging Configuration:**
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/api.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'myapp': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

### Audit Logs

**Definition:** Audit logs record important actions for compliance and security auditing.

**Model for Audit Logs:**
```python
class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)  # CREATE, UPDATE, DELETE
    model_name = models.CharField(max_length=100)
    object_id = models.IntegerField()
    changes = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['model_name', 'object_id']),
        ]
```

**Audit Log Middleware:**
```python
from .models import AuditLog

class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Log important actions
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            if request.user.is_authenticated:
                AuditLog.objects.create(
                    user=request.user,
                    action=request.method,
                    model_name=self.get_model_name(request.path),
                    object_id=self.get_object_id(request.path),
                    ip_address=self.get_client_ip(request),
                    changes=request.data if hasattr(request, 'data') else {},
                )
        
        return response
    
    def get_model_name(self, path):
        # Extract model name from path
        parts = path.strip('/').split('/')
        return parts[-2] if len(parts) > 1 else 'unknown'
    
    def get_object_id(self, path):
        # Extract object ID from path
        parts = path.strip('/').split('/')
        return int(parts[-1]) if parts[-1].isdigit() else None
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
```

**Signal-based Audit Logging:**
```python
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save)
def log_model_save(sender, instance, created, **kwargs):
    """Log model saves"""
    if sender.__name__ in ['AuditLog', 'LogEntry']:
        return  # Don't log audit logs
    
    action = 'CREATE' if created else 'UPDATE'
    AuditLog.objects.create(
        user=get_current_user(),
        action=action,
        model_name=sender.__name__,
        object_id=instance.id,
        changes=get_model_changes(instance),
    )

@receiver(post_delete)
def log_model_delete(sender, instance, **kwargs):
    """Log model deletes"""
    AuditLog.objects.create(
        user=get_current_user(),
        action='DELETE',
        model_name=sender.__name__,
        object_id=instance.id,
        changes={'deleted': True},
    )
```

### Error Tracking

**Definition:** Error tracking captures and aggregates exceptions for debugging.

**Using Sentry:**
```bash
pip install sentry-sdk
```

```python
# settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)

# Automatically captures exceptions
```

**Custom Error Tracking:**
```python
import logging
from .models import ErrorLog

class ErrorTrackingHandler(logging.Handler):
    """Custom handler to log errors to database"""
    
    def emit(self, record):
        try:
            ErrorLog.objects.create(
                level=record.levelname,
                message=record.getMessage(),
                module=record.module,
                function=record.funcName,
                line_number=record.lineno,
                traceback=self.format(record),
            )
        except Exception:
            self.handleError(record)

# Add to logging config
LOGGING = {
    'handlers': {
        'error_tracking': {
            '()': ErrorTrackingHandler,
            'level': 'ERROR',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['error_tracking'],
        },
    },
}
```

### Monitoring Concepts

**Definition:** Monitoring tracks API performance, availability, and usage metrics.

**Key Metrics:**
- Request rate (requests per second)
- Response times (latency)
- Error rates
- Success/failure rates
- Active users

**Basic Monitoring Middleware:**
```python
import time
from django.core.cache import cache

class MonitoringMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        start_time = time.time()
        
        response = self.get_response(request)
        
        duration = time.time() - start_time
        
        # Track metrics
        self.track_metrics(request, response, duration)
        
        return response
    
    def track_metrics(self, request, response, duration):
        # Increment request counter
        cache.incr('api:requests:total')
        cache.incr(f'api:requests:{request.method.lower()}')
        
        # Track response time
        cache.lpush('api:response_times', duration)
        cache.ltrim('api:response_times', 0, 999)  # Keep last 1000
        
        # Track status codes
        cache.incr(f'api:status:{response.status_code}')
        
        # Track errors
        if response.status_code >= 400:
            cache.incr('api:errors:total')
```

### Metrics Exposure

**Definition:** Exposing metrics for monitoring systems like Prometheus.

**Using django-prometheus:**
```bash
pip install django-prometheus
```

```python
# settings.py
INSTALLED_APPS = [
    'django_prometheus',
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    # ... other middleware
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

# urls.py
urlpatterns = [
    path('', include('django_prometheus.urls')),
]

# Access metrics at /metrics
```

**Custom Metrics Endpoint:**
```python
from django.http import JsonResponse
from django.core.cache import cache

class MetricsView(APIView):
    def get(self, request):
        """Expose API metrics"""
        metrics = {
            'requests': {
                'total': cache.get('api:requests:total', 0),
                'by_method': {
                    'get': cache.get('api:requests:get', 0),
                    'post': cache.get('api:requests:post', 0),
                    'put': cache.get('api:requests:put', 0),
                    'delete': cache.get('api:requests:delete', 0),
                },
            },
            'errors': {
                'total': cache.get('api:errors:total', 0),
                'by_status': {
                    '400': cache.get('api:status:400', 0),
                    '401': cache.get('api:status:401', 0),
                    '403': cache.get('api:status:403', 0),
                    '404': cache.get('api:status:404', 0),
                    '500': cache.get('api:status:500', 0),
                },
            },
            'performance': {
                'avg_response_time': self.calculate_avg_response_time(),
            },
        }
        return JsonResponse(metrics)
    
    def calculate_avg_response_time(self):
        times = cache.lrange('api:response_times', 0, -1)
        if times:
            return sum(float(t) for t in times) / len(times)
        return 0
```

### Best Practices

1. **Log at appropriate levels:** DEBUG, INFO, WARNING, ERROR, CRITICAL
2. **Include context:** User ID, IP address, request ID
3. **Don't log sensitive data:** Passwords, tokens, PII
4. **Use structured logging:** JSON format for easier parsing
5. **Set up log rotation:** Prevent log files from growing too large
6. **Monitor error rates:** Alert on high error rates
7. **Track performance metrics:** Response times, throughput
8. **Set up alerts:** Notify on critical errors or high latency

