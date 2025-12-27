from django.contrib import admin
from .models import Company, Department, Employee, Project, Task

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'founded_year', 'headquarters', 'employee_count', 'created_at']
    list_filter = ['founded_year', 'created_at']
    search_fields = ['name', 'description', 'headquarters']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'manager', 'budget', 'created_at']
    list_filter = ['company', 'created_at']
    search_fields = ['name', 'description', 'company__name']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id', 'position', 'department', 'salary', 'is_active', 'hire_date']
    list_filter = ['is_active', 'position', 'department', 'hire_date']
    search_fields = ['user__username', 'user__email', 'employee_id', 'position']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'department', 'manager', 'status', 'start_date', 'budget']
    list_filter = ['status', 'company', 'department', 'start_date']
    search_fields = ['name', 'description']
    filter_horizontal = ['employees']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'assigned_to', 'priority', 'status', 'due_date']
    list_filter = ['status', 'priority', 'project', 'due_date']
    search_fields = ['title', 'description', 'project__name']

