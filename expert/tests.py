"""
EXPERT: Test Cases for Advanced Patterns

These tests verify caching, throttling, transactions, and bulk operations.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import Company, Department, Employee


class CompanyCachingTestCase(TestCase):
    """Test cases for caching functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        # Clear cache before each test
        cache.clear()
    
    def test_company_list_caching(self):
        """Test that company list is cached"""
        Company.objects.create(
            name='Test Company',
            description='Test',
            founded_year=2020,
            headquarters='Test City',
            website='https://test.com'
        )
        
        # First request - should hit database
        response1 = self.client.get('/api/expert/companies/')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        
        # Second request - should use cache (faster)
        response2 = self.client.get('/api/expert/companies/')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        # Both should have same data
        self.assertEqual(response1.data, response2.data)
    
    def test_company_statistics_caching(self):
        """Test that statistics are cached"""
        company = Company.objects.create(
            name='Test Company',
            description='Test',
            founded_year=2020,
            headquarters='Test City',
            website='https://test.com'
        )
        
        # First request - calculates statistics
        response1 = self.client.get(f'/api/expert/companies/{company.id}/statistics/')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        
        # Second request - should use cache
        response2 = self.client.get(f'/api/expert/companies/{company.id}/statistics/')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.data, response2.data)


class BulkOperationTestCase(TestCase):
    """Test cases for bulk operations"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.company = Company.objects.create(
            name='Test Company',
            description='Test',
            founded_year=2020,
            headquarters='Test City',
            website='https://test.com'
        )
        
        self.department = Department.objects.create(
            company=self.company,
            name='Engineering',
            budget=100000
        )
    
    def test_bulk_create_employees(self):
        """
        Test bulk creating employees - The Batch Processor
        
        This tests creating multiple employees at once, like hiring
        multiple people in one batch instead of one at a time.
        """
        user1 = User.objects.create_user(username='emp1', email='emp1@test.com')
        user2 = User.objects.create_user(username='emp2', email='emp2@test.com')
        
        # Use user_id for writing (ForeignKey relationship)
        data = {
            'employees': [
                {
                    'department': self.department.id,
                    'user_id': user1.id,  # Use user_id for writing
                    'employee_id': 'EMP001',
                    'position': 'Developer',
                    'salary': 50000,
                    'hire_date': '2024-01-01'
                },
                {
                    'department': self.department.id,
                    'user_id': user2.id,  # Use user_id for writing
                    'employee_id': 'EMP002',
                    'position': 'Designer',
                    'salary': 45000,
                    'hire_date': '2024-01-01'
                }
            ]
        }
        
        response = self.client.post('/api/expert/employees/bulk_create/', data, format='json')
        
        # Check if bulk create was successful
        if response.status_code != status.HTTP_201_CREATED:
            # If it failed, print the error for debugging
            print(f"Response status: {response.status_code}")
            print(f"Response data: {response.data}")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)
