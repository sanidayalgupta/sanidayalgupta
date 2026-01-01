# Security

## 🔒 Security Best Practices

### CSRF Protection

**Definition:** CSRF (Cross-Site Request Forgery) protection prevents malicious sites from making requests on behalf of users.

**Real-life example:**
Like preventing someone from forging your signature on a check.

**In DRF:**
```python
# Session authentication uses CSRF protection automatically
# Token/JWT authentication doesn't need CSRF (stateless)

# For session auth
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ]
}
# CSRF middleware handles this automatically

# For API-only (token/JWT)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}
# CSRF not needed (stateless)
```

**Disabling CSRF for API views:**
```python
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

@csrf_exempt  # Only if absolutely necessary
class MyAPIView(APIView):
    pass
```

### CORS Configuration

**Definition:** CORS (Cross-Origin Resource Sharing) allows browsers to make requests to different domains.

**Real-life example:**
Like allowing your website to make requests to your API on a different domain.

**Setup:**
```bash
pip install django-cors-headers
```

```python
# settings.py
INSTALLED_APPS = [
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Should be near top
    'django.middleware.common.CommonMiddleware',
    ...
]

# Allow all origins (development only)
CORS_ALLOW_ALL_ORIGINS = True

# Or configure specific origins (production)
CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://www.example.com",
]

# Allow credentials
CORS_ALLOW_CREDENTIALS = True

# Allowed headers
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
```

### HTTPS Enforcement

**Definition:** HTTPS enforcement ensures all connections use secure HTTPS protocol.

**Real-life example:**
Like requiring all mail to be sent in locked boxes instead of open envelopes.

**Setup:**
```python
# settings.py
SECURE_SSL_REDIRECT = True  # Redirect HTTP to HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True  # Only send cookies over HTTPS
CSRF_COOKIE_SECURE = True  # Only send CSRF cookies over HTTPS
SECURE_HSTS_SECONDS = 31536000  # HTTP Strict Transport Security
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

**In Production (Nginx/Apache):**
```nginx
# Nginx example
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name example.com;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ...
}
```

### Sensitive Data Masking

**Definition:** Sensitive data masking hides sensitive information in logs and responses.

**Real-life example:**
Like blacking out credit card numbers in documents.

**Example:**
```python
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Mask email partially
        email = data.get('email', '')
        if email:
            parts = email.split('@')
            if len(parts) == 2:
                username = parts[0]
                domain = parts[1]
                masked_username = username[0] + '*' * (len(username) - 1)
                data['email'] = f"{masked_username}@{domain}"
        
        return data

# Response: {"email": "j***@example.com"}
```

**Logging Sensitive Data:**
```python
import logging
import re

class SensitiveDataFilter(logging.Filter):
    def filter(self, record):
        # Mask credit card numbers
        message = record.getMessage()
        message = re.sub(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', 
                        'XXXX-XXXX-XXXX-XXXX', message)
        # Mask passwords
        message = re.sub(r'password["\']?\s*[:=]\s*["\']?[^"\']+', 
                        'password="***"', message, flags=re.IGNORECASE)
        record.msg = message
        return True

LOGGING = {
    'filters': {
        'sensitive_data': {
            '()': SensitiveDataFilter,
        },
    },
    'handlers': {
        'console': {
            'filters': ['sensitive_data'],
            ...
        },
    },
}
```

### Encryption at Rest

**Definition:** Encryption at rest encrypts data stored in the database.

**Real-life example:**
Like storing valuables in a locked safe.

**Field-level Encryption:**
```python
from cryptography.fernet import Fernet
from django.db import models

class EncryptedField(models.TextField):
    def __init__(self, *args, **kwargs):
        self.encryption_key = settings.ENCRYPTION_KEY
        super().__init__(*args, **kwargs)
    
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        fernet = Fernet(self.encryption_key)
        return fernet.decrypt(value.encode()).decode()
    
    def to_python(self, value):
        if isinstance(value, str):
            return value
        if value is None:
            return value
        return self.from_db_value(value, None, None)
    
    def get_prep_value(self, value):
        if value is None:
            return value
        fernet = Fernet(self.encryption_key)
        return fernet.encrypt(value.encode()).decode()

# Usage
class User(models.Model):
    name = models.CharField(max_length=100)
    ssn = EncryptedField()  # Encrypted in database
```

### Encryption in Transit

**Definition:** Encryption in transit encrypts data during transmission (HTTPS/TLS).

**Real-life example:**
Like sending mail in locked boxes instead of open envelopes.

**Implementation:**
- Use HTTPS/TLS (covered in HTTPS Enforcement)
- Ensure all API endpoints use HTTPS
- Use secure WebSocket connections (WSS) if needed

### Prevent CWE-319 / CWE-352

**CWE-319: Cleartext Transmission of Sensitive Information**
- Always use HTTPS
- Never send passwords in query parameters
- Use secure authentication methods

**CWE-352: Cross-Site Request Forgery (CSRF)**
- Use CSRF tokens for state-changing operations
- Use SameSite cookies
- Implement proper CORS policies

**Example:**
```python
# settings.py
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Strict'

# Use HTTPS only
SECURE_SSL_REDIRECT = True
```

### Input Sanitization

**Definition:** Input sanitization cleans and validates user input to prevent attacks.

**Real-life example:**
Like checking mail for dangerous items before accepting it.

**Example:**
```python
from django.utils.html import strip_tags
from django.utils.text import slugify

class PostSerializer(serializers.ModelSerializer):
    content = serializers.CharField()
    
    def validate_content(self, value):
        # Remove HTML tags
        cleaned = strip_tags(value)
        
        # Check length
        if len(cleaned) < 10:
            raise serializers.ValidationError("Content too short")
        
        # Check for SQL injection patterns
        dangerous_patterns = ['DROP TABLE', 'DELETE FROM', '--']
        for pattern in dangerous_patterns:
            if pattern.lower() in value.lower():
                raise serializers.ValidationError("Invalid content")
        
        return cleaned
```

**Using bleach for HTML sanitization:**
```bash
pip install bleach
```

```python
import bleach

def sanitize_html(value):
    allowed_tags = ['p', 'br', 'strong', 'em', 'a']
    allowed_attributes = {'a': ['href']}
    return bleach.clean(value, tags=allowed_tags, attributes=allowed_attributes)
```

### Secure Headers

**Definition:** Secure headers add security-related HTTP headers to responses.

**Real-life example:**
Like adding security instructions to documents.

**Setup with django-secure:**
```bash
pip install django-secure
```

```python
# settings.py
INSTALLED_APPS = [
    'djangosecure',
]

MIDDLEWARE = [
    'djangosecure.middleware.SecurityMiddleware',
    ...
]

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'  # Prevent clickjacking
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
```

**Manual Headers:**
```python
from rest_framework.response import Response

class SecureAPIView(APIView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response
```

**Using django-cors-headers for CORS security:**
```python
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "https://trusted-domain.com",
]
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
```

---

## 🎓 Advanced Interview Topics (4+ Years Experience)

### Security Headers

**1. Comprehensive Security Headers:**
```python
# django-security package
INSTALLED_APPS = ['django_security']

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Input Sanitization

**1. XSS Prevention:**
```python
from django.utils.html import escape

def sanitize_input(data):
    """Sanitize user input"""
    if isinstance(data, str):
        return escape(data)
    elif isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(item) for item in data]
    return data
```

### SQL Injection Prevention

**1. Always Use ORM:**
```python
# ❌ BAD: SQL injection vulnerable
Student.objects.raw(f"SELECT * FROM students WHERE name = '{name}'")

# ✅ GOOD: ORM prevents injection
Student.objects.filter(name=name)
```

### Rate Limiting Security

**1. IP-Based Rate Limiting:**
```python
from rest_framework.throttling import UserRateThrottle

class IPRateThrottle(UserRateThrottle):
    def get_cache_key(self, request, view):
        # Rate limit by IP address
        ident = self.get_ident(request)
        return f'throttle_ip_{ident}'
```

### Security Audit

**1. Dependency Scanning:**
```bash
# Install: pip install safety
safety check

# Or use: pip-audit
pip-audit
```

---

*This guide covers essential and advanced security patterns. Master these for senior Django REST Framework positions.*

