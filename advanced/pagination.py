"""
ADVANCED: Custom Pagination

DRF provides several pagination classes:
1. PageNumberPagination - Standard page number pagination
2. LimitOffsetPagination - Limit/offset based pagination
3. CursorPagination - Cursor-based pagination (for large datasets)

You can customize these or create your own.
"""

from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class SmallResultsSetPagination(PageNumberPagination):
    """
    Custom pagination for small result sets
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20
    page_query_param = 'page'


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination (default)
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'


class LargeResultsSetPagination(PageNumberPagination):
    """
    Pagination for large result sets
    """
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200
    page_query_param = 'page'


class BlogPostLimitOffsetPagination(LimitOffsetPagination):
    """
    Limit/Offset pagination example
    """
    default_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 50


class BlogPostCursorPagination(CursorPagination):
    """
    Cursor-based pagination (best for large datasets)
    More efficient than offset-based pagination
    """
    page_size = 10
    ordering = '-created_at'
    page_size_query_param = 'page_size'
    max_page_size = 50

