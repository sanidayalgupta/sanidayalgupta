from django.contrib import admin
from .models import Author, Category, Book, Review

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'birth_date', 'website']
    search_fields = ['user__username', 'user__email']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'price', 'is_available', 'publication_date']
    list_filter = ['is_available', 'categories', 'publication_date']
    search_fields = ['title', 'isbn', 'author__user__username']
    filter_horizontal = ['categories']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'reviewer', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['book__title', 'reviewer__username']

