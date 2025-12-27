"""
EXPERT APP - Level 4: Advanced Patterns and Expert Concepts

This app demonstrates:
1. Deep nested serializers (creating nested objects)
2. Custom throttling classes
3. API versioning
4. Custom renderers/parsers
5. Transaction management
6. Bulk operations
7. Advanced serializer validation
8. Custom exception handling
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Company(models.Model):
    """Company model"""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    founded_year = models.IntegerField()
    headquarters = models.CharField(max_length=200)
    website = models.URLField()
    employee_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Department(models.Model):
    """Department model - belongs to Company"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    budget = models.DecimalField(max_digits=15, decimal_places=2)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='managed_departments')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['company', 'name']
    
    def __str__(self):
        return f"{self.company.name} - {self.name}"


class Employee(models.Model):
    """Employee model - belongs to Department"""
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    employee_id = models.CharField(max_length=50, unique=True)
    position = models.CharField(max_length=200)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    hire_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}"


class Project(models.Model):
    """Project model - many-to-many with employees"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='projects')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='managed_projects')
    employees = models.ManyToManyField(Employee, related_name='projects', blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('planning', 'Planning'),
            ('active', 'Active'),
            ('on_hold', 'On Hold'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='planning'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Task(models.Model):
    """Task model - belongs to Project"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='tasks')
    priority = models.CharField(
        max_length=10,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
        default='medium'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('todo', 'To Do'),
            ('in_progress', 'In Progress'),
            ('review', 'In Review'),
            ('done', 'Done'),
        ],
        default='todo'
    )
    due_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.project.name} - {self.title}"

