"""
EXPERT: Advanced Serializer Patterns

This demonstrates:
1. Deep nested serializers with write operations
2. Writable nested serializers
3. Custom field serialization
4. Complex validation
5. Bulk operations
6. SerializerMethodField with parameters
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from .models import Company, Department, Employee, Project, Task


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']


# ============================================================================
# Nested Serializers with Write Operations
# ============================================================================

class TaskSerializer(serializers.ModelSerializer):
    """Task serializer"""
    assigned_to_name = serializers.CharField(source='assigned_to.user.get_full_name', read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'assigned_to', 'assigned_to_name',
            'priority', 'status', 'due_date', 'completed_at', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class EmployeeNestedSerializer(serializers.ModelSerializer):
    """Nested employee serializer for use in other serializers"""
    user = UserSerializer(read_only=True)
    tasks_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Employee
        fields = [
            'id', 'user', 'employee_id', 'position', 'salary',
            'hire_date', 'is_active', 'tasks_count'
        ]
        read_only_fields = ['id']
    
    def get_tasks_count(self, obj):
        """Get count of tasks"""
        return obj.tasks.count() if hasattr(obj, 'tasks') else 0


class DepartmentNestedSerializer(serializers.ModelSerializer):
    """Nested department serializer"""
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)
    employees_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = [
            'id', 'name', 'description', 'budget', 'manager', 'manager_name',
            'employees_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_employees_count(self, obj):
        """Get count of employees"""
        return obj.employees.count() if hasattr(obj, 'employees') else 0


class CompanySerializer(serializers.ModelSerializer):
    """Company serializer with nested departments"""
    departments = DepartmentNestedSerializer(many=True, read_only=True)
    departments_count = serializers.SerializerMethodField()
    employees_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'description', 'founded_year', 'headquarters',
            'website', 'employee_count', 'departments', 'departments_count',
            'employees_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_departments_count(self, obj):
        """Count departments"""
        return obj.departments.count()
    
    def get_employees_count(self, obj):
        """Count all employees across departments"""
        total = 0
        for dept in obj.departments.all():
            total += dept.employees.count()
        return total


class DepartmentSerializer(serializers.ModelSerializer):
    """Department serializer with nested employees"""
    company_name = serializers.CharField(source='company.name', read_only=True)
    employees = EmployeeNestedSerializer(many=True, read_only=True)
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)
    
    class Meta:
        model = Department
        fields = [
            'id', 'company', 'company_name', 'name', 'description', 'budget',
            'manager', 'manager_name', 'employees', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Employee serializer with nested user and department info
    
    This serializer can be used for both reading (with nested user info)
    and writing (with user ID for ForeignKey relationship).
    """
    user = UserSerializer(read_only=True)  # Read-only: shows user details when reading
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True,
        required=False
    )
    department_name = serializers.CharField(source='department.name', read_only=True)
    company_name = serializers.CharField(source='department.company.name', read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    
    class Meta:
        model = Employee
        fields = [
            'id', 'department', 'department_name', 'company_name', 'user', 'user_id',
            'employee_id', 'position', 'salary', 'hire_date', 'is_active',
            'tasks', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


# ============================================================================
# Writable Nested Serializers
# ============================================================================

class DepartmentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating departments with nested employees
    """
    employees = EmployeeNestedSerializer(many=True, required=False)
    
    class Meta:
        model = Department
        fields = ['company', 'name', 'description', 'budget', 'manager', 'employees']
    
    def create(self, validated_data):
        """
        Create department and employees in a transaction using context manager
        
        What it does:
        Creates a department and its employees atomically. If any part fails,
        everything is rolled back. Uses Django's transaction.atomic() context manager.
        
        Real-life example:
        Like buying a house with furniture - either you get everything (commit)
        or nothing (rollback). You don't want a house without furniture or
        furniture without a house.
        
        Context Manager Explanation:
        transaction.atomic() is a context manager that:
        1. Starts a database transaction (enters)
        2. Executes your code
        3. Commits if successful, rolls back if error (exits)
        """
        employees_data = validated_data.pop('employees', [])
        
        # transaction.atomic() is a context manager - ensures all-or-nothing
        # If any employee creation fails, department creation is also rolled back
        with transaction.atomic():  # Context manager ensures transaction safety
            department = Department.objects.create(**validated_data)
            
            for employee_data in employees_data:
                # Extract user data if nested
                user_data = employee_data.pop('user', None)
                if user_data:
                    user = User.objects.create(**user_data)
                    employee_data['user'] = user
                
                Employee.objects.create(department=department, **employee_data)
        
        # If we reach here, everything succeeded and transaction was committed
        return department


class ProjectSerializer(serializers.ModelSerializer):
    """Project serializer with nested tasks"""
    company_name = serializers.CharField(source='company.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)
    employees = EmployeeNestedSerializer(many=True, read_only=True)
    employee_ids = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        many=True,
        source='employees',
        write_only=True,
        required=False
    )
    tasks = TaskSerializer(many=True, read_only=True)
    tasks_count = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'company', 'company_name',
            'department', 'department_name', 'manager', 'manager_name',
            'employees', 'employee_ids', 'start_date', 'end_date',
            'budget', 'status', 'tasks', 'tasks_count', 'progress_percentage',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_tasks_count(self, obj):
        """Get total tasks count"""
        return obj.tasks.count() if hasattr(obj, 'tasks') else 0
    
    def get_progress_percentage(self, obj):
        """Calculate project progress based on tasks"""
        tasks = obj.tasks.all() if hasattr(obj, 'tasks') else []
        if not tasks:
            return 0
        
        done_tasks = sum(1 for task in tasks if task.status == 'done')
        return round((done_tasks / len(tasks)) * 100, 2)
    
    def validate(self, data):
        """Object-level validation"""
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if end_date and start_date and end_date < start_date:
            raise serializers.ValidationError({
                'end_date': 'End date must be after start date'
            })
        
        return data


class ProjectCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating projects with nested tasks - Writable Nested Serializer
    
    What is a Writable Nested Serializer?
    A writable nested serializer allows you to create related objects (tasks)
    along with the main object (project) in a single request. This is different
    from read-only nested serializers which only display related data.
    
    Real-life example:
    Like ordering a pizza with toppings - you specify the pizza (project) and
    toppings (tasks) in one order, and they're created together.
    
    This demonstrates:
    - Creating parent object (project) with child objects (tasks) in one request
    - Transaction safety (all-or-nothing)
    - Nested data handling
    """
    tasks = TaskSerializer(many=True, required=False)  # Nested tasks serializer
    
    class Meta:
        model = Project
        fields = [
            'name', 'description', 'company', 'department', 'manager',
            'start_date', 'end_date', 'budget', 'status', 'tasks'
        ]
    
    def create(self, validated_data):
        """
        Create project and tasks in a transaction using context manager
        
        What it does:
        Creates a project and its tasks atomically. Uses transaction.atomic()
        context manager to ensure all-or-nothing behavior.
        
        Real-life example:
        Like booking a hotel room with amenities - either you get the room
        with all amenities (commit) or nothing (rollback).
        
        Context Manager Explanation:
        transaction.atomic() is a context manager that:
        1. Starts a database transaction when entering (with statement)
        2. Executes your code
        3. Commits if successful, rolls back if error when exiting
        This prevents partial data (project without tasks or vice versa).
        """
        tasks_data = validated_data.pop('tasks', [])  # Extract nested tasks data
        
        # Context manager: ensures transaction safety
        # Enter: starts transaction
        # Exit: commits if success, rolls back if error
        with transaction.atomic():  # This is a context manager!
            # Create the main object (project)
            project = Project.objects.create(**validated_data)
            
            # Create related objects (tasks) in the same transaction
            for task_data in tasks_data:
                Task.objects.create(project=project, **task_data)
        
        # If we reach here, everything succeeded and was committed
        return project


# ============================================================================
# Bulk Operations Serializer
# ============================================================================

class BulkEmployeeCreateSerializer(serializers.Serializer):
    """
    Serializer for bulk creating employees
    """
    employees = EmployeeSerializer(many=True)
    
    def create(self, validated_data):
        """
        Bulk create employees using transaction context manager
        
        What it does:
        Creates multiple employees in a single transaction. If any employee
        creation fails, all are rolled back. Demonstrates bulk operations with
        transaction safety.
        
        Real-life example:
        Like hiring a team - either all candidates pass background checks and
        are hired (commit), or if any fails, none are hired (rollback).
        
        Context Manager Benefits:
        - Automatic rollback on error (no partial data)
        - Cleaner code (no manual try/except needed)
        - Guaranteed consistency (all-or-nothing)
        """
        employees_data = validated_data['employees']
        employees = []
        
        # Context manager ensures transaction safety
        # If any employee creation fails, all are rolled back
        with transaction.atomic():  # Enter: start transaction
            for employee_data in employees_data:
                employees.append(Employee.objects.create(**employee_data))
        
        # Exit: commit if successful, rollback if error
        return {'employees': employees}

