"""
EXPERT: Advanced ViewSet Patterns - The Professional Level

This demonstrates expert-level patterns used in production applications.
Think of this as the "master chef" level - using advanced techniques
to create high-performance, scalable APIs.

Real-life analogy:
Like a professional kitchen - everything is optimized:
- Throttling = Controlling how many orders come in (prevent kitchen overload)
- Transactions = Making sure all ingredients are ready before cooking (all-or-nothing)
- Bulk operations = Cooking multiple dishes at once (efficiency)
- Query optimization = Prepping ingredients in advance (faster service)
- Caching = Keeping popular dishes ready (instant service)

This demonstrates:
1. Custom throttling per action - Different speed limits for different roads
2. Transaction management - All-or-nothing operations (like bank transfers)
3. Bulk operations - Processing multiple items at once (like batch cooking)
4. Complex queryset optimization - Smart database queries (like efficient shopping)
5. Caching - Storing frequently accessed data (like keeping popular items in front)
6. Advanced filtering and aggregation - Complex data analysis (like sales reports)
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.db import transaction
from django.db.models import Count, Sum, Avg, Q
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Company, Department, Employee, Project, Task
from .serializers import (
    CompanySerializer,
    DepartmentSerializer,
    DepartmentCreateSerializer,
    EmployeeSerializer,
    EmployeeNestedSerializer,
    ProjectSerializer,
    ProjectCreateSerializer,
    TaskSerializer,
    BulkEmployeeCreateSerializer
)
from .throttling import (
    BurstRateThrottle,
    SustainedRateThrottle,
    EmployeeListThrottle,
    ProjectCreateThrottle
)
from .caching import (
    cache_key_company_list,
    cache_key_company_detail,
    cache_key_company_statistics,
    CacheMixin
)
from .context_managers import (
    timing_context,
    logging_context,
    cache_invalidation_context,
    transaction_with_timing
)
import logging

logger = logging.getLogger(__name__)


class CompanyViewSet(viewsets.ModelViewSet, CacheMixin):
    """
    Company ViewSet with Advanced Features - The Smart Company Manager
    
    This ViewSet demonstrates multiple expert patterns working together.
    Think of it as a smart office manager that:
    - Controls access (authentication/permissions)
    - Limits requests (throttling)
    - Speeds up responses (caching)
    - Optimizes queries (prefetch_related)
    
    Real-life example:
    Like a corporate headquarters that efficiently manages all departments,
    employees, and projects with smart systems in place.
    """
    # prefetch_related = Load related data in advance (like pre-loading all departments)
    # This is like getting all ingredients ready before cooking - much faster!
    queryset = Company.objects.prefetch_related('departments', 'departments__employees').all()
    serializer_class = CompanySerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    # Filtering = Like a search engine for your data
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'description', 'headquarters']  # Fields you can search
    ordering_fields = ['name', 'founded_year', 'employee_count', 'created_at']  # Fields you can sort by
    ordering = ['-created_at']  # Default: newest first (like newest posts on social media)
    
    def get_throttles(self):
        """
        Custom throttling based on action - The Traffic Controller
        
        Different actions have different speed limits.
        Like a highway - some lanes have higher speed limits than others.
        
        Real-life example:
        - List view (many companies) = Higher limit (like a wide highway)
        - Detail view (one company) = Lower limit (like a narrow street)
        """
        if self.action == 'list':
            return [BurstRateThrottle()]  # Allow more requests for listing
        return [SustainedRateThrottle()]  # Lower rate for other actions
    
    def list(self, request, *args, **kwargs):
        """
        List companies with caching - The Fast List
        
        This checks cache first (like checking if menu is already printed).
        If found, returns immediately. If not, fetches from database and caches it.
        
        Real-life example:
        Like a restaurant keeping today's menu ready - if someone asks,
        they give the ready menu (cache) instead of creating a new one (database).
        """
        cache_key = cache_key_company_list()
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            # Return cached data immediately (like instant service)
            return Response(cached_data)
        
        # If not in cache, get from database (like going to storage)
        response = super().list(request, *args, **kwargs)
        
        # Store in cache for next time (like keeping a copy ready)
        cache.set(cache_key, response.data, 300)  # Cache for 5 minutes
        
        return response
    
    def retrieve(self, request, *args, **kwargs):
        """
        Get single company with caching - The Fast Lookup
        
        Like looking up a contact in your phone - if you recently looked it up,
        it's faster (cache). Otherwise, you search (database).
        """
        company = self.get_object()
        cache_key = cache_key_company_detail(company.pk)
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
        
        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, 300)
        
        return response
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """
        Custom action: GET /companies/{id}/statistics/ - The Report Generator
        
        Returns aggregated statistics about a company.
        This is expensive to calculate (like generating a financial report),
        so we cache it heavily.
        
        Real-life example:
        Like a company's annual report - it takes time to compile all the data,
        so once it's ready, you keep copies (cache) for quick access.
        """
        company = self.get_object()
        cache_key = cache_key_company_statistics(company.pk)
        
        # Check cache first (like checking if report is already printed)
        cached_stats = cache.get(cache_key)
        if cached_stats is not None:
            return Response(cached_stats)
        
        # Calculate statistics (like compiling the report)
        # This is expensive, so we cache the result
        stats = {
            'total_departments': company.departments.count(),  # Count departments
            'total_employees': sum(dept.employees.count() for dept in company.departments.all()),  # Sum all employees
            'total_projects': company.projects.count(),  # Count projects
            'active_projects': company.projects.filter(status='active').count(),  # Count active ones
            'total_budget': company.departments.aggregate(Sum('budget'))['budget__sum'] or 0,  # Sum all budgets
            'average_salary': Employee.objects.filter(
                department__company=company
            ).aggregate(Avg('salary'))['salary__avg'] or 0,  # Calculate average
        }
        
        # Cache for 10 minutes (statistics don't change often)
        cache.set(cache_key, stats, 600)
        
        return Response(stats)
    
    def perform_create(self, serializer):
        """
        Override create to clear cache - The Cache Invalidator
        
        When a new company is created, we need to clear the list cache
        because the list has changed. Like updating a menu when a new dish is added.
        """
        super().perform_create(serializer)
        # Clear the list cache (new company added, list changed)
        cache.delete(cache_key_company_list())
    
    def perform_update(self, serializer):
        """
        Override update to clear cache - Keep Cache Fresh
        
        When company is updated, clear its detail cache and statistics cache.
        Like updating a document - old copies are invalid.
        """
        company = self.get_object()
        super().perform_update(serializer)
        # Clear caches for this company
        cache.delete(cache_key_company_detail(company.pk))
        cache.delete(cache_key_company_statistics(company.pk))
        cache.delete(cache_key_company_list())  # Also clear list cache


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    Department ViewSet with nested creation
    """
    queryset = Department.objects.select_related('company', 'manager').prefetch_related('employees').all()
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['company', 'manager']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'budget', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Different serializers for different actions"""
        if self.action == 'create':
            return DepartmentCreateSerializer
        return DepartmentSerializer
    
    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """Get employees in this department"""
        department = self.get_object()
        employees = department.employees.select_related('user', 'department').all()
        serializer = EmployeeNestedSerializer(employees, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_employee(self, request, pk=None):
        """Add employee to department"""
        department = self.get_object()
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(department=department)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    Employee ViewSet with custom throttling
    """
    queryset = Employee.objects.select_related('user', 'department', 'department__company').prefetch_related('tasks', 'projects').all()
    serializer_class = EmployeeSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['department', 'is_active', 'position']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'position', 'employee_id']
    ordering_fields = ['hire_date', 'salary', 'created_at']
    ordering = ['-created_at']
    
    def get_throttles(self):
        """Custom throttling for list action"""
        if self.action == 'list':
            return [EmployeeListThrottle()]
        return super().get_throttles()
    
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """
        Custom action: POST /employees/bulk_create/
        Bulk create employees using context managers
        
        What it does:
        Creates multiple employees in a single transaction with timing and logging.
        Demonstrates context managers for resource management.
        
        Real-life example:
        Like a factory assembly line - you set up the line (context manager),
        process multiple items (bulk create), and automatically clean up (context manager exits).
        """
        # Use context managers for timing and logging
        # Note: Transaction is handled in serializer, so we don't nest it here
        # This demonstrates context managers for logging and timing
        with logging_context('bulk_create_employees'), \
             timing_context('bulk_employee_creation'):
            
            serializer = BulkEmployeeCreateSerializer(data=request.data)
            if serializer.is_valid():
                # Serializer handles transaction internally
                result = serializer.save()
                logger.info(f'Bulk created {len(result["employees"])} employees')
                return Response(
                    EmployeeSerializer(result['employees'], many=True).data,
                    status=status.HTTP_201_CREATED
                )
            else:
                logger.warning(f'Bulk create validation failed: {serializer.errors}')
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        """Get tasks assigned to employee"""
        employee = self.get_object()
        tasks = employee.tasks.select_related('project').all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def projects(self, request, pk=None):
        """Get projects employee is working on"""
        employee = self.get_object()
        projects = employee.projects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Project ViewSet with advanced features
    """
    queryset = Project.objects.select_related(
        'company', 'department', 'manager'
    ).prefetch_related('employees', 'tasks').all()
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['company', 'department', 'manager', 'status']
    search_fields = ['name', 'description']
    ordering_fields = ['start_date', 'end_date', 'budget', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Different serializers for different actions"""
        if self.action == 'create':
            return ProjectCreateSerializer
        return ProjectSerializer
    
    def get_throttles(self):
        """Custom throttling for create action"""
        if self.action == 'create':
            return [ProjectCreateThrottle()]
        return super().get_throttles()
    
    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        """Get tasks for this project"""
        project = self.get_object()
        tasks = project.tasks.select_related('assigned_to', 'assigned_to__user').all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_task(self, request, pk=None):
        """Add task to project"""
        project = self.get_object()
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def assign_employee(self, request, pk=None):
        """Assign employee to project"""
        project = self.get_object()
        employee_id = request.data.get('employee_id')
        
        try:
            employee = Employee.objects.get(id=employee_id)
            project.employees.add(employee)
            return Response({'message': 'Employee assigned successfully'})
        except Employee.DoesNotExist:
            return Response(
                {'error': 'Employee not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        """Get project progress statistics"""
        project = self.get_object()
        tasks = project.tasks.all()
        
        progress = {
            'total_tasks': tasks.count(),
            'todo': tasks.filter(status='todo').count(),
            'in_progress': tasks.filter(status='in_progress').count(),
            'review': tasks.filter(status='review').count(),
            'done': tasks.filter(status='done').count(),
            'completion_percentage': 0
        }
        
        if progress['total_tasks'] > 0:
            progress['completion_percentage'] = round(
                (progress['done'] / progress['total_tasks']) * 100, 2
            )
        
        return Response(progress)


class TaskViewSet(viewsets.ModelViewSet):
    """
    Task ViewSet
    """
    queryset = Task.objects.select_related('project', 'assigned_to', 'assigned_to__user').all()
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['project', 'assigned_to', 'status', 'priority']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark task as complete"""
        task = self.get_object()
        from django.utils import timezone
        
        task.status = 'done'
        task.completed_at = timezone.now()
        task.save()
        
        serializer = self.get_serializer(task)
        return Response(serializer.data)

