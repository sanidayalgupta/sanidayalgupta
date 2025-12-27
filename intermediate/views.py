"""
INTERMEDIATE: ViewSets and Routers

ViewSets combine the logic for multiple related views into a single class.
Routers automatically generate URL patterns for ViewSets.

Types of ViewSets:
1. ModelViewSet - Full CRUD operations
2. ReadOnlyModelViewSet - Only read operations (list, retrieve)
3. GenericViewSet - Base class, you define actions
4. ViewSet - Most basic, no default actions
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Author, Category, Book, Review
from .serializers import (
    AuthorSerializer,
    CategorySerializer,
    BookListSerializer,
    BookDetailSerializer,
    BookCreateUpdateSerializer,
    ReviewSerializer
)


# ============================================================================
# ModelViewSet - Provides full CRUD operations automatically
# ============================================================================

class CategoryViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet automatically provides:
    - list() - GET /categories/
    - create() - POST /categories/
    - retrieve() - GET /categories/{id}/
    - update() - PUT /categories/{id}/
    - partial_update() - PATCH /categories/{id}/
    - destroy() - DELETE /categories/{id}/
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'id']
    ordering = ['name']


class AuthorViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet for Authors with custom queryset
    """
    queryset = Author.objects.select_related('user').prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__username', 'user__email', 'bio']
    ordering_fields = ['created_at', 'user__username']
    ordering = ['-created_at']


# ============================================================================
# Custom ViewSet with different serializers for different actions
# ============================================================================

class BookViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet with custom serializers for different actions
    
    Uses:
    - BookListSerializer for list (faster, less data)
    - BookDetailSerializer for retrieve (more data, nested)
    - BookCreateUpdateSerializer for create/update (efficient writes)
    """
    queryset = Book.objects.select_related('author__user').prefetch_related('categories', 'reviews').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Filtering and searching
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_available', 'author', 'categories']
    search_fields = ['title', 'description', 'isbn', 'author__user__username']
    ordering_fields = ['title', 'price', 'publication_date', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """
        Return different serializers based on the action
        """
        if self.action == 'list':
            return BookListSerializer
        elif self.action == 'retrieve':
            return BookDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return BookCreateUpdateSerializer
        return BookDetailSerializer
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """
        Custom action: GET /books/{id}/reviews/
        
        @action decorator creates custom endpoints beyond CRUD
        detail=True means it operates on a single object
        detail=False would operate on the collection
        """
        book = self.get_object()
        reviews = book.reviews.select_related('reviewer').all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_review(self, request, pk=None):
        """
        Custom action: POST /books/{id}/add_review/
        """
        book = self.get_object()
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(book=book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """
        Custom action: GET /books/available/
        
        detail=False means it operates on the collection, not a single object
        """
        available_books = self.queryset.filter(is_available=True)
        serializer = BookListSerializer(available_books, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """
        Custom action: GET /books/by_category/?category_id=1
        """
        category_id = request.query_params.get('category_id')
        if category_id:
            books = self.queryset.filter(categories__id=category_id)
            serializer = BookListSerializer(books, many=True)
            return Response(serializer.data)
        return Response({'error': 'category_id parameter required'}, status=status.HTTP_400_BAD_REQUEST)


# ============================================================================
# ReadOnlyModelViewSet - Only read operations
# ============================================================================

class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnlyModelViewSet provides only:
    - list() - GET /reviews/
    - retrieve() - GET /reviews/{id}/
    
    No create, update, or delete operations
    """
    queryset = Review.objects.select_related('book', 'reviewer').all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['book', 'reviewer', 'rating']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

