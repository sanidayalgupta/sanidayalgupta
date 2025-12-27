"""
INTERMEDIATE: Advanced Serializers

This demonstrates:
1. Nested serializers (serializing related objects)
2. Read-only vs write-only fields
3. SerializerMethodField (computed fields)
4. PrimaryKeyRelatedField, StringRelatedField
5. Nested writes (creating related objects)
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Author, Category, Book, Review


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):
    """Simple serializer for Category"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug']
        read_only_fields = ['id']


class AuthorSerializer(serializers.ModelSerializer):
    """
    Author serializer with nested user information
    """
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    books_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = ['id', 'user', 'user_id', 'bio', 'birth_date', 'website', 'books_count', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_books_count(self, obj):
        """Custom method field - returns count of books"""
        return obj.books.count()


class BookListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing books (no nested data)
    More efficient for list views
    """
    author_name = serializers.CharField(source='author.user.get_full_name', read_only=True)
    categories = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author_name', 'categories', 'price', 'is_available', 'publication_date']


class BookDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer with nested relationships
    Used for retrieve operations
    """
    author = AuthorSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        source='categories',
        write_only=True,
        required=False
    )
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'description', 'author', 'categories', 'category_ids',
            'isbn', 'publication_date', 'price', 'pages', 'is_available',
            'average_rating', 'reviews_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_average_rating(self, obj):
        """Calculate average rating from reviews"""
        reviews = obj.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 2)
        return None
    
    def get_reviews_count(self, obj):
        """Get count of reviews"""
        return obj.reviews.count()


class ReviewSerializer(serializers.ModelSerializer):
    """Review serializer with nested book and reviewer info"""
    book_title = serializers.CharField(source='book.title', read_only=True)
    reviewer_name = serializers.CharField(source='reviewer.username', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'book', 'book_title', 'reviewer', 'reviewer_name', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'reviewer']
    
    def create(self, validated_data):
        """Override create to set reviewer from request"""
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Separate serializer for create/update operations
    Uses PrimaryKeyRelatedField for relationships (more efficient)
    """
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        required=False
    )
    
    class Meta:
        model = Book
        fields = [
            'title', 'description', 'author', 'categories',
            'isbn', 'publication_date', 'price', 'pages', 'is_available'
        ]
    
    def validate_isbn(self, value):
        """Custom validation for ISBN"""
        if len(value) not in [10, 13]:
            raise serializers.ValidationError("ISBN must be 10 or 13 characters")
        return value

