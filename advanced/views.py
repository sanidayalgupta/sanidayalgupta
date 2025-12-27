"""
ADVANCED: Authentication, Permissions, Filtering, Pagination

This demonstrates:
1. Token Authentication
2. Custom Permissions
3. Advanced Filtering with django-filter
4. Custom Pagination
5. Search and Ordering
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from .models import BlogPost, Comment, UserProfile
from .serializers import (
    BlogPostListSerializer,
    BlogPostDetailSerializer,
    BlogPostCreateSerializer,
    CommentSerializer,
    UserProfileSerializer
)
from .permissions import IsOwnerOrReadOnly, IsAuthorOrAdmin, CanApproveComment
from .filters import BlogPostFilter, CommentFilter
from .pagination import (
    SmallResultsSetPagination,
    StandardResultsSetPagination,
    BlogPostLimitOffsetPagination
)


class BlogPostViewSet(viewsets.ModelViewSet):
    """
    Advanced ViewSet demonstrating:
    - Multiple authentication methods
    - Custom permissions
    - Advanced filtering
    - Custom pagination
    - Search and ordering
    """
    queryset = BlogPost.objects.select_related('author').prefetch_related('comments').all()
    
    # Authentication: Multiple methods supported
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    
    # Permissions: Different for different actions
    def get_permissions(self):
        """
        Customize permissions based on action
        """
        if self.action in ['list', 'retrieve']:
            # Anyone can read
            permission_classes = [AllowAny]
        elif self.action == 'create':
            # Must be authenticated to create
            permission_classes = [IsAuthenticated]
        else:
            # Owner or admin can update/delete
            permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]
    
    # Filtering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BlogPostFilter
    search_fields = ['title', 'content', 'tags', 'author__username']
    ordering_fields = ['created_at', 'updated_at', 'views_count', 'likes_count', 'title']
    ordering = ['-created_at']
    
    # Pagination
    pagination_class = StandardResultsSetPagination
    
    def get_serializer_class(self):
        """Different serializers for different actions"""
        if self.action == 'list':
            return BlogPostListSerializer
        elif self.action == 'retrieve':
            return BlogPostDetailSerializer
        elif self.action == 'create':
            return BlogPostCreateSerializer
        return BlogPostDetailSerializer
    
    def perform_create(self, serializer):
        """Set author automatically when creating"""
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """
        Custom action: POST /blogposts/{id}/like/
        """
        post = self.get_object()
        post.likes_count += 1
        post.save()
        return Response({'likes_count': post.likes_count})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def view(self, request, pk=None):
        """
        Custom action: POST /blogposts/{id}/view/
        Increment view count
        """
        post = self.get_object()
        post.views_count += 1
        post.save()
        return Response({'views_count': post.views_count})
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def published(self, request):
        """
        Custom action: GET /blogposts/published/
        Get only published posts
        """
        published_posts = self.queryset.filter(status='published')
        page = self.paginate_queryset(published_posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(published_posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def featured(self, request):
        """
        Custom action: GET /blogposts/featured/
        Get only featured posts
        """
        featured_posts = self.queryset.filter(is_featured=True, status='published')
        serializer = self.get_serializer(featured_posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_posts(self, request):
        """
        Custom action: GET /blogposts/my_posts/
        Get current user's posts
        """
        my_posts = self.queryset.filter(author=request.user)
        page = self.paginate_queryset(my_posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(my_posts, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Comment ViewSet with custom permissions and filtering
    """
    queryset = Comment.objects.select_related('post', 'author').all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    
    # Filtering
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CommentFilter
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    # Pagination
    pagination_class = SmallResultsSetPagination
    
    def get_permissions(self):
        """Custom permissions"""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthorOrAdmin]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """Set author automatically"""
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[CanApproveComment])
    def approve(self, request, pk=None):
        """
        Custom action: POST /comments/{id}/approve/
        Only post author or admin can approve
        """
        comment = self.get_object()
        comment.is_approved = True
        comment.save()
        return Response({'message': 'Comment approved', 'is_approved': True})
    
    @action(detail=True, methods=['post'], permission_classes=[CanApproveComment])
    def reject(self, request, pk=None):
        """
        Custom action: POST /comments/{id}/reject/
        """
        comment = self.get_object()
        comment.is_approved = False
        comment.save()
        return Response({'message': 'Comment rejected', 'is_approved': False})


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    User Profile ViewSet
    """
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = UserProfileSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Users can only see their own profile unless admin"""
        if self.request.user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Set user automatically"""
        serializer.save(user=self.request.user)

