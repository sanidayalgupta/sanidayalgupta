from django.contrib import admin
from .models import Student, Course

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'age', 'grade', 'created_at']
    list_filter = ['grade', 'created_at']
    search_fields = ['name', 'email']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'duration_hours', 'price', 'is_active']
    list_filter = ['is_active', 'instructor']
    search_fields = ['title', 'description']

