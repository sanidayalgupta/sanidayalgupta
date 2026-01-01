# Parsers & Renderers

## 📥 Parsers & 📤 Renderers

### What are Parsers?

**Definition:** Parsers convert incoming request data (JSON, form data, etc.) into Python objects that your views can use.

**Real-life example:**
Like a translator that converts different languages (JSON, XML, form data) into a language your code understands (Python).

### JSONParser

**Definition:** JSONParser parses JSON request bodies into Python dictionaries.

**Example:**
```python
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

class MyView(APIView):
    parser_classes = [JSONParser]
    
    def post(self, request):
        # request.data is already parsed JSON
        name = request.data.get('name')
        return Response({'received': name})

# Client sends:
# Content-Type: application/json
# Body: {"name": "John"}
```

### FormParser

**Definition:** FormParser parses HTML form data (application/x-www-form-urlencoded).

**Example:**
```python
from rest_framework.parsers import FormParser
from rest_framework.views import APIView

class MyView(APIView):
    parser_classes = [FormParser]
    
    def post(self, request):
        # request.data contains form data
        name = request.data.get('name')
        return Response({'received': name})

# Client sends:
# Content-Type: application/x-www-form-urlencoded
# Body: name=John&age=25
```

### MultiPartParser

**Definition:** MultiPartParser parses multipart form data (used for file uploads).

**Example:**
```python
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        file = request.FILES.get('file')
        name = request.data.get('name')
        # Process file upload...
        return Response({'uploaded': file.name})

# Client sends:
# Content-Type: multipart/form-data
# Body: (multipart form with file and fields)
```

### Custom Parser

**Definition:** Custom parsers allow you to parse custom data formats.

**Example:**
```python
from rest_framework.parsers import BaseParser
from rest_framework.exceptions import ParseError
import xml.etree.ElementTree as ET

class XMLParser(BaseParser):
    """Custom XML parser"""
    media_type = 'application/xml'
    
    def parse(self, stream, media_type=None, parser_context=None):
        """Parse XML request body"""
        try:
            tree = ET.parse(stream)
            root = tree.getroot()
            # Convert XML to dictionary
            return self.xml_to_dict(root)
        except ET.ParseError as e:
            raise ParseError(f'XML parse error: {str(e)}')
    
    def xml_to_dict(self, root):
        """Convert XML element to dictionary"""
        result = {}
        for child in root:
            result[child.tag] = child.text
        return result

# Usage
class MyView(APIView):
    parser_classes = [XMLParser]
    
    def post(self, request):
        # request.data contains parsed XML
        return Response({'received': request.data})
```

### Default Parsers

**Configuration:**
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
}
```

**Content Negotiation:**
DRF automatically selects the parser based on the `Content-Type` header:
- `application/json` → JSONParser
- `application/x-www-form-urlencoded` → FormParser
- `multipart/form-data` → MultiPartParser

---

### What are Renderers?

**Definition:** Renderers convert Python objects into the response format (JSON, XML, HTML, etc.).

**Real-life example:**
Like formatting data for different output formats - the same data can be JSON, XML, or HTML.

### JSONRenderer

**Definition:** JSONRenderer converts Python objects to JSON responses.

**Example:**
```python
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

class MyView(APIView):
    renderer_classes = [JSONRenderer]
    
    def get(self, request):
        data = {'name': 'John', 'age': 25}
        return Response(data)

# Response:
# Content-Type: application/json
# Body: {"name": "John", "age": 25}
```

### BrowsableAPIRenderer

**Definition:** BrowsableAPIRenderer provides an HTML interface for exploring and testing APIs.

**Example:**
```python
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.views import APIView

class MyView(APIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    
    def get(self, request):
        data = {'name': 'John', 'age': 25}
        return Response(data)

# Visit /api/endpoint/ in browser to see HTML interface
# Accept: application/json → JSON response
# Accept: text/html → HTML browsable interface
```

**Configuration:**
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # Enable browsable API
    ],
}
```

### Custom Renderer

**Definition:** Custom renderers allow you to create responses in custom formats.

**Example:**
```python
from rest_framework.renderers import BaseRenderer
from rest_framework import renderers
import json

class XMLRenderer(BaseRenderer):
    """Custom XML renderer"""
    media_type = 'application/xml'
    format = 'xml'
    
    def render(self, data, media_type=None, renderer_context=None):
        """Convert Python dict to XML"""
        if data is None:
            return ''
        
        xml = '<response>'
        xml += self.dict_to_xml(data)
        xml += '</response>'
        return xml.encode('utf-8')
    
    def dict_to_xml(self, data, parent=''):
        """Convert dictionary to XML"""
        xml = ''
        if isinstance(data, dict):
            for key, value in data.items():
                xml += f'<{key}>'
                xml += self.dict_to_xml(value, key)
                xml += f'</{key}>'
        elif isinstance(data, list):
            for item in data:
                xml += '<item>'
                xml += self.dict_to_xml(item)
                xml += '</item>'
        else:
            xml += str(data)
        return xml

# Usage
class MyView(APIView):
    renderer_classes = [JSONRenderer, XMLRenderer]
    
    def get(self, request):
        data = {'name': 'John', 'age': 25}
        return Response(data)

# Client requests:
# Accept: application/xml → XML response
# Accept: application/json → JSON response
```

**CSV Renderer Example:**
```python
import csv
from io import StringIO
from rest_framework.renderers import BaseRenderer

class CSVRenderer(BaseRenderer):
    media_type = 'text/csv'
    format = 'csv'
    
    def render(self, data, media_type=None, renderer_context=None):
        """Convert list of dicts to CSV"""
        if not data:
            return ''
        
        output = StringIO()
        
        if isinstance(data, list) and data:
            # Get field names from first item
            fieldnames = data[0].keys()
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        elif isinstance(data, dict):
            writer = csv.DictWriter(output, fieldnames=data.keys())
            writer.writeheader()
            writer.writerow(data)
        
        return output.getvalue()

# Usage
class StudentExportView(APIView):
    renderer_classes = [CSVRenderer, JSONRenderer]
    
    def get(self, request):
        students = Student.objects.all()
        data = StudentSerializer(students, many=True).data
        return Response(data)

# GET /api/students/export/
# Accept: text/csv → CSV download
# Accept: application/json → JSON response
```

### Custom Response Class

**Definition:** Custom response classes allow you to customize the response structure.

**Example:**
```python
from rest_framework.response import Response

class StandardResponse(Response):
    """Standard API response format"""
    
    def __init__(self, data=None, status=None, message=None, **kwargs):
        response_data = {
            'success': status is None or 200 <= status < 300,
            'message': message,
            'data': data
        }
        super().__init__(response_data, status, **kwargs)

# Usage
class MyView(APIView):
    def get(self, request):
        data = {'students': [...]}
        return StandardResponse(
            data=data,
            message='Students retrieved successfully'
        )

# Response:
# {
#   "success": true,
#   "message": "Students retrieved successfully",
#   "data": {"students": [...]}
# }
```

**Paginated Response Wrapper:**
```python
class PaginatedResponse(Response):
    """Response with pagination metadata"""
    
    def __init__(self, data, paginator, request, **kwargs):
        response_data = {
            'success': True,
            'data': data,
            'pagination': {
                'count': paginator.count,
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'page_size': paginator.page_size,
                'current_page': paginator.page.number,
                'total_pages': paginator.num_pages
            }
        }
        super().__init__(response_data, **kwargs)

# Usage
class StudentViewSet(viewsets.ModelViewSet):
    pagination_class = StandardPagination
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return PaginatedResponse(
                serializer.data,
                self.paginator,
                request
            )
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
```

### Default Renderers

**Configuration:**
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}
```

**Content Negotiation:**
DRF selects renderer based on `Accept` header:
- `Accept: application/json` → JSONRenderer
- `Accept: text/html` → BrowsableAPIRenderer
- `Accept: application/xml` → XMLRenderer (if configured)

### Best Practices

1. **Use appropriate parsers:** Match parser to Content-Type
2. **Support multiple formats:** Allow JSON, XML, etc.
3. **Keep BrowsableAPIRenderer in development:** Helpful for testing
4. **Remove BrowsableAPIRenderer in production:** Security and performance
5. **Create custom renderers for exports:** CSV, Excel, PDF formats
6. **Standardize response format:** Use custom response classes
7. **Handle content negotiation:** Let clients choose format
8. **Validate parsed data:** Always validate after parsing

