# Exception Handling

## ⚠️ Exception Handling in DRF

### What is Exception Handling?

**Definition:** Exception handling manages errors and exceptions in a consistent way, providing meaningful error responses to clients.

**Real-life example:**
Like error messages on forms - instead of crashing, you show helpful messages like "Email already exists" or "Password too short".

### DRF Default Exceptions

**Definition:** DRF provides default exception handling for common errors.

**Built-in Exceptions:**
```python
from rest_framework.exceptions import (
    APIException,
    NotFound,
    PermissionDenied,
    ValidationError,
    AuthenticationFailed,
    NotAuthenticated,
    MethodNotAllowed,
    Throttled,
)

# Common exceptions
ValidationError          # 400 - Invalid input data
AuthenticationFailed     # 401 - Invalid authentication
NotAuthenticated        # 401 - No authentication provided
PermissionDenied        # 403 - Insufficient permissions
NotFound                # 404 - Resource not found
MethodNotAllowed        # 405 - HTTP method not allowed
Throttled               # 429 - Rate limit exceeded
```

**Example:**
```python
from rest_framework.exceptions import NotFound

class BookViewSet(viewsets.ModelViewSet):
    def get_object(self):
        try:
            return super().get_object()
        except Book.DoesNotExist:
            raise NotFound("Book not found")
```

### Custom Exception Classes

**Definition:** Custom exceptions allow you to create domain-specific error responses.

**Example:**
```python
from rest_framework.exceptions import APIException
from rest_framework import status

class InsufficientStockException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Insufficient stock available'
    default_code = 'insufficient_stock'

class PaymentFailedException(APIException):
    status_code = status.HTTP_402_PAYMENT_REQUIRED
    default_detail = 'Payment processing failed'
    default_code = 'payment_failed'

# Usage
class OrderViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        product = Product.objects.get(id=request.data['product_id'])
        quantity = request.data['quantity']
        
        if product.stock < quantity:
            raise InsufficientStockException(
                f'Only {product.stock} items available, requested {quantity}'
            )
        
        # Process order...
```

**Advanced Custom Exception:**
```python
from rest_framework.exceptions import APIException
from rest_framework import status

class BusinessLogicException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    
    def __init__(self, detail=None, code=None, errors=None):
        super().__init__(detail, code)
        self.errors = errors or {}
    
    def get_full_details(self):
        return {
            'error': self.default_detail,
            'code': self.default_code,
            'details': self.errors
        }

# Usage
raise BusinessLogicException(
    detail='Order validation failed',
    errors={
        'items': ['At least one item required'],
        'payment': ['Payment method invalid']
    }
)
```

### Global Exception Handler

**Definition:** Global exception handler customizes how all exceptions are handled across your API.

**Setup:**
```python
# exceptions.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """Custom exception handler"""
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)
    
    # Customize response
    if response is not None:
        custom_response_data = {
            'error': {
                'status_code': response.status_code,
                'message': str(exc),
                'details': response.data
            }
        }
        response.data = custom_response_data
    
    # Handle unhandled exceptions
    else:
        # Log unexpected exceptions
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        
        custom_response_data = {
            'error': {
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'An unexpected error occurred',
                'details': str(exc) if settings.DEBUG else None
            }
        }
        response = Response(custom_response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response

# settings.py
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'myapp.exceptions.custom_exception_handler',
}
```

**Enhanced Exception Handler:**
```python
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        # Add request ID for tracking
        request = context.get('request')
        request_id = getattr(request, 'id', None)
        
        custom_response = {
            'success': False,
            'error': {
                'code': response.status_code,
                'message': get_error_message(response.data),
                'request_id': request_id,
                'timestamp': timezone.now().isoformat(),
            }
        }
        
        # Add validation errors if present
        if isinstance(exc, ValidationError):
            custom_response['error']['validation_errors'] = response.data
        
        response.data = custom_response
    
    return response

def get_error_message(data):
    """Extract error message from exception data"""
    if isinstance(data, dict):
        if 'detail' in data:
            return data['detail']
        # Return first error message
        return list(data.values())[0][0] if data.values() else 'Validation error'
    return str(data)
```

### Error Format Standardization

**Definition:** Standardizing error response format ensures consistent error structure across all endpoints.

**Standard Error Format:**
```python
# Standard format
{
    "success": false,
    "error": {
        "code": 400,
        "message": "Validation failed",
        "type": "ValidationError",
        "details": {
            "field_name": ["Error message"]
        },
        "request_id": "abc123",
        "timestamp": "2024-01-01T12:00:00Z"
    }
}
```

**Implementation:**
```python
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import uuid

class StandardErrorResponse:
    @staticmethod
    def format_error(exc, context, response=None):
        """Format error in standard structure"""
        request = context.get('request')
        
        error_data = {
            'success': False,
            'error': {
                'code': response.status_code if response else status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': StandardErrorResponse.get_error_message(exc, response),
                'type': exc.__class__.__name__,
                'request_id': getattr(request, 'id', str(uuid.uuid4())),
                'timestamp': timezone.now().isoformat(),
            }
        }
        
        # Add details for validation errors
        if response and isinstance(response.data, dict):
            if 'detail' in response.data:
                error_data['error']['details'] = response.data['detail']
            else:
                error_data['error']['details'] = response.data
        
        return error_data
    
    @staticmethod
    def get_error_message(exc, response):
        """Extract error message"""
        if response and isinstance(response.data, dict):
            if 'detail' in response.data:
                return str(response.data['detail'])
            # Get first error message
            if response.data:
                first_error = list(response.data.values())[0]
                if isinstance(first_error, list) and first_error:
                    return str(first_error[0])
        return str(exc)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        error_data = StandardErrorResponse.format_error(exc, context, response)
        response.data = error_data
    else:
        # Handle unhandled exceptions
        error_data = StandardErrorResponse.format_error(exc, context)
        response = Response(error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response
```

**Real Project Example:**
```python
# exceptions.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
import uuid
import logging

logger = logging.getLogger(__name__)

class APIExceptionHandler:
    @staticmethod
    def handle(exc, context):
        """Main exception handler"""
        # Get DRF's default handler response
        response = exception_handler(exc, context)
        
        # Standardize error format
        if response:
            return APIExceptionHandler.format_response(exc, context, response)
        
        # Handle unexpected exceptions
        return APIExceptionHandler.handle_unexpected(exc, context)
    
    @staticmethod
    def format_response(exc, context, response):
        """Format error response"""
        request = context.get('request')
        
        error_response = {
            'success': False,
            'error': {
                'code': response.status_code,
                'message': APIExceptionHandler.get_message(exc, response),
                'type': exc.__class__.__name__,
                'request_id': getattr(request, 'request_id', str(uuid.uuid4())),
                'timestamp': timezone.now().isoformat(),
            }
        }
        
        # Add validation details
        if hasattr(exc, 'detail'):
            if isinstance(exc.detail, dict):
                error_response['error']['validation_errors'] = exc.detail
            else:
                error_response['error']['details'] = str(exc.detail)
        
        response.data = error_response
        return response
    
    @staticmethod
    def get_message(exc, response):
        """Extract error message"""
        if hasattr(exc, 'detail'):
            if isinstance(exc.detail, dict) and 'detail' in exc.detail:
                return str(exc.detail['detail'])
            return str(exc.detail)
        return str(exc)
    
    @staticmethod
    def handle_unexpected(exc, context):
        """Handle unexpected exceptions"""
        request = context.get('request')
        
        # Log error
        logger.error(
            f"Unhandled exception: {exc}",
            exc_info=True,
            extra={'request': request}
        )
        
        error_response = {
            'success': False,
            'error': {
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'An unexpected error occurred',
                'type': exc.__class__.__name__,
                'request_id': getattr(request, 'request_id', str(uuid.uuid4())),
                'timestamp': timezone.now().isoformat(),
            }
        }
        
        # Include details in development
        if settings.DEBUG:
            error_response['error']['details'] = str(exc)
        
        return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# settings.py
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'myapp.exceptions.APIExceptionHandler.handle',
}
```

### Best Practices

1. **Use appropriate status codes:** Match HTTP status codes to error types
2. **Provide clear messages:** Help users understand what went wrong
3. **Include request IDs:** Help track errors in logs
4. **Standardize error format:** Consistent structure across all endpoints
5. **Log all errors:** Track exceptions for debugging
6. **Don't expose internals:** Hide sensitive information in production
7. **Handle validation errors separately:** Provide detailed field-level errors
8. **Use custom exceptions:** Domain-specific errors improve clarity

