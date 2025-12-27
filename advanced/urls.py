from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet, CommentViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r'blogposts', BlogPostViewSet, basename='blogpost')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'profiles', UserProfileViewSet, basename='profile')

app_name = 'advanced'

urlpatterns = [
    path('', include(router.urls)),
]

