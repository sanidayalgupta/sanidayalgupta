"""
URL configuration for drf_tutorial project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
Main URL Configuration for DRF Tutorial Project

This project demonstrates Django REST Framework concepts from basics to advanced.
Each app represents a different level of complexity.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Swagger/OpenAPI Documentation - Beautiful API docs!
    # Like an interactive manual for your API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI - Interactive API documentation (try it out!)
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # ReDoc - Alternative documentation view (cleaner, more readable)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Tutorial Apps - Progressive Learning Path
    path('api/basics/', include('basics.urls')),           # Level 1: Basics
    path('api/intermediate/', include('intermediate.urls')), # Level 2: Intermediate
    path('api/advanced/', include('advanced.urls')),       # Level 3: Advanced
    path('api/expert/', include('expert.urls')),           # Level 4: Expert
    
    # DRF Authentication URLs (for token authentication)
    path('api-auth/', include('rest_framework.urls')),     # Browsable API login
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
