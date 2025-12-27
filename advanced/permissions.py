"""
ADVANCED: Custom Permissions

DRF provides several built-in permissions, but you can create custom ones
for more granular control over access.

Built-in permissions:
- AllowAny: Anyone can access
- IsAuthenticated: Only authenticated users
- IsAdminUser: Only admin users
- IsAuthenticatedOrReadOnly: Read for all, write for authenticated
- DjangoModelPermissions: Based on Django model permissions
"""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Others can only read.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        return obj.author == request.user


class IsAuthorOrAdmin(permissions.BasePermission):
    """
    Custom permission: Only the author or admin can modify
    """
    
    def has_object_permission(self, request, view, obj):
        # Admin can do anything
        if request.user.is_staff:
            return True
        
        # Author can modify their own posts
        if hasattr(obj, 'author'):
            return obj.author == request.user
        
        return False


class IsOwner(permissions.BasePermission):
    """
    Custom permission: Only the owner can access
    """
    
    def has_object_permission(self, request, view, obj):
        # Check if object has a user/author field
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'author'):
            return obj.author == request.user
        return False


class CanApproveComment(permissions.BasePermission):
    """
    Custom permission: Only post authors or admins can approve comments
    """
    
    def has_permission(self, request, view):
        # Only authenticated users can approve
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admin can always approve
        if request.user.is_staff:
            return True
        
        # Post author can approve comments on their posts
        if hasattr(obj, 'post') and hasattr(obj.post, 'author'):
            return obj.post.author == request.user
        
        return False

