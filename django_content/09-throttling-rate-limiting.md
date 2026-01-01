# Throttling / Rate Limiting

## 🚦 Throttling

### What is Throttling?

**Definition:** Throttling limits the number of requests a client can make within a time period.

**Real-life example:**
Like limiting how many times you can use a vending machine per hour to prevent abuse.

### Anonymous Throttling

**Definition:** Anonymous throttling limits requests from unauthenticated users.

**Example:**
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',  # 100 requests per hour for anonymous users
    }
}
```

**Usage:**
```python
from rest_framework.viewsets import ModelViewSet

class BookViewSet(ModelViewSet):
    # Uses default throttle classes
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
# Anonymous users: 100 requests/hour
# Authenticated users: unlimited (unless specified)
```

**Custom Anonymous Rate:**
```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'anon': '50/hour',  # More restrictive
    }
}
```

### User-based Throttling

**Definition:** User-based throttling limits requests per authenticated user.

**Example:**
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/hour',  # 1000 requests per hour per user
    }
}
```

**Usage:**
```python
class BookViewSet(ModelViewSet):
    # Uses default throttle classes (UserRateThrottle)
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

**Per-view Throttling:**
```python
from rest_framework.throttling import UserRateThrottle

class HighRateThrottle(UserRateThrottle):
    scope = 'high_rate'

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'high_rate': '5000/hour',
    }
}

# In view
class BookViewSet(ModelViewSet):
    throttle_classes = [HighRateThrottle]
    throttle_scope = 'high_rate'
```

### Scoped Throttling

**Definition:** Scoped throttling allows different rates for different views/actions.

**Example:**
```python
from rest_framework.throttling import ScopedRateThrottle

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'books': '100/hour',
        'orders': '20/hour',
        'payments': '10/hour',
    }
}

# In views
class BookViewSet(ModelViewSet):
    throttle_scope = 'books'  # 100/hour
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class OrderViewSet(ModelViewSet):
    throttle_scope = 'orders'  # 20/hour
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class PaymentViewSet(ModelViewSet):
    throttle_scope = 'payments'  # 10/hour
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
```

### Custom Throttles

**Definition:** Custom throttles allow you to create your own rate limiting logic.

**Example:**
```python
from rest_framework.throttling import BaseThrottle
from django.core.cache import cache
import time

class CustomRateThrottle(BaseThrottle):
    def allow_request(self, request, view):
        # Get user identifier
        if request.user.is_authenticated:
            ident = request.user.id
        else:
            ident = self.get_ident(request)
        
        # Check rate limit
        key = f'throttle_{ident}'
        history = cache.get(key, [])
        
        # Remove old entries (older than 1 hour)
        now = time.time()
        history = [h for h in history if h > now - 3600]
        
        # Check if limit exceeded
        if len(history) >= 100:  # 100 requests per hour
            return False
        
        # Add current request
        history.append(now)
        cache.set(key, history, 3600)
        return True
    
    def wait(self):
        # Return seconds to wait
        return 60

# Usage
class BookViewSet(ModelViewSet):
    throttle_classes = [CustomRateThrottle]
```

**IP-based Throttling:**
```python
from rest_framework.throttling import BaseThrottle
from django.core.cache import cache

class IPRateThrottle(BaseThrottle):
    def allow_request(self, request, view):
        ip = self.get_ident(request)
        key = f'ip_throttle_{ip}'
        count = cache.get(key, 0)
        
        if count >= 200:  # 200 requests per hour
            return False
        
        cache.set(key, count + 1, 3600)
        return True

class BookViewSet(ModelViewSet):
    throttle_classes = [IPRateThrottle]
```

### Per-role/per-API Limits

**Definition:** Different rate limits for different user roles or API endpoints.

**Example:**
```python
from rest_framework.throttling import UserRateThrottle

class RoleBasedThrottle(UserRateThrottle):
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            # Different rates for different roles
            if request.user.is_staff:
                self.scope = 'admin'  # Higher limit
            elif request.user.groups.filter(name='Premium').exists():
                self.scope = 'premium'
            else:
                self.scope = 'user'
        return super().get_cache_key(request, view)

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'admin': '10000/hour',
        'premium': '5000/hour',
        'user': '1000/hour',
    }
}

# Usage
class BookViewSet(ModelViewSet):
    throttle_classes = [RoleBasedThrottle]
```

**Per-API Endpoint Limits:**
```python
class EndpointThrottle(UserRateThrottle):
    def get_cache_key(self, request, view):
        # Include endpoint in cache key
        key = super().get_cache_key(request, view)
        endpoint = f"{request.method}:{view.__class__.__name__}"
        return f"{key}:{endpoint}"

# Different limits per endpoint
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'books': '1000/hour',
        'orders': '100/hour',
        'payments': '50/hour',
    }
}

class BookViewSet(ModelViewSet):
    throttle_classes = [EndpointThrottle]
    throttle_scope = 'books'
```

### Throttle Response Headers

**Definition:** Throttle response headers inform clients about rate limit status.

**Example:**
```python
# DRF automatically adds headers:
# X-RateLimit-Limit: Maximum requests allowed
# X-RateLimit-Remaining: Remaining requests
# X-RateLimit-Reset: When limit resets

# Custom throttle can add more headers
class CustomThrottle(UserRateThrottle):
    def allow_request(self, request, view):
        allowed = super().allow_request(request, view)
        
        if not allowed:
            # Add wait time header
            wait_time = self.wait()
            # This is handled by DRF automatically
        
        return allowed
```

**Response Example:**
```
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1640995200
Retry-After: 3600
```

### Handling Throttle Exceptions

**Definition:** Custom exception handling for throttle violations.

**Example:**
```python
from rest_framework.exceptions import Throttled
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if isinstance(exc, Throttled):
        # Custom response format
        custom_response_data = {
            'error': 'Rate limit exceeded',
            'detail': str(exc.detail),
            'wait_seconds': exc.wait if hasattr(exc, 'wait') else None
        }
        response.data = custom_response_data
    
    return response

# settings.py
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'myapp.exceptions.custom_exception_handler',
}
```

### Best Practices

1. **Set appropriate limits:**
   - Too high: Doesn't prevent abuse
   - Too low: Frustrates legitimate users

2. **Use different limits for different endpoints:**
   - Read endpoints: Higher limits
   - Write endpoints: Lower limits

3. **Cache throttle data:**
   - Use Redis for distributed systems
   - Use Django cache for single-server

4. **Monitor throttle violations:**
   - Log throttled requests
   - Alert on unusual patterns

5. **Provide clear error messages:**
   - Tell users when they can retry
   - Include retry-after header

