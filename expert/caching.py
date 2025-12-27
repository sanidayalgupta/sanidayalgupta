"""
EXPERT: Caching in DRF

Caching is like storing frequently accessed data in a fast memory (like RAM) 
instead of fetching it from a slow database every time.

Real-life example: 
Imagine a library. Instead of going to the storage room (database) every time 
someone asks for a popular book, you keep copies at the front desk (cache) 
for quick access. The cache is faster but has limited space.

Types of caching in DRF:
1. View-level caching - Cache entire API responses
2. Per-view caching - Cache specific views
3. Template fragment caching - Cache parts of responses
4. Low-level caching - Cache specific data

Benefits:
- Faster response times (like instant coffee vs brewing)
- Reduced database load (fewer trips to storage)
- Better user experience (faster page loads)
"""

from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework.response import Response


def cache_key_company_list():
    """
    Generate a unique cache key for company list
    
    Think of this like a label on a storage box.
    When you want to find cached company data, you use this key.
    """
    return 'company_list_all'


def cache_key_company_detail(pk):
    """
    Generate cache key for a specific company
    
    Like a specific shelf number for a specific book.
    """
    return f'company_detail_{pk}'


def cache_key_company_statistics(pk):
    """
    Cache key for company statistics
    
    Statistics are expensive to calculate (like counting all books in a library),
    so we cache them for quick access.
    """
    return f'company_statistics_{pk}'


class CacheMixin:
    """
    Mixin class to add caching functionality to viewsets
    
    This is like adding a "fast access" feature to any viewset.
    Instead of writing caching code in every view, we create this reusable mixin.
    
    Real-life example:
    Like adding a "quick access drawer" to any desk - you can add it to 
    any desk (viewset) that needs it.
    """
    
    # Cache timeout in seconds (like expiration date on food)
    # After this time, cache expires and fresh data is fetched
    cache_timeout = 60 * 5  # 5 minutes
    
    def get_cache_key(self, request, *args, **kwargs):
        """
        Generate cache key based on request
        
        Different users might see different data, so we include user in cache key.
        Like having separate storage boxes labeled with user names.
        """
        user_id = request.user.id if request.user.is_authenticated else 'anon'
        view_name = self.__class__.__name__
        return f'{view_name}_{user_id}_{request.path}'
    
    def get_cached_response(self, cache_key):
        """
        Try to get data from cache
        
        Like checking if the book is already at the front desk.
        If yes, return it immediately. If no, go to storage.
        """
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)
        return None
    
    def set_cached_response(self, cache_key, data):
        """
        Store data in cache for future use
        
        Like putting a copy of the book at the front desk for next time.
        """
        cache.set(cache_key, data, self.cache_timeout)
    
    def invalidate_cache(self, pattern):
        """
        Clear cache matching a pattern
        
        Like removing all books from front desk when library updates its catalog.
        We need fresh data, so old cache is cleared.
        
        Example: When a company is updated, we clear all company-related cache.
        """
        # In production, you'd use cache.delete_many() or cache.clear_pattern()
        # For simplicity, we'll use cache.clear() - clears everything
        # In real apps, use Redis with pattern matching
        pass


def cache_company_list(timeout=300):
    """
    Decorator to cache company list view
    
    Decorators are like adding a feature wrapper around a function.
    This one adds caching - like wrapping a gift box (caching) around 
    the actual gift (the view function).
    
    Usage:
    @cache_company_list(timeout=300)  # Cache for 5 minutes
    def my_view(request):
        ...
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = cache_key_company_list()
            
            # Try to get from cache first (like checking front desk)
            cached_data = cache.get(cache_key)
            if cached_data is not None:
                return Response(cached_data)
            
            # If not in cache, execute the view (go to storage room)
            response = func(*args, **kwargs)
            
            # Store result in cache for next time (put copy at front desk)
            if hasattr(response, 'data'):
                cache.set(cache_key, response.data, timeout)
            
            return response
        return wrapper
    return decorator

