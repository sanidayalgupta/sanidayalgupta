# File Upload APIs

## 📁 File Handling in DRF

### What is File Upload?

**Definition:** File upload allows clients to send files (images, documents, etc.) to the server via API.

**Real-life example:**
Like uploading photos to social media - you send the image file, and the server stores it.

### File Upload APIs

**Basic File Upload:**
```python
from rest_framework import serializers, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 'uploaded_at']
        read_only_fields = ['uploaded_at']

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = [MultiPartParser, FormParser]  # Required for file uploads
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
```

**Model Setup:**
```python
from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
```

**Settings Configuration:**
```python
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your URL patterns
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Image Handling

**Definition:** Image handling allows uploading, validating, and processing images.

**Image Upload:**
```python
from rest_framework import serializers
from django.core.files.images import get_image_dimensions

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'title', 'image', 'thumbnail', 'uploaded_at']
        read_only_fields = ['thumbnail', 'uploaded_at']
    
    def validate_image(self, value):
        """Validate image file"""
        # Check file size (e.g., max 5MB)
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Image size cannot exceed 5MB")
        
        # Check file type
        valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
        ext = value.name.split('.')[-1].lower()
        if ext not in valid_extensions:
            raise serializers.ValidationError(
                f"Invalid image format. Allowed: {', '.join(valid_extensions)}"
            )
        
        # Check dimensions
        width, height = get_image_dimensions(value)
        if width < 100 or height < 100:
            raise serializers.ValidationError("Image must be at least 100x100 pixels")
        
        return value

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = [MultiPartParser, FormParser]
```

**Creating Thumbnails:**
```python
from PIL import Image
from django.core.files.base import ContentFile
import io

class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    
    def create_thumbnail(self):
        """Create thumbnail from image"""
        if not self.image:
            return
        
        # Open image
        img = Image.open(self.image)
        img.thumbnail((200, 200), Image.ANTIALIAS)
        
        # Save thumbnail
        thumb_io = io.BytesIO()
        img.save(thumb_io, format='JPEG')
        
        # Create thumbnail file
        thumbnail_name = f"thumb_{self.image.name}"
        self.thumbnail.save(
            thumbnail_name,
            ContentFile(thumb_io.getvalue()),
            save=False
        )
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.thumbnail:
            self.create_thumbnail()
            super().save(*args, **kwargs)
```

### File Validation

**Definition:** File validation ensures uploaded files meet requirements (size, type, content).

**Comprehensive Validation:**
```python
from rest_framework import serializers
import magic

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    description = serializers.CharField(max_length=500, required=False)
    
    def validate_file(self, value):
        """Validate file"""
        # Check file size (max 10MB)
        max_size = 10 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError(
                f"File size cannot exceed {max_size / (1024*1024)}MB"
            )
        
        # Check file type using python-magic
        file_type = magic.from_buffer(value.read(1024), mime=True)
        value.seek(0)  # Reset file pointer
        
        allowed_types = [
            'application/pdf',
            'image/jpeg',
            'image/png',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ]
        
        if file_type not in allowed_types:
            raise serializers.ValidationError(
                f"File type {file_type} not allowed. Allowed types: {', '.join(allowed_types)}"
            )
        
        # Check file extension
        ext = value.name.split('.')[-1].lower()
        allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx']
        if ext not in allowed_extensions:
            raise serializers.ValidationError(
                f"File extension .{ext} not allowed"
            )
        
        return value

class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            # Process file
            document = Document.objects.create(
                file=file,
                description=serializer.validated_data.get('description', '')
            )
            return Response(
                {'id': document.id, 'url': document.file.url},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

**Content-based Validation:**
```python
import zipfile

def validate_zip_file(value):
    """Validate ZIP file content"""
    try:
        with zipfile.ZipFile(value, 'r') as zip_file:
            # Check for dangerous files
            dangerous_extensions = ['.exe', '.bat', '.sh', '.php']
            for name in zip_file.namelist():
                if any(name.endswith(ext) for ext in dangerous_extensions):
                    raise serializers.ValidationError(
                        f"Dangerous file found in archive: {name}"
                    )
    except zipfile.BadZipFile:
        raise serializers.ValidationError("Invalid ZIP file")
    
    return value
```

### Streaming Downloads

**Definition:** Streaming downloads send large files in chunks instead of loading everything into memory.

**Streaming Response:**
```python
from django.http import StreamingHttpResponse
from rest_framework.views import APIView
import os

class FileDownloadView(APIView):
    def get(self, request, file_id):
        document = Document.objects.get(id=file_id)
        file_path = document.file.path
        
        def file_iterator(file_path, chunk_size=8192):
            """Generate file chunks"""
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
        
        response = StreamingHttpResponse(
            file_iterator(file_path),
            content_type='application/octet-stream'
        )
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        response['Content-Length'] = os.path.getsize(file_path)
        return response
```

**Chunked Download:**
```python
from rest_framework.response import Response
from django.http import Http404

class ChunkedDownloadView(APIView):
    def get(self, request, file_id):
        document = Document.objects.get(id=file_id)
        file_path = document.file.path
        
        # Get range header for partial content
        range_header = request.META.get('HTTP_RANGE', '').strip()
        
        if not range_header:
            # Return full file
            return self.serve_file(file_path)
        
        # Parse range header
        range_match = re.match(r'bytes=(\d+)-(\d*)', range_header)
        if not range_match:
            return Response(
                {'error': 'Invalid range header'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        file_size = os.path.getsize(file_path)
        start = int(range_match.group(1))
        end = int(range_match.group(2)) if range_match.group(2) else file_size - 1
        
        # Validate range
        if start >= file_size or end >= file_size:
            return Response(
                {'error': 'Range not satisfiable'},
                status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE
            )
        
        # Stream chunk
        def file_chunk_iterator(file_path, start, end):
            with open(file_path, 'rb') as f:
                f.seek(start)
                remaining = end - start + 1
                while remaining:
                    chunk_size = min(8192, remaining)
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    remaining -= len(chunk)
                    yield chunk
        
        response = StreamingHttpResponse(
            file_chunk_iterator(file_path, start, end),
            status=status.HTTP_206_PARTIAL_CONTENT
        )
        response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
        response['Content-Length'] = str(end - start + 1)
        response['Content-Type'] = 'application/octet-stream'
        return response
```

### Large File Optimization

**Definition:** Optimizing large file uploads by chunking, resuming, or using async processing.

**Chunked Upload:**
```python
from rest_framework.views import APIView
from django.core.cache import cache
import hashlib

class ChunkedUploadView(APIView):
    def post(self, request):
        """Handle chunked file upload"""
        chunk_number = int(request.data.get('chunk_number', 0))
        total_chunks = int(request.data.get('total_chunks', 1))
        file_id = request.data.get('file_id')
        chunk_data = request.FILES.get('chunk')
        
        # Create file ID if first chunk
        if chunk_number == 0:
            file_id = hashlib.md5(
                f"{request.user.id}_{time.time()}".encode()
            ).hexdigest()
        
        # Store chunk
        cache_key = f"chunk_{file_id}_{chunk_number}"
        cache.set(cache_key, chunk_data.read(), timeout=3600)
        
        # Check if all chunks received
        if chunk_number == total_chunks - 1:
            # Combine chunks
            file_content = b''
            for i in range(total_chunks):
                chunk_key = f"chunk_{file_id}_{i}"
                chunk = cache.get(chunk_key)
                if chunk:
                    file_content += chunk
                    cache.delete(chunk_key)
            
            # Save file
            document = Document.objects.create(
                file=ContentFile(file_content, name=request.data.get('filename')),
                uploaded_by=request.user
            )
            return Response(
                {'id': document.id, 'file_id': file_id},
                status=status.HTTP_201_CREATED
            )
        
        return Response({'file_id': file_id, 'chunk_received': chunk_number + 1})
```

**Async File Processing:**
```python
from celery import shared_task
from django.core.files.base import ContentFile

@shared_task
def process_large_file(document_id):
    """Process large file asynchronously"""
    document = Document.objects.get(id=document_id)
    
    # Process file (e.g., generate thumbnails, extract text, etc.)
    # This runs in background without blocking the API response
    
    # Update document status
    document.processing_status = 'completed'
    document.save()

class LargeFileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            document = serializer.save(uploaded_by=request.user)
            document.processing_status = 'processing'
            document.save()
            
            # Process asynchronously
            process_large_file.delay(document.id)
            
            return Response(
                {'id': document.id, 'status': 'processing'},
                status=status.HTTP_202_ACCEPTED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

**File Storage Optimization:**
```python
# settings.py - Use cloud storage for large files
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = 'your-access-key'
AWS_SECRET_ACCESS_KEY = 'your-secret-key'
AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
AWS_S3_REGION_NAME = 'us-east-1'
```

### Complete Example

**Real Project Example:**
```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.files.storage import default_storage
from PIL import Image
import os

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download file"""
        document = self.get_object()
        
        def file_iterator(file_path, chunk_size=8192):
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
        
        response = StreamingHttpResponse(
            file_iterator(document.file.path),
            content_type='application/octet-stream'
        )
        response['Content-Disposition'] = f'attachment; filename="{document.file.name}"'
        return response
    
    @action(detail=True, methods=['delete'])
    def delete_file(self, request, pk=None):
        """Delete file and database record"""
        document = self.get_object()
        
        # Delete file from storage
        if document.file:
            document.file.delete()
        
        # Delete database record
        document.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
```

### Best Practices

1. **Validate file types and sizes:** Prevent malicious uploads
2. **Use streaming for large files:** Avoid memory issues
3. **Store files securely:** Use proper file permissions
4. **Generate unique filenames:** Prevent overwrites
5. **Clean up temporary files:** Remove unused chunks/files
6. **Use cloud storage for production:** Scalable and reliable
7. **Process large files asynchronously:** Don't block API responses
8. **Provide upload progress:** Better user experience

