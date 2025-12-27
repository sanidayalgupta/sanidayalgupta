"""
BASICS APP - Level 1: Introduction to DRF Concepts

This app demonstrates:
1. Basic Models
2. Serializers (ModelSerializer, Serializer)
3. API Views (Function-based and Class-based)
4. Basic CRUD operations
"""

from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    """
    Simple Student model for basic CRUD operations
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    grade = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.email}"


class Course(models.Model):
    """
    Course model for demonstrating relationships
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.CharField(max_length=100)
    duration_hours = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

