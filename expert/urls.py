from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompanyViewSet,
    DepartmentViewSet,
    EmployeeViewSet,
    ProjectViewSet,
    TaskViewSet
)

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')

app_name = 'expert'

urlpatterns = [
    path('', include(router.urls)),
]

