"""
INTERMEDIATE APP - Level 2: ViewSets, Routers, and Relationships

This app demonstrates:
1. ViewSets (ModelViewSet, ReadOnlyModelViewSet, GenericViewSet)
2. Routers (automatic URL routing)
3. Model relationships (ForeignKey, ManyToMany)
4. Nested serializers
"""

from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    """Author model with user relationship"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author_profile')
    bio = models.TextField()
    birth_date = models.DateField(null=True, blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Category(models.Model):
    """Category for books"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name


class Book(models.Model):
    """Book model with ForeignKey and ManyToMany relationships"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    categories = models.ManyToManyField(Category, related_name='books', blank=True)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pages = models.IntegerField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Review(models.Model):
    """Review model - demonstrates nested relationships"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['book', 'reviewer']  # One review per user per book
    
    def __str__(self):
        return f"{self.reviewer.username} - {self.book.title} - {self.rating} stars"

