"""
ADVANCED: Custom Filtering with django-filter

django-filter provides powerful filtering capabilities beyond DRF's built-in filters.
"""

import django_filters
from .models import BlogPost, Comment


class BlogPostFilter(django_filters.FilterSet):
    """
    Custom filter set for BlogPost
    
    This allows filtering by:
    - title (icontains - case-insensitive contains)
    - status (exact match)
    - author (exact match)
    - is_featured (boolean)
    - created_at (date range)
    - views_count (range)
    """
    title = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=BlogPost.STATUS_CHOICES)
    author = django_filters.NumberFilter(field_name='author__id')
    author_username = django_filters.CharFilter(field_name='author__username', lookup_expr='icontains')
    is_featured = django_filters.BooleanFilter()
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    views_min = django_filters.NumberFilter(field_name='views_count', lookup_expr='gte')
    views_max = django_filters.NumberFilter(field_name='views_count', lookup_expr='lte')
    tags = django_filters.CharFilter(method='filter_tags')
    
    class Meta:
        model = BlogPost
        fields = ['title', 'status', 'author', 'is_featured']
    
    def filter_tags(self, queryset, name, value):
        """
        Custom filter method for tags
        Filters posts that contain any of the provided tags
        """
        tags = [tag.strip() for tag in value.split(',')]
        queryset = queryset.filter(tags__icontains=tags[0])
        for tag in tags[1:]:
            queryset = queryset | queryset.model.objects.filter(tags__icontains=tag)
        return queryset.distinct()


class CommentFilter(django_filters.FilterSet):
    """Filter set for comments"""
    post = django_filters.NumberFilter(field_name='post__id')
    author = django_filters.NumberFilter(field_name='author__id')
    is_approved = django_filters.BooleanFilter()
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    
    class Meta:
        model = Comment
        fields = ['post', 'author', 'is_approved']

