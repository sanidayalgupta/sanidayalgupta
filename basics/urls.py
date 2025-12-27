"""
BASICS: URL Routing

URL patterns connect HTTP requests to views.
DRF views can be used just like regular Django views in URL patterns.
"""

from django.urls import path
from . import views

app_name = 'basics'

urlpatterns = [
    # Function-based views
    path('students-fbv/', views.student_list_create, name='student-list-create-fbv'),
    path('students-fbv/<int:pk>/', views.student_detail, name='student-detail-fbv'),
    
    # Class-based views (APIView)
    path('students-cbv/', views.StudentListCreateAPIView.as_view(), name='student-list-create-cbv'),
    path('students-cbv/<int:pk>/', views.StudentDetailAPIView.as_view(), name='student-detail-cbv'),
    
    # Generic views (most common and recommended)
    path('courses/', views.CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
]

