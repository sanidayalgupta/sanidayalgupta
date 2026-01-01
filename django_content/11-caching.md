# Caching

## 💾 Caching in DRF

### What is Caching?

**Definition:** Caching stores frequently accessed data in fast memory to avoid expensive database queries or computations.

**Real-life example:**
Like keeping popular items near the front of a store instead of in the warehouse - faster to access.

### Django Caching

**Definition:** Django provides a caching framework that can cache data in memory, database, filesystem, or external cache servers.

**Backend Types:**
```python
# settings.py

# 1. In-memory caching (development)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# 2. Database caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}

# 3. File-based caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}

# 4. Redis (production - recommended)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### API Response Caching

**Definition:** Caching entire API responses to avoid processing the same request multiple times.

**Example:**
```python
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework.decorators import api_view

@api_view(['GET'])
@cache_page(60 * 15)  # Cache for 15 minutes
def student_list(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)
```

**Cache by User:**
```python
from django.views.decorators.vary import vary_on_headers

@api_view(['GET'])
@cache_page(60 * 15)
@vary_on_headers('Authorization')  # Different cache per user
def user_specific_view(request):
    # Cache varies by authentication header
    return Response({'data': 'user-specific'})
```

### Per-View Caching

**Definition:** Caching specific views with custom cache keys and timeouts.

**Using cache_page decorator:**
```python
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from rest_framework.response import Response

class StudentListView(APIView):
    @method_decorator(cache_page(60 * 10))  # 10 minutes
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
```

**Using cache decorator:**
```python
from django.core.cache import cache
from rest_framework.views import APIView

class BookListView(APIView):
    def get(self, request):
        cache_key = 'book_list'
        cached_data = cache.get(cache_key)
        
        if cached_data is None:
            # Data not in cache, fetch from database
            books = Book.objects.all()
            serializer = BookSerializer(books, many=True)
            cached_data = serializer.data
            
            # Store in cache for 1 hour
            cache.set(cache_key, cached_data, 60 * 60)
        
        return Response(cached_data)
```

**Cache Key Patterns:**
```python
from django.core.cache import cache

class BookViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        # Create cache key with query params
        cache_key = f"book_list_{request.GET.urlencode()}"
        cached_data = cache.get(cache_key)
        
        if cached_data is None:
            # Fetch and serialize
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            cached_data = serializer.data
            
            # Cache for 30 minutes
            cache.set(cache_key, cached_data, 60 * 30)
        
        return Response(cached_data)
```

### Redis Basics

**Definition:** Redis is an in-memory data store used for caching, session storage, and message brokering.

**Setup:**
```bash
pip install redis django-redis
```

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'drf_tutorial',  # Prefix all keys
        'TIMEOUT': 300,  # Default timeout (5 minutes)
    }
}
```

**Using Redis directly:**
```python
import redis
from django.conf import settings

redis_client = redis.Redis(
    host=settings.CACHES['default']['LOCATION'].split('://')[1].split('/')[0].split(':')[0],
    port=6379,
    db=1
)

# Set value
redis_client.set('key', 'value', ex=3600)  # Expires in 1 hour

# Get value
value = redis_client.get('key')

# Delete key
redis_client.delete('key')
```

**Advanced Redis Operations:**
```python
from django.core.cache import cache

# Set with timeout
cache.set('key', 'value', timeout=3600)

# Get or set pattern
value = cache.get_or_set('key', lambda: expensive_computation(), timeout=3600)

# Add (only if key doesn't exist)
cache.add('key', 'value', timeout=3600)

# Get multiple keys
values = cache.get_many(['key1', 'key2', 'key3'])

# Set multiple keys
cache.set_many({'key1': 'value1', 'key2': 'value2'}, timeout=3600)

# Delete multiple keys
cache.delete_many(['key1', 'key2'])

# Clear all cache
cache.clear()

# Increment/Decrement (for counters)
cache.incr('counter')  # Increment by 1
cache.decr('counter')  # Decrement by 1
cache.incr('counter', delta=5)  # Increment by 5
```

### Cache Invalidation Strategies

**Definition:** Cache invalidation removes or updates cached data when the underlying data changes.

**Strategy 1: Time-based Expiration**
```python
# Simple - cache expires after time
cache.set('key', 'value', timeout=3600)  # Expires in 1 hour
```

**Strategy 2: Manual Invalidation**
```python
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=Book)
def invalidate_book_cache(sender, instance, **kwargs):
    """Invalidate cache when book is saved"""
    cache.delete('book_list')
    cache.delete(f'book_{instance.id}')

@receiver(post_delete, sender=Book)
def invalidate_book_cache_on_delete(sender, instance, **kwargs):
    """Invalidate cache when book is deleted"""
    cache.delete('book_list')
    cache.delete(f'book_{instance.id}')
```

**Strategy 3: Version-based Cache Keys**
```python
from django.core.cache import cache

def get_cache_key_with_version(base_key, version):
    """Create cache key with version"""
    return f"{base_key}_v{version}"

# When data changes, increment version
cache_version = cache.get('book_list_version', 1)
cache_key = get_cache_key_with_version('book_list', cache_version)
data = cache.get(cache_key)

if data is None:
    data = fetch_data()
    cache.set(cache_key, data, timeout=None)  # No expiration

# To invalidate, just increment version
cache.incr('book_list_version')
```

**Strategy 4: Cache Tags (Redis-specific)**
```python
# Using django-redis with tags
from django_redis import get_redis_connection

redis_client = get_redis_connection("default")

# Set with tags (requires django-redis-cache extension)
# This allows invalidating all keys with a specific tag
redis_client.set('book:1', 'data', tags=['books', 'book:1'])
redis_client.set('book:2', 'data', tags=['books', 'book:2'])

# Invalidate all books
redis_client.delete_pattern('books:*')  # Invalidates all book caches
```

**Strategy 5: Cache Invalidation Mixin**
```python
from django.core.cache import cache
from rest_framework import viewsets

class CacheInvalidationMixin:
    """Mixin to handle cache invalidation"""
    
    cache_keys = []  # Override in subclass
    
    def invalidate_cache(self):
        """Invalidate all cache keys"""
        for key in self.cache_keys:
            cache.delete(key)
    
    def perform_create(self, serializer):
        instance = serializer.save()
        self.invalidate_cache()
        return instance
    
    def perform_update(self, serializer):
        instance = serializer.save()
        self.invalidate_cache()
        return instance
    
    def perform_destroy(self, instance):
        instance.delete()
        self.invalidate_cache()

class BookViewSet(CacheInvalidationMixin, viewsets.ModelViewSet):
    cache_keys = ['book_list', 'book_statistics']
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

**Real Project Example:**
```python
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework import viewsets

def get_book_list_cache_key():
    """Generate cache key for book list"""
    return 'book_list'

def get_book_detail_cache_key(book_id):
    """Generate cache key for book detail"""
    return f'book_{book_id}'

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def list(self, request, *args, **kwargs):
        cache_key = get_book_list_cache_key()
        cached_data = cache.get(cache_key)
        
        if cached_data is None:
            response = super().list(request, *args, **kwargs)
            cache.set(cache_key, response.data, 60 * 30)  # 30 minutes
            return response
        
        return Response(cached_data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        cache_key = get_book_detail_cache_key(instance.id)
        cached_data = cache.get(cache_key)
        
        if cached_data is None:
            response = super().retrieve(request, *args, **kwargs)
            cache.set(cache_key, response.data, 60 * 60)  # 1 hour
            return response
        
        return Response(cached_data)
    
    def perform_create(self, serializer):
        instance = serializer.save()
        # Invalidate list cache
        cache.delete(get_book_list_cache_key())
    
    def perform_update(self, serializer):
        instance = serializer.save()
        # Invalidate both list and detail cache
        cache.delete(get_book_list_cache_key())
        cache.delete(get_book_detail_cache_key(instance.id))
    
    def perform_destroy(self, instance):
        book_id = instance.id
        instance.delete()
        # Invalidate caches
        cache.delete(get_book_list_cache_key())
        cache.delete(get_book_detail_cache_key(book_id))

# Signal-based invalidation (alternative approach)
@receiver(post_save, sender=Book)
def invalidate_book_cache(sender, instance, **kwargs):
    cache.delete(get_book_list_cache_key())
    cache.delete(get_book_detail_cache_key(instance.id))

@receiver(post_delete, sender=Book)
def invalidate_book_cache_on_delete(sender, instance, **kwargs):
    cache.delete(get_book_list_cache_key())
    cache.delete(get_book_detail_cache_key(instance.id))
```

### Cache Patterns

**1. Cache-Aside (Look-Aside) Pattern:**
```python
# Check cache first, then database
def get_expensive_data():
    cache_key = 'expensive_data'
    data = cache.get(cache_key)
    
    if data is None:
        # Not in cache, fetch from database
        data = expensive_database_query()
        cache.set(cache_key, data, timeout=3600)
    
    return data
```

**2. Write-Through Pattern:**
```python
# Write to both cache and database
def update_data(new_data):
    # Update database
    instance = Model.objects.get(id=1)
    instance.field = new_data
    instance.save()
    
    # Update cache
    cache.set(f'model_{instance.id}', instance, timeout=3600)
```

**3. Write-Behind (Write-Back) Pattern:**
```python
# Write to cache immediately, database later (async)
def update_data(new_data):
    # Update cache immediately
    cache.set('data', new_data, timeout=3600)
    
    # Update database asynchronously (using Celery)
    update_database_async.delay(new_data)
```

### Best Practices

1. **Use appropriate timeouts:** Balance freshness vs performance
2. **Invalidate on updates:** Always invalidate when data changes
3. **Use cache keys wisely:** Include relevant parameters in keys
4. **Monitor cache hit rate:** Track cache effectiveness
5. **Use Redis for production:** More reliable than local memory
6. **Cache serialized data:** Cache the final response format
7. **Don't cache user-specific data without user ID in key**
8. **Set reasonable defaults:** Use sensible timeout values

---

## 🎓 Advanced Interview Topics (4+ Years Experience)

### Cache Invalidation Strategies

**1. Time-Based Invalidation:**
```python
# Cache expires after time
cache.set('key', value, timeout=3600)  # 1 hour

# Use for: Data that changes infrequently
```

**2. Event-Based Invalidation:**
```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Student)
def invalidate_student_cache(sender, instance, **kwargs):
    # Invalidate cache when student is saved
    cache.delete(f'student_{instance.id}')
    cache.delete('students_list')  # Invalidate list cache
```

**3. Version-Based Caching:**
```python
def get_students():
    cache_version = cache.get('students_version', 1)
    cache_key = f'students_v{cache_version}'
    students = cache.get(cache_key)
    
    if students is None:
        students = list(Student.objects.all())
        cache.set(cache_key, students, timeout=None)  # No expiration
    
    return students

# Invalidate by incrementing version
def invalidate_students():
    version = cache.get('students_version', 1)
    cache.set('students_version', version + 1)
```

### Distributed Caching

**1. Redis Cluster:**
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': [
            'redis://127.0.0.1:6379/1',
            'redis://127.0.0.1:6380/1',
            'redis://127.0.0.1:6381/1',
        ],
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

**2. Cache Sharding:**
```python
def get_cache_key(user_id):
    # Shard by user ID
    shard = user_id % 4
    return f'cache_shard_{shard}:user_{user_id}'
```

### Cache Warming

**1. Pre-populate Cache:**
```python
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Warm cache on startup
        students = Student.objects.all()
        cache.set('students_list', list(students), timeout=3600)
```

### Cache Monitoring

**1. Cache Statistics:**
```python
from django.core.cache import cache

def get_cache_stats():
    # Redis stats
    if hasattr(cache, 'get_client'):
        client = cache.get_client()
        info = client.info('stats')
        return {
            'hits': info.get('keyspace_hits', 0),
            'misses': info.get('keyspace_misses', 0),
            'hit_rate': info['keyspace_hits'] / (info['keyspace_hits'] + info['keyspace_misses'])
        }
```

---

*This guide covers essential and advanced caching patterns. Master these for senior Django REST Framework positions.*

