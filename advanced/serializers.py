"""
ADVANCED: Advanced Serializer Patterns

This demonstrates:
1. SerializerMethodField for computed values
2. Custom field validation
3. Nested serializers with write operations
4. Different serializers for different actions
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BlogPost, Comment, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer"""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'bio', 'avatar', 'website', 'location', 'birth_date', 'is_verified', 'created_at']
        read_only_fields = ['id', 'created_at', 'is_verified']


class CommentSerializer(serializers.ModelSerializer):
    """Comment serializer"""
    author_name = serializers.CharField(source='author.username', read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'post_title', 'author', 'author_name', 'content', 'is_approved', 'is_edited', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'is_approved', 'is_edited', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Set author from request"""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class BlogPostListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list view"""
    author_name = serializers.CharField(source='author.username', read_only=True)
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'author', 'author_name', 'status', 'is_featured', 'views_count', 'likes_count', 'comments_count', 'published_at', 'created_at']
        read_only_fields = ['id', 'author', 'views_count', 'likes_count', 'created_at']
    
    def get_comments_count(self, obj):
        """Get count of approved comments"""
        return obj.comments.filter(is_approved=True).count()


class BlogPostDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer with nested relationships"""
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_email = serializers.EmailField(source='author.email', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    approved_comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'content', 'author', 'author_name', 'author_email',
            'status', 'tags', 'views_count', 'likes_count', 'is_featured',
            'published_at', 'comments', 'approved_comments_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'views_count', 'likes_count', 'created_at', 'updated_at']
    
    def get_approved_comments_count(self, obj):
        """Count of approved comments"""
        return obj.comments.filter(is_approved=True).count()
    
    def validate_status(self, value):
        """Custom validation for status"""
        if value == 'published' and not self.instance:
            # New posts can't be published immediately
            raise serializers.ValidationError("New posts cannot be published immediately. Save as draft first.")
        return value
    
    def update(self, instance, validated_data):
        """Custom update logic"""
        # Auto-set published_at when status changes to published
        if validated_data.get('status') == 'published' and instance.status != 'published':
            from django.utils import timezone
            validated_data['published_at'] = timezone.now()
        elif validated_data.get('status') != 'published':
            validated_data['published_at'] = None
        
        return super().update(instance, validated_data)


class BlogPostCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating posts"""
    class Meta:
        model = BlogPost
        fields = ['title', 'slug', 'content', 'status', 'tags', 'is_featured']
    
    def validate_slug(self, value):
        """Ensure slug is unique"""
        if BlogPost.objects.filter(slug=value).exists():
            raise serializers.ValidationError("A post with this slug already exists.")
        return value

