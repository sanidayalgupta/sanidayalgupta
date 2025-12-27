"""
INTERMEDIATE: Routers

Routers automatically generate URL patterns for ViewSets.
They handle:
- Standard CRUD routes
- Custom actions (decorated with @action)
- Nested routes (if configured)

Default routes created by DefaultRouter:
- list: GET /resource/
- create: POST /resource/
- retrieve: GET /resource/{id}/
- update: PUT /resource/{id}/
- partial_update: PATCH /resource/{id}/
- destroy: DELETE /resource/{id}/
- custom_action: GET/POST /resource/{id}/custom_action/
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    AuthorViewSet,
    BookViewSet,
    ReviewViewSet
)

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'books', BookViewSet, basename='book')
router.register(r'reviews', ReviewViewSet, basename='review')

app_name = 'intermediate'

# Include router URLs
urlpatterns = [
    path('', include(router.urls)),
]

