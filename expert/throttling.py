"""
EXPERT: Custom Throttling

Throttling controls the rate of requests that clients can make to an API.
This is important for:
- Preventing abuse
- Managing server load
- Fair usage policies

DRF provides:
1. AnonRateThrottle - For anonymous users
2. UserRateThrottle - For authenticated users
3. ScopedRateThrottle - Different rates for different views

You can create custom throttling classes for more control.
"""

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, SimpleRateThrottle


class BurstRateThrottle(UserRateThrottle):
    """
    Custom throttle for burst requests
    Allows more requests in a short period
    """
    scope = 'burst'


class SustainedRateThrottle(UserRateThrottle):
    """
    Custom throttle for sustained requests
    Lower rate over longer period
    """
    scope = 'sustained'


class EmployeeListThrottle(SimpleRateThrottle):
    """
    Custom throttle for specific view
    Different rate for employee listing
    """
    scope = 'employee_list'
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }


class ProjectCreateThrottle(UserRateThrottle):
    """
    Throttle for project creation
    More restrictive than general user throttle
    """
    scope = 'project_create'

