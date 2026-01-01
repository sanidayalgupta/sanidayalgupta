# Async Views & Background Jobs

## ⚡ Async Views

### What are Async Views?

**Definition:** Async views handle requests asynchronously, allowing better performance for I/O-bound operations.

**Real-life example:**
Like a restaurant with multiple waiters - while one waiter waits for the kitchen (I/O), others can serve other customers.

### Async Views

**Basic Async View:**
```python
from django.http import JsonResponse
import asyncio

async def async_view(request):
    """Simple async view"""
    await asyncio.sleep(1)  # Simulate async operation
    return JsonResponse({'message': 'Hello from async view'})
```

**DRF Async View:**
```python
from rest_framework.views import APIView
from rest_framework.response import Response
import asyncio

class AsyncAPIView(APIView):
    async def get(self, request):
        """Async GET endpoint"""
        # Perform async operations
        data = await self.fetch_data_async()
        return Response(data)
    
    async def fetch_data_async(self):
        """Async data fetching"""
        await asyncio.sleep(1)  # Simulate async I/O
        return {'data': 'async result'}
```

### Django Async Support

**Requirements:**
- Django 3.1+ for async views
- ASGI server (Daphne, Uvicorn)
- Python 3.7+ with async/await

**Setup:**
```python
# asgi.py
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
application = get_asgi_application()

# Run with ASGI server
# uvicorn myproject.asgi:application --reload
```

**Async ViewSet:**
```python
from rest_framework import viewsets
from rest_framework.decorators import action

class StudentAsyncViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    async def list(self, request, *args, **kwargs):
        """Async list view"""
        queryset = await sync_to_async(list)(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    async def async_action(self, request):
        """Async custom action"""
        data = await self.fetch_external_data()
        return Response(data)
```

**Using sync_to_async:**
```python
from asgiref.sync import sync_to_async

class AsyncView(APIView):
    async def get(self, request):
        # Convert sync ORM calls to async
        students = await sync_to_async(list)(Student.objects.all())
        
        # Or use async database operations
        student = await Student.objects.aget(id=1)
        
        return Response({'students': students})
```

### Celery Integration

**Definition:** Celery executes tasks asynchronously in the background using distributed task queues.

**Real-life example:**
Like a task queue - you submit tasks (like sending emails), and workers process them in the background.

**Setup:**
```bash
pip install celery redis
```

```python
# celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# settings.py
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
```

**Basic Task:**
```python
# tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_welcome_email(user_id):
    """Background task to send email"""
    from django.contrib.auth.models import User
    user = User.objects.get(id=user_id)
    send_mail(
        'Welcome!',
        'Welcome to our platform',
        'from@example.com',
        [user.email],
        fail_silently=False,
    )

# In view
class UserViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # Send email in background
        send_welcome_email.delay(response.data['id'])
        return response
```

### Background Jobs

**Definition:** Background jobs perform long-running tasks without blocking the API response.

**Example:**
```python
@shared_task
def process_large_file(file_path):
    """Process large file in background"""
    # Long-running operation
    with open(file_path) as f:
        # Process file...
        pass
    return {'status': 'processed'}

class FileUploadView(APIView):
    def post(self, request):
        file = request.FILES['file']
        # Save file
        file_path = default_storage.save(file.name, file)
        
        # Process in background
        task = process_large_file.delay(file_path)
        
        return Response({
            'task_id': task.id,
            'status': 'processing'
        }, status=status.HTTP_202_ACCEPTED)
```

**Task Status:**
```python
@shared_task(bind=True)
def process_task(self, data):
    """Task with progress tracking"""
    total = len(data)
    for i, item in enumerate(data):
        # Process item
        process_item(item)
        
        # Update progress
        self.update_state(
            state='PROGRESS',
            meta={'current': i + 1, 'total': total}
        )
    return {'status': 'completed'}

class TaskStatusView(APIView):
    def get(self, request, task_id):
        task = process_task.AsyncResult(task_id)
        
        if task.state == 'PENDING':
            response = {'state': task.state, 'status': 'Waiting...'}
        elif task.state == 'PROGRESS':
            response = {
                'state': task.state,
                'current': task.info.get('current', 0),
                'total': task.info.get('total', 1),
            }
        elif task.state == 'SUCCESS':
            response = {
                'state': task.state,
                'result': task.result,
            }
        else:
            response = {
                'state': task.state,
                'error': str(task.info),
            }
        
        return Response(response)
```

### Task Retries & Idempotency

**Definition:** Task retries automatically retry failed tasks, while idempotency ensures safe retries.

**Retry Configuration:**
```python
@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def process_payment(self, order_id):
    """Task with automatic retries"""
    try:
        # Process payment
        result = payment_gateway.charge(order_id)
        return result
    except PaymentGatewayException as exc:
        # Retry on failure
        raise self.retry(exc=exc, countdown=60)

# Exponential backoff
@shared_task(bind=True, max_retries=5)
def fetch_external_data(self, url):
    """Task with exponential backoff"""
    try:
        response = requests.get(url)
        return response.json()
    except requests.RequestException as exc:
        # Exponential backoff: 2^retry seconds
        raise self.retry(
            exc=exc,
            countdown=2 ** self.request.retries
        )
```

**Idempotency:**
```python
from django.core.cache import cache

@shared_task(bind=True)
def idempotent_task(self, task_key, data):
    """Idempotent task - safe to retry"""
    # Check if already processed
    result_key = f'task_result:{task_key}'
    cached_result = cache.get(result_key)
    
    if cached_result:
        return cached_result  # Already processed
    
    try:
        # Process task
        result = process_data(data)
        
        # Cache result
        cache.set(result_key, result, timeout=3600)
        
        return result
    except Exception as exc:
        # Don't cache on error, allow retry
        raise self.retry(exc=exc)
```

**Complete Example:**
```python
# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.core.cache import cache

@shared_task(bind=True, max_retries=3)
def send_notification_email(self, user_id, subject, message):
    """Send email with retry logic"""
    try:
        user = User.objects.get(id=user_id)
        send_mail(
            subject,
            message,
            'from@example.com',
            [user.email],
        )
        return {'status': 'sent', 'user_id': user_id}
    except User.DoesNotExist:
        # Don't retry - user doesn't exist
        return {'status': 'failed', 'reason': 'user_not_found'}
    except Exception as exc:
        # Retry on other errors
        raise self.retry(exc=exc, countdown=60)

@shared_task
def generate_report(report_id):
    """Generate report in background"""
    report = Report.objects.get(id=report_id)
    
    # Long-running operation
    data = fetch_report_data()
    report.file = generate_pdf(data)
    report.status = 'completed'
    report.save()
    
    return {'report_id': report_id, 'status': 'completed'}

# views.py
class NotificationView(APIView):
    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            # Send email in background
            task = send_notification_email.delay(
                user_id=serializer.validated_data['user_id'],
                subject=serializer.validated_data['subject'],
                message=serializer.validated_data['message'],
            )
            return Response(
                {'task_id': task.id, 'status': 'processing'},
                status=status.HTTP_202_ACCEPTED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReportViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['post'])
    def generate(self, request, pk=None):
        """Generate report in background"""
        report = self.get_object()
        report.status = 'processing'
        report.save()
        
        task = generate_report.delay(report.id)
        report.task_id = task.id
        report.save()
        
        return Response(
            {'task_id': task.id, 'status': 'processing'},
            status=status.HTTP_202_ACCEPTED
        )
```

### Best Practices

1. **Use async for I/O-bound operations:** Database queries, API calls
2. **Use Celery for long-running tasks:** Email sending, file processing
3. **Implement retry logic:** Handle transient failures
4. **Make tasks idempotent:** Safe to retry
5. **Track task status:** Allow clients to check progress
6. **Set appropriate timeouts:** Prevent hanging tasks
7. **Monitor task queues:** Track task execution
8. **Use task priorities:** Important tasks first

