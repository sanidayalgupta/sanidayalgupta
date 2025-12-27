"""
INTERMEDIATE: Test Cases for ViewSets and Relationships

These tests verify that ViewSets and relationships work correctly.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author, Category, Book, Review


class BookViewSetTestCase(TestCase):
    """Test cases for Book ViewSet"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.author = Author.objects.create(user=self.user, bio='Test bio')
        self.category = Category.objects.create(name='Fiction', slug='fiction')
    
    def test_list_books(self):
        """Test listing books"""
        Book.objects.create(
            title='Test Book',
            description='Test description',
            author=self.author,
            isbn='1234567890123',
            publication_date='2024-01-01',
            price=29.99,
            pages=300
        )
        
        response = self.client.get('/api/intermediate/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Paginated response
    
    def test_custom_action_reviews(self):
        """Test custom action for getting book reviews"""
        book = Book.objects.create(
            title='Test Book',
            description='Test',
            author=self.author,
            isbn='1234567890123',
            publication_date='2024-01-01',
            price=29.99,
            pages=300
        )
        
        Review.objects.create(
            book=book,
            reviewer=self.user,
            rating=5,
            comment='Great book!'
        )
        
        response = self.client.get(f'/api/intermediate/books/{book.id}/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
