# Filtering, Search & Pagination

## 🔍 Filtering

### DjangoFilterBackend

**Definition:** DjangoFilterBackend allows filtering by exact field values.

**Real-life example:**
Like a search filter - "Show me only red shirts".

**Setup:**
```bash
pip install django-filter
```

```python
# settings.py
INSTALLED_APPS = [
    'django_filters',
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ]
}
```

**Example:**
```python
# Import DjangoFilterBackend from django-filters
# DjangoFilterBackend: Filter backend that uses django-filter library
from django_filters.rest_framework import DjangoFilterBackend

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # filter_backends: List of filter backends to apply
    # Executed in order, each can modify queryset
    # Alternative: Set in settings.py DEFAULT_FILTER_BACKENDS (applies to all views)
    # Difference: Per-view allows customization, settings applies globally
    filter_backends = [DjangoFilterBackend]
    
    # filterset_fields: Simple field-based filtering
    # Allows filtering by exact match on specified fields
    # Format: ?field_name=value
    # Alternative: filterset_class (custom FilterSet with complex logic)
    # Difference: filterset_fields is simple, filterset_class is powerful
    filterset_fields = ['is_available', 'author', 'category']
    
# Usage: GET /books/?is_available=true&author=1&category=fiction
# - Filters books where is_available=True AND author=1 AND category='fiction'
# - Multiple filters are ANDed together
# - Empty values are ignored
```

**Custom Filterset:**
```python
import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    # Exact match
    title = django_filters.CharFilter(lookup_expr='iexact')
    
    # Contains
    description = django_filters.CharFilter(lookup_expr='icontains')
    
    # Range
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    # Date range
    published_after = django_filters.DateFilter(field_name='published_date', lookup_expr='gte')
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'category']

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilter
    
# Usage: GET /books/?price_min=10&price_max=50&published_after=2020-01-01
```

### SearchFilter

**Definition:** SearchFilter searches across multiple fields.

**Real-life example:**
Like Google search - searches across title, description, etc.

**Example:**
```python
from rest_framework.filters import SearchFilter

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description', 'isbn', 'author__name']
    
# Usage: GET /books/?search=django
# Searches in title, description, isbn, and author name
```

**Search Operators:**
```python
search_fields = [
    '^title',      # Starts with (title__istartswith)
    '=isbn',       # Exact match (isbn__iexact)
    '@description', # Full-text search (PostgreSQL)
    '$author__name' # Regex search
]
```

### OrderingFilter

**Definition:** OrderingFilter allows sorting results.

**Real-life example:**
Like sorting products by price or date.

**Example:**
```python
from rest_framework.filters import OrderingFilter

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['title', 'price', 'created_at', 'author__name']
    ordering = ['-created_at']  # Default: newest first
    
# Usage: GET /books/?ordering=-price  (highest price first)
# Usage: GET /books/?ordering=title,-price  (title asc, price desc)
```

### Custom Filters

**Definition:** Custom filters allow you to create your own filtering logic.

**Example:**
```python
from rest_framework.filters import BaseFilterBackend

class IsAvailableFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        is_available = request.query_params.get('is_available')
        if is_available is not None:
            return queryset.filter(quantity__gt=0)
        return queryset

class BookViewSet(viewsets.ModelViewSet):
    filter_backends = [IsAvailableFilter]
    
# Usage: GET /books/?is_available=true
```

### Dynamic Filtering

**Definition:** Dynamic filtering allows filtering based on request parameters or user permissions.

**Example:**
```python
class BookViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Book.objects.all()
        
        # Filter by query params
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by user
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_public=True)
        
        return queryset
```

---

## 📄 Pagination

### PageNumberPagination

**Definition:** PageNumberPagination splits results into pages using page numbers.

**Real-life example:**
Like book pages - you go to page 1, 2, 3, etc.

**Global Configuration:**
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}
```

**Custom Pagination:**
```python
from rest_framework.pagination import PageNumberPagination

class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'  # Allow client to override
    max_page_size = 100  # Maximum page size
    page_query_param = 'page'  # URL parameter name

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = StandardPagination
    
# Usage: GET /books/?page=2&page_size=50
# Response:
# {
#   "count": 200,
#   "next": "http://example.com/books/?page=3",
#   "previous": "http://example.com/books/?page=1",
#   "results": [...]
# }
```

### LimitOffsetPagination

**Definition:** LimitOffsetPagination uses limit and offset parameters (like SQL LIMIT/OFFSET).

**Real-life example:**
Like "Show me 10 items starting from item 20".

**Example:**
```python
from rest_framework.pagination import LimitOffsetPagination

class StandardLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 100

class BookViewSet(viewsets.ModelViewSet):
    pagination_class = StandardLimitOffsetPagination
    
# Usage: GET /books/?limit=10&offset=20
# Response:
# {
#   "count": 200,
#   "next": "http://example.com/books/?limit=10&offset=30",
#   "previous": "http://example.com/books/?limit=10&offset=10",
#   "results": [...]
# }
```

### CursorPagination

**Definition:** CursorPagination provides cursor-based pagination for large datasets (efficient for infinite scroll).

**Real-life example:**
Like "Show me next 10 items after this cursor" - more efficient than offset for large datasets.

**Example:**
```python
from rest_framework.pagination import CursorPagination

class BookCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-created_at'  # Must be unique, consistent ordering
    cursor_query_param = 'cursor'

class BookViewSet(viewsets.ModelViewSet):
    pagination_class = BookCursorPagination
    
# Usage: GET /books/?cursor=cD0yMDIzLTEyLTAx
# Response:
# {
#   "next": "http://example.com/books/?cursor=cD0yMDIzLTEyLTAy",
#   "previous": null,
#   "results": [...]
# }
```

### Custom Pagination

**Definition:** Custom pagination allows you to create your own pagination style.

**Example:**
```python
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 10
    
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data
        })
```

### Custom Pagination Metadata

**Definition:** Custom pagination metadata adds extra information to paginated responses.

**Example:**
```python
class EnhancedPagination(PageNumberPagination):
    page_size = 20
    
    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'count': self.page.paginator.count,
                'page_size': self.page_size,
                'current_page': self.page.number,
                'total_pages': self.page.paginator.num_pages,
                'has_next': self.page.has_next(),
                'has_previous': self.page.has_previous(),
            },
            'data': data
        })
```

---

## 🔄 Combining Filtering, Search & Pagination

**Example:**
```python
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'author']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'price', 'created_at']
    ordering = ['-created_at']
    pagination_class = StandardPagination
    
# Usage: GET /books/?category=fiction&search=django&ordering=-price&page=2
```

---

## 🎓 Advanced Interview Topics (4+ Years Experience)

### Advanced Filtering Patterns

**1. Dynamic Filtering Based on User:**
```python
class BookViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Book.objects.all()
        
        # Filter based on user role
        if self.request.user.is_staff:
            # Staff sees all books
            return queryset
        else:
            # Regular users see only published books
            return queryset.filter(status='published')
    
    def get_filterset_class(self):
        # Return different filterset based on user
        if self.request.user.is_staff:
            return AdminBookFilter
        return BookFilter
```

**2. Filtering with Related Fields:**
```python
class BookFilter(django_filters.FilterSet):
    # Filter by related model fields
    author_name = django_filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains'
    )
    author_country = django_filters.CharFilter(
        field_name='author__country'
    )
    
    class Meta:
        model = Book
        fields = ['author_name', 'author_country']

# Usage: GET /books/?author_name=John&author_country=USA
```

**3. Custom Filter Methods:**
```python
class BookFilter(django_filters.FilterSet):
    price_range = django_filters.CharFilter(method='filter_price_range')
    
    def filter_price_range(self, queryset, name, value):
        # Custom filter logic
        # Format: "10-50" or "50+" or "-20"
        if '-' in value:
            min_price, max_price = value.split('-')
            return queryset.filter(
                price__gte=min_price,
                price__lte=max_price
            )
        elif value.endswith('+'):
            min_price = value[:-1]
            return queryset.filter(price__gte=min_price)
        elif value.startswith('-'):
            max_price = value[1:]
            return queryset.filter(price__lte=max_price)
        return queryset
    
    class Meta:
        model = Book
        fields = ['price_range']

# Usage: GET /books/?price_range=10-50
```

### Advanced Pagination Strategies

**1. Cursor Pagination for Large Datasets:**
```python
from rest_framework.pagination import CursorPagination

class BookCursorPagination(CursorPagination):
    page_size = 50
    ordering = '-created_at'  # Must be unique, stable ordering
    cursor_query_param = 'cursor'
    page_size_query_param = 'page_size'
    max_page_size = 100

# Benefits:
# - Efficient for large datasets (no OFFSET)
# - Consistent even with new data
# - Better performance than offset pagination
```

**2. Time-Based Pagination:**
```python
class TimeBasedPagination(CursorPagination):
    ordering = '-created_at'
    
    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
            'time_range': {
                'start': self.page[0].created_at if self.page else None,
                'end': self.page[-1].created_at if self.page else None,
            }
        })
```

**3. Hybrid Pagination:**
```python
class HybridPagination(PageNumberPagination):
    """Use offset for small datasets, cursor for large"""
    
    def paginate_queryset(self, queryset, request, view=None):
        total = queryset.count()
        
        if total > 10000:
            # Use cursor pagination for large datasets
            return CursorPagination().paginate_queryset(queryset, request, view)
        else:
            # Use offset pagination for small datasets
            return super().paginate_queryset(queryset, request, view)
```

### Search Optimization

**1. Full-Text Search (PostgreSQL):**
```python
from django.contrib.postgres.search import SearchVector

class BookViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Book.objects.all()
        search = self.request.query_params.get('search')
        
        if search:
            # Use PostgreSQL full-text search
            queryset = queryset.annotate(
                search=SearchVector('title', 'description')
            ).filter(search=search)
        
        return queryset
```

**2. Elasticsearch Integration:**
```python
# Install: pip install django-elasticsearch-dsl
from elasticsearch_dsl import Document, Text, Keyword

class BookDocument(Document):
    title = Text()
    description = Text()
    author = Keyword()
    
    class Index:
        name = 'books'

# In viewset
class BookViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        search = self.request.query_params.get('search')
        if search:
            # Search in Elasticsearch
            s = BookDocument.search().query('multi_match', query=search)
            book_ids = [hit.id for hit in s]
            return Book.objects.filter(id__in=book_ids)
        return Book.objects.all()
```

### Filtering Performance

**1. Indexed Fields:**
```python
class Book(models.Model):
    title = models.CharField(max_length=200, db_index=True)  # Indexed for filtering
    category = models.CharField(max_length=100, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['category', 'price']),  # Composite index
        ]
```

**2. Query Optimization:**
```python
class BookViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        # Always use select_related/prefetch_related with filters
        queryset = Book.objects.select_related(
            'author'
        ).prefetch_related(
            'tags'
        ).all()
        
        # Apply filters (uses indexes)
        return queryset
```

### Pagination Best Practices

**1. Configurable Page Size:**
```python
class ConfigurablePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100  # Prevent abuse
    
    def get_page_size(self, request):
        # Allow client to specify, but limit max
        if self.page_size_query_param:
            page_size = request.query_params.get(self.page_size_query_param)
            if page_size:
                return min(int(page_size), self.max_page_size)
        return self.page_size
```

**2. Pagination Metadata:**
```python
class DetailedPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'count': self.page.paginator.count,
                'page_size': self.page_size,
                'current_page': self.page.number,
                'total_pages': self.page.paginator.num_pages,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'results': data
        })
```

---

*This guide covers essential and advanced filtering/pagination patterns. Master these for senior Django REST Framework positions.*

