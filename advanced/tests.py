"""
ADVANCED: Test Cases for Authentication and Permissions

These tests verify that authentication and permissions work correctly.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import BlogPost, Comment


class BlogPostAuthenticationTestCase(TestCase):
    """Test cases for authenticated endpoints"""
    
    def setUp(self):
        """Set up test data with authentication"""
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        
        # Set authentication token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
    
    def test_create_blogpost_authenticated(self):
        """Test creating blog post when authenticated"""
        data = {
            'title': 'Test Post',
            'slug': 'test-post',
            'content': 'Test content',
            'status': 'draft',
            'tags': 'test, django'
        }
        
        response = self.client.post('/api/advanced/blogposts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BlogPost.objects.count(), 1)
    
    def test_create_blogpost_unauthenticated(self):
        """Test that unauthenticated users cannot create posts"""
        self.client.credentials()  # Remove authentication
        
        data = {
            'title': 'Test Post',
            'slug': 'test-post',
            'content': 'Test content',
            'status': 'draft'
        }
        
        response = self.client.post('/api/advanced/blogposts/', data, format='json')
        # Should fail - unauthenticated users can't create
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_blogposts_unauthenticated(self):
        """Test that anyone can list posts (read permission)"""
        BlogPost.objects.create(
            title='Public Post',
            slug='public-post',
            content='Content',
            author=self.user,
            status='published'
        )
        
        self.client.credentials()  # Remove authentication
        
        response = self.client.get('/api/advanced/blogposts/')
        # Should succeed - read is allowed for all
        self.assertEqual(response.status_code, status.HTTP_200_OK)
