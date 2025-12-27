"""
BASICS: Test Cases - The Quality Checkers

Tests are like quality control in a factory - they check if everything works correctly.
When you write code, tests verify that it does what you expect.

Real-life example:
Like a car safety test - you test brakes, steering, etc. before selling the car.
In code, we test if our API endpoints work correctly before deploying.

This file contains tests for the basics app.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Student, Course


class StudentAPITestCase(TestCase):
    """
    Test cases for Student API endpoints
    
    This is like a checklist to verify:
    - Can we create students? ✓
    - Can we list students? ✓
    - Can we update students? ✓
    - Can we delete students? ✓
    """
    
    def setUp(self):
        """
        Set up test data - like preparing ingredients before cooking
        
        This runs before each test, creating fresh data for testing.
        Like resetting a game level before each attempt.
        """
        # Create a test client (like a browser for testing)
        self.client = APIClient()
        
        # Create test data (like sample students for testing)
        self.student_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'age': 20,
            'grade': 'A'
        }
    
    def test_create_student(self):
        """
        Test creating a new student - like testing if you can add a new contact
        
        This verifies that POST request creates a student successfully.
        """
        # Make a POST request (like submitting a form)
        response = self.client.post('/api/basics/students-fbv/', self.student_data, format='json')
        
        # Check if request was successful (status code 201 = created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check if student was actually created in database
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(Student.objects.get().name, 'John Doe')
    
    def test_list_students(self):
        """
        Test listing students - like testing if you can view all contacts
        
        This verifies that GET request returns a list of students.
        """
        # Create a student first (like having data to list)
        Student.objects.create(**self.student_data)
        
        # Make a GET request (like viewing a list)
        response = self.client.get('/api/basics/students-fbv/')
        
        # Check if request was successful (status code 200 = OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if we got the student in the response
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'John Doe')
    
    def test_get_student_detail(self):
        """
        Test getting a single student - like testing if you can view one contact
        
        This verifies that GET request with ID returns a specific student.
        """
        # Create a student
        student = Student.objects.create(**self.student_data)
        
        # Make a GET request with student ID
        response = self.client.get(f'/api/basics/students-fbv/{student.id}/')
        
        # Check if request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Doe')
    
    def test_update_student(self):
        """
        Test updating a student - like testing if you can edit a contact
        
        This verifies that PUT/PATCH requests update a student.
        """
        # Create a student
        student = Student.objects.create(**self.student_data)
        
        # Update data
        updated_data = {'name': 'Jane Doe', 'email': 'jane@example.com', 'age': 21, 'grade': 'A'}
        
        # Make a PUT request (full update)
        response = self.client.put(f'/api/basics/students-fbv/{student.id}/', updated_data, format='json')
        
        # Check if update was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        student.refresh_from_db()  # Get latest data from database
        self.assertEqual(student.name, 'Jane Doe')
    
    def test_delete_student(self):
        """
        Test deleting a student - like testing if you can remove a contact
        
        This verifies that DELETE request removes a student.
        """
        # Create a student
        student = Student.objects.create(**self.student_data)
        
        # Make a DELETE request
        response = self.client.delete(f'/api/basics/students-fbv/{student.id}/')
        
        # Check if delete was successful (status code 204 = no content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check if student was actually deleted
        self.assertEqual(Student.objects.count(), 0)
    
    def test_validation(self):
        """
        Test validation - like testing if the system rejects invalid data
        
        This verifies that invalid data (like negative age) is rejected.
        """
        # Try to create student with invalid age
        invalid_data = {'name': 'Test', 'email': 'test@example.com', 'age': -5, 'grade': 'A'}
        response = self.client.post('/api/basics/students-fbv/', invalid_data, format='json')
        
        # Should fail validation (status code 400 = bad request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CourseAPITestCase(TestCase):
    """
    Test cases for Course API endpoints
    
    Similar to Student tests, but for Course model.
    """
    
    def setUp(self):
        """Set up test data for courses"""
        self.client = APIClient()
        self.course_data = {
            'title': 'Django Basics',
            'description': 'Learn Django fundamentals',
            'instructor': 'John Smith',
            'duration_hours': 40,
            'price': 99.99
        }
    
    def test_create_course(self):
        """Test creating a course"""
        response = self.client.post('/api/basics/courses/', self.course_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)
