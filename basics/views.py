"""
BASICS: API Views - The Request Handlers

API Views are like waiters in a restaurant - they receive orders (HTTP requests)
and bring back food (responses). Different types of waiters handle things differently.

Real-life analogy:
- Function-based views = Individual waiters (one waiter per task)
- Class-based views = Organized waiters (one waiter handles multiple related tasks)
- Generic views = Super-efficient waiters (pre-built for common tasks)

DRF provides several ways to create API views:
1. Function-based views with @api_view decorator - Simple, one function per endpoint
2. Class-based views (APIView) - Organized, one class handles multiple HTTP methods
3. Generic views - Pre-built views for common operations (like templates)
4. ViewSets - Advanced pattern (covered in intermediate app)

This file demonstrates all three approaches so you can see the differences.
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny  # Allow anyone to access (for basics)
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from django.shortcuts import get_object_or_404
from .models import Student, Course
from .serializers import StudentSerializer, CourseSerializer


# ============================================================================
# FUNCTION-BASED VIEWS (using @api_view decorator)
# ============================================================================

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # Allow anyone for basics tutorial
def student_list_create(request):
    """
    Function-based view for listing and creating students
    
    GET: Returns list of all students
    POST: Creates a new student
    
    Real-life example:
    Like a student registration desk - anyone can view the list (GET)
    and register new students (POST) without special permissions.
    """
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])  # Allow anyone for basics tutorial
def student_detail(request, pk):
    """
    Function-based view for retrieving, updating, or deleting a student
    
    GET: Retrieve a specific student
    PUT: Full update (all fields required)
    PATCH: Partial update (only provided fields)
    DELETE: Delete the student
    
    Real-life example:
    Like a student information counter - you can view, update, or remove
    student records without needing special login.
    """
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(
            {'error': 'Student not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ============================================================================
# CLASS-BASED VIEWS (using APIView)
# ============================================================================

class StudentListCreateAPIView(APIView):
    """
    Class-based view using APIView base class
    
    More organized than function-based views, especially for complex logic.
    Like organizing your tools in a toolbox instead of scattered on a table.
    
    Real-life example:
    Like a well-organized restaurant - different methods handle different
    tasks (get = take orders, post = process orders), all in one organized class.
    """
    permission_classes = [AllowAny]  # Allow anyone for basics tutorial
    
    def get(self, request):
        """Handle GET requests - List all students"""
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """Handle POST requests - Create a new student"""
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetailAPIView(APIView):
    """
    Class-based view for individual student operations
    
    Real-life example:
    Like a student information desk - you can view (GET), update (PUT/PATCH),
    or remove (DELETE) a specific student's record.
    """
    permission_classes = [AllowAny]  # Allow anyone for basics tutorial
    
    def get_object(self, pk):
        """Helper method to get student or return 404"""
        return get_object_or_404(Student, pk=pk)
    
    def get(self, request, pk):
        """Retrieve a specific student"""
        student = self.get_object(pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """Full update"""
        student = self.get_object(pk)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        """Partial update"""
        student = self.get_object(pk)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """Delete a student"""
        student = self.get_object(pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ============================================================================
# GENERIC VIEWS (Pre-built views for common operations)
# ============================================================================

class CourseListCreateView(ListCreateAPIView):
    """
    Generic view that handles both listing and creation
    
    ListCreateAPIView provides:
    - GET: List all objects
    - POST: Create new object
    
    You only need to specify:
    - queryset: What data to work with
    - serializer_class: How to serialize/deserialize
    
    Real-life example:
    Like a self-service kiosk - you can view the menu (GET) and place orders (POST)
    without needing special permissions (AllowAny).
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]  # Allow anyone (for basics tutorial)


class CourseDetailView(RetrieveUpdateDestroyAPIView):
    """
    Generic view for retrieve, update, and delete operations
    
    RetrieveUpdateDestroyAPIView provides:
    - GET: Retrieve single object
    - PUT: Full update
    - PATCH: Partial update
    - DELETE: Delete object
    
    Real-life example:
    Like a product detail page - you can view (GET), edit (PUT/PATCH),
    or remove (DELETE) the product information.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]  # Allow anyone (for basics tutorial)


# You can also use individual generic views:
# - ListAPIView: Only list
# - CreateAPIView: Only create
# - RetrieveAPIView: Only retrieve
# - UpdateAPIView: Only update
# - DestroyAPIView: Only delete

