# Authentication & Authorization

## 🔐 Authentication

### What is Authentication?

**Definition:** Authentication verifies who you are (login/identity).

**Real-life example:**
Like showing ID at the entrance - "Are you who you say you are?"

### Session Authentication

**Definition:** Session authentication uses Django's session framework. The server stores session data.

**Real-life example:**
Like a membership card - you show it once, and the system remembers you.

**Example:**
```python
# In settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ]
}
```

**How it works:**
1. User logs in (gets session cookie)
2. Browser sends cookie with each request
3. Server checks cookie to identify user

### Basic Authentication

**Definition:** Basic Authentication sends username and password with each request (encoded but not encrypted).

**Real-life example:**
Like showing ID every time you enter - not very secure, mainly for testing.

**Example:**
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
    ]
}

# Client sends:
# Authorization: Basic base64(username:password)
```

**⚠️ Warning:** Not secure for production! Use only with HTTPS.

### Token Authentication

**Definition:** Token authentication uses a unique token for each user. The client sends the token with each request.

**Real-life example:**
Like a keycard - you have a unique card (token) that grants access.

**Setup:**
```python
# settings.py
INSTALLED_APPS = [
    ...
    'rest_framework.authtoken',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}

# Create token for user
from rest_framework.authtoken.models import Token
token, created = Token.objects.get_or_create(user=user)
```

**Usage:**
```python
# Client sends:
# Authorization: Token abc123def456

# In view
class MyView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user  # Authenticated user
        return Response({'username': user.username})
```

### JWT Authentication

**Definition:** JWT (JSON Web Token) is a stateless authentication method. The token contains user information.

**Real-life example:**
Like a passport - it contains your identity information, and anyone can verify it.

**Setup:**
```bash
pip install djangorestframework-simplejwt
```

```python
# settings.py
INSTALLED_APPS = [
    'rest_framework_simplejwt',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

# urls.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]
```

**Usage:**
```python
# Client gets token
POST /api/token/
Body: {"username": "user", "password": "pass"}

# Response: {"access": "...", "refresh": "..."}

# Client uses token
# Authorization: Bearer <access_token>
```

### OAuth2

**Definition:** OAuth2 allows users to grant limited access to their resources without sharing passwords.

**Real-life example:**
Like "Login with Google" - you authorize an app to access your Google account without giving your password.

**Note:** Requires `django-oauth-toolkit` or similar package.

### OpenID Connect (OIDC)

**Definition:** OIDC is a layer on top of OAuth2 that provides identity information.

**Real-life example:**
Like OAuth2 but also tells you who the user is (name, email, etc.).

### Custom Authentication Classes

**Definition:** Custom authentication allows you to create your own authentication method.

**Example:**
```python
# Import authentication base class
# authentication: DRF's authentication framework
from rest_framework import authentication
# Import exception for authentication failures
from rest_framework.exceptions import AuthenticationFailed

# BaseAuthentication: Base class for custom authentication
# - Must implement authenticate() method
# - Returns (user, token) tuple on success
# - Returns None if authentication not applicable
# - Raises AuthenticationFailed on invalid credentials
# - Alternative: Use built-in authentication classes
class CustomTokenAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication using custom header token
    - Checks X-Custom-Token header
    - Validates token against database
    - Returns authenticated user
    """
    
    def authenticate(self, request):
        """
        authenticate(): Main authentication method
        request: DRF Request object
        Returns: (user, token) tuple or None
        
        Called by DRF for each request
        - Return (user, token) if authenticated
        - Return None if this auth class doesn't apply
        - Raise AuthenticationFailed if credentials invalid
        """
        # request.headers: Case-insensitive dictionary of HTTP headers
        # .get(): Returns header value or None if not found
        # 'X-Custom-Token': Custom header name (X- prefix is convention for custom headers)
        token = request.headers.get('X-Custom-Token')
        
        # If no token, this auth class doesn't apply (let other classes try)
        # Returning None allows other authentication classes to attempt authentication
        if not token:
            return None
        
        try:
            # Validate token by looking up user
            # User.objects.get(): Returns single user or raises DoesNotExist
            # custom_token: Custom field on User model (would need to be added)
            user = User.objects.get(custom_token=token)
            
            # Return tuple: (user, token)
            # user: Authenticated user (sets request.user)
            # token: Auth token (sets request.auth) - can be None if not needed
            return (user, None)
        except User.DoesNotExist:
            # Raise exception if token is invalid
            # AuthenticationFailed: DRF exception (returns 401 Unauthorized)
            # Alternative: Return None (but this is less secure - reveals token format)
            raise AuthenticationFailed('Invalid token')

# Alternative: Using decorator for token validation
# from functools import wraps
# def validate_token(token):
#     # Custom validation logic
#     return user
# 
# class CustomTokenAuthentication(authentication.BaseAuthentication):
#     def authenticate(self, request):
#         token = request.headers.get('X-Custom-Token')
#         if not token:
#             return None
#         user = validate_token(token)
#         if user:
#             return (user, token)
#         raise AuthenticationFailed('Invalid token')

**Usage:**
```python
# Apply to specific view
class MyView(APIView):
    # authentication_classes: List of authentication classes to try
    # DRF tries each class in order until one succeeds
    # Alternative: Set in settings.py DEFAULT_AUTHENTICATION_CLASSES (applies to all views)
    authentication_classes = [CustomTokenAuthentication]
    
    # permission_classes: What authenticated users can do
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # request.user: Authenticated user (set by authentication)
        # request.auth: Authentication token/credential (set by authentication)
        user = request.user  # User object from authenticate() method
        return Response({'username': user.username})
```

---

## 🛡️ Authorization / Permissions

### What is Authorization?

**Definition:** Authorization determines what you can do (permissions).

**Real-life example:**
Like access levels - "You're logged in, but can you delete this file?"

### Permission Classes

**Definition:** Permissions determine what authenticated users can do.

**Built-in Permissions:**
```python
AllowAny                    # Anyone can access
IsAuthenticated             # Must be logged in
IsAdminUser                 # Must be admin
IsAuthenticatedOrReadOnly   # Read for all, write for authenticated
```

**Example:**
```python
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class BlogPostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # Only logged-in users

class AdminViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]  # Only admins
```

### Custom Permissions

**Definition:** Custom permissions allow you to define your own access rules.

**Example:**
```python
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: only owner can edit, everyone can read
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only to owner
        return obj.author == request.user

# Usage
class BlogPostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = BlogPost.objects.all()
```

**Real Project Example:**
```python
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Admins can do anything
        if request.user.is_staff:
            return True
        
        # Owners can edit their own objects
        return obj.owner == request.user

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrAdmin]
```

### Object-level Permissions

**Definition:** Object-level permissions check permissions for specific objects, not just views.

**Example:**
```python
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

# DRF checks this automatically for retrieve, update, destroy
```

### Role-Based Access Control (RBAC)

**Definition:** RBAC assigns permissions based on user roles (admin, manager, user, etc.).

**Real-life example:**
Like job titles - Admin can do everything, Manager can manage team, User can only view.

**Example:**
```python
class IsManagerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or 
            request.user.groups.filter(name='Managers').exists()
        )

# In model
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

# Permission check
class HasRole(permissions.BasePermission):
    required_role = None
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role == self.required_role

class AdminView(APIView):
    permission_classes = [HasRole]
    required_role = 'admin'
```

### Policy-Based Permissions

**Definition:** Policy-based permissions use external policy engines to determine access.

**Real-life example:**
Like complex business rules - "User can edit if they own it OR if they're in the same department AND it's not archived."

**Example:**
```python
class PolicyBasedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check policy rules
        return self.check_policy(request.user, view.action)
    
    def check_policy(self, user, action):
        # Complex logic here
        if action == 'create':
            return user.has_perm('app.add_order')
        elif action == 'update':
            return user.has_perm('app.change_order')
        return False
```

**Real Project Example:**
```python
class OrderPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # Policy: Owner can edit
        if obj.customer == user:
            return True
        
        # Policy: Manager in same department can edit
        if (user.role == 'manager' and 
            user.department == obj.department):
            return True
        
        # Policy: Admin can always edit
        if user.is_staff:
            return True
        
        return False
```

---

## 🔄 Combining Authentication & Permissions

**Example:**
```python
class SecureViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        # Filter by authenticated user
        return Order.objects.filter(customer=self.request.user)
```

**Multiple Authentication Methods:**
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    # DRF tries each until one works
}
```

---

## 🎓 Advanced Interview Topics (4+ Years Experience)

### OAuth2 Implementation Patterns

**1. OAuth2 with django-oauth-toolkit:**
```python
# Install: pip install django-oauth-toolkit
# settings.py
INSTALLED_APPS = [
    'oauth2_provider',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Create OAuth2 application
# python manage.py shell
# from oauth2_provider.models import Application
# Application.objects.create(
#     user=user,
#     client_type=Application.CLIENT_CONFIDENTIAL,
#     authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
# )
```

**2. JWT Token Refresh Strategy:**
```python
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Try to authenticate
        result = super().authenticate(request)
        
        if result:
            user, token = result
            # Check if token is about to expire
            if token.payload.get('exp') - time.time() < 300:  # 5 minutes
                # Generate new token
                refresh = RefreshToken.for_user(user)
                # Add to response header
                request._new_access_token = str(refresh.access_token)
        
        return result
```

### Security Best Practices

**1. Token Storage:**
```python
# ❌ BAD: Store tokens in localStorage (XSS vulnerable)
# ✅ GOOD: Store in httpOnly cookies
# ✅ GOOD: Store in memory (for SPAs)

# Secure token storage in React:
# - Use httpOnly cookies (set by server)
# - Use memory storage (cleared on refresh)
# - Never store in localStorage
```

**2. CSRF Protection:**
```python
# For session authentication, CSRF is required
# For token/JWT authentication, CSRF is not needed (token in header)

# Disable CSRF for API views
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class APIView(APIView):
    # CSRF exempt for token-based auth
    pass
```

**3. Rate Limiting Authentication Endpoints:**
```python
from rest_framework.throttling import AnonRateThrottle

class LoginThrottle(AnonRateThrottle):
    rate = '5/minute'  # 5 login attempts per minute

class TokenObtainPairView(APIView):
    throttle_classes = [LoginThrottle]
    # Prevents brute force attacks
```

### Permission Patterns

**1. Dynamic Permissions:**
```python
class DynamicPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Get permission from view attribute
        required_permission = getattr(view, 'required_permission', None)
        if required_permission:
            return request.user.has_perm(required_permission)
        return True

class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = [DynamicPermission]
    required_permission = 'app.view_student'
```

**2. Time-Based Permissions:**
```python
class TimeBasedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if within business hours
        now = timezone.now()
        if now.hour < 9 or now.hour > 17:
            return False  # Outside business hours
        return True
```

**3. IP-Based Permissions:**
```python
class IPWhitelistPermission(permissions.BasePermission):
    allowed_ips = ['192.168.1.0/24', '10.0.0.0/8']
    
    def has_permission(self, request, view):
        client_ip = self.get_client_ip(request)
        return self.is_ip_allowed(client_ip)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
```

### Multi-Tenant Authentication

**1. Tenant-Aware Authentication:**
```python
class TenantTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Get tenant from header
        tenant_id = request.headers.get('X-Tenant-ID')
        if not tenant_id:
            return None
        
        # Get token
        token = request.headers.get('Authorization', '').replace('Token ', '')
        if not token:
            return None
        
        try:
            # Validate token and tenant
            user_token = Token.objects.select_related('user').get(key=token)
            user = user_token.user
            
            # Verify user belongs to tenant
            if user.tenant_id != int(tenant_id):
                raise AuthenticationFailed('Invalid tenant')
            
            return (user, token)
        except (Token.DoesNotExist, ValueError):
            raise AuthenticationFailed('Invalid token')
```

### Authentication Testing

**1. Testing Authentication:**
```python
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

class AuthenticationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'pass')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
    
    def test_token_authentication(self):
        # Authenticate with token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/protected/')
        self.assertEqual(response.status_code, 200)
    
    def test_unauthenticated_access(self):
        # No authentication
        response = self.client.get('/api/protected/')
        self.assertEqual(response.status_code, 401)
```

### JWT vs Token Authentication

**Comparison:**

| Aspect | Token Auth | JWT Auth |
|--------|-----------|----------|
| Storage | Database | Stateless |
| Revocation | Easy (delete token) | Hard (need blacklist) |
| Scalability | Requires shared DB | Stateless |
| Payload | Fixed | Customizable |
| Expiration | Manual | Built-in |
| Use Case | Single server | Microservices |

**When to Use Each:**
- **Token**: Single application, need easy revocation
- **JWT**: Microservices, stateless architecture, distributed systems

---

*This guide covers essential and advanced authentication/authorization patterns. Master these for senior Django REST Framework positions.*

