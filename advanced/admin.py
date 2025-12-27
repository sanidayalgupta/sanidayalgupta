from django.contrib import admin
from .models import BlogPost, Comment, UserProfile

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'is_featured', 'views_count', 'likes_count', 'created_at']
    list_filter = ['status', 'is_featured', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'is_approved', 'is_edited', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['content', 'post__title', 'author__username']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_verified', 'location', 'created_at']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['user__username', 'user__email', 'bio']

