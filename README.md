# Django REST Framework - Complete Tutorial Project

A comprehensive Django REST Framework tutorial project covering concepts from **basics to advanced pro level**.

## 📚 Quick Navigation

- **[ENDPOINTS_GUIDE.md](ENDPOINTS_GUIDE.md)** - Complete endpoint usage with payloads ⭐
- **[CONCEPTS_EXPLAINED.md](CONCEPTS_EXPLAINED.md)** - All concepts explained (definition + examples) ⭐
- **[INDEX.md](INDEX.md)** - Complete navigation guide
- **[Swagger UI](http://127.0.0.1:8000/api/docs/)** - Interactive API documentation

## 📚 Project Structure

This project is organized into 4 progressive levels, each building upon the previous:

### 🟢 Level 1: Basics (`basics/`)
**Concepts Covered:**
- ✅ Serializers (ModelSerializer, Serializer)
- ✅ Function-based API Views (`@api_view`)
- ✅ Class-based API Views (`APIView`)
- ✅ Generic Views (`ListCreateAPIView`, `RetrieveUpdateDestroyAPIView`)
- ✅ Basic CRUD operations
- ✅ Field validation

**Endpoints:**
- `GET/POST /api/basics/students-fbv/` - Function-based view
- `GET/PUT/PATCH/DELETE /api/basics/students-fbv/<id>/`
- `GET/POST /api/basics/students-cbv/` - Class-based view
- `GET/PUT/PATCH/DELETE /api/basics/students-cbv/<id>/`
- `GET/POST /api/basics/courses/` - Generic views
- `GET/PUT/PATCH/DELETE /api/basics/courses/<id>/`

---

### 🟡 Level 2: Intermediate (`intermediate/`)
**Concepts Covered:**
- ✅ ViewSets (`ModelViewSet`, `ReadOnlyModelViewSet`)
- ✅ Routers (automatic URL generation)
- ✅ Model relationships (ForeignKey, ManyToMany)
- ✅ Nested serializers (read operations)
- ✅ Custom actions with `@action` decorator
- ✅ Query optimization (select_related, prefetch_related)

**Endpoints:**
- `GET/POST /api/intermediate/categories/` - Full CRUD with ViewSet
- `GET/POST /api/intermediate/authors/`
- `GET/POST /api/intermediate/books/`
- `GET /api/intermediate/books/<id>/reviews/` - Custom action
- `POST /api/intermediate/books/<id>/add_review/` - Custom action
- `GET /api/intermediate/books/available/` - Collection-level custom action

---

### 🔴 Level 3: Advanced (`advanced/`)
**Concepts Covered:**
- ✅ Token Authentication
- ✅ Custom Permissions (`IsOwnerOrReadOnly`, `IsAuthorOrAdmin`)
- ✅ Advanced Filtering (django-filter with custom filtersets)
- ✅ Custom Pagination classes
- ✅ Search and Ordering
- ✅ Different serializers for different actions
- ✅ File uploads (ImageField)

**Endpoints:**
- `GET/POST /api/advanced/blogposts/` - With authentication & permissions
- `POST /api/advanced/blogposts/<id>/like/` - Custom action
- `GET /api/advanced/blogposts/published/` - Filtered list
- `GET /api/advanced/blogposts/my_posts/` - User's own posts
- `GET/POST /api/advanced/comments/`
- `POST /api/advanced/comments/<id>/approve/` - Custom permission

**Authentication:**
- Token-based: Include header `Authorization: Token <your-token>`
- Session-based: Login via `/api-auth/login/`

---

### 🟣 Level 4: Expert (`expert/`)
**Concepts Covered:**
- ✅ Deep nested serializers with write operations
- ✅ Writable nested serializers (creating related objects)
- ✅ Custom Throttling classes
- ✅ Transaction management (`@transaction.atomic`)
- ✅ Bulk operations
- ✅ Complex queryset optimization
- ✅ Aggregations (Count, Sum, Avg)
- ✅ Custom exception handling patterns

**Endpoints:**
- `GET/POST /api/expert/companies/`
- `GET /api/expert/companies/<id>/statistics/` - Aggregated data
- `GET/POST /api/expert/departments/` - With nested employees
- `POST /api/expert/employees/bulk_create/` - Bulk operation
- `GET/POST /api/expert/projects/` - With nested tasks
- `GET /api/expert/projects/<id>/progress/` - Custom statistics

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone/Navigate to the project:**
```bash
cd drf_tutorial
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create a superuser:**
```bash
python manage.py createsuperuser
```

6. **Run the development server:**
```bash
python manage.py runserver
```

7. **Access the API:**
- Browsable API: http://127.0.0.1:8000/api/basics/
- Admin Panel: http://127.0.0.1:8000/admin/

---

## 🔑 Authentication Setup

### Create API Token for a User:

1. **Via Admin Panel:**
   - Go to `/admin/`
   - Navigate to "Tokens" under "AUTHENTICATION AND AUTHORIZATION"
   - Create a token for your user

2. **Via Django Shell:**
```python
python manage.py shell
>>> from rest_framework.authtoken.models import Token
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='your_username')
>>> token = Token.objects.create(user=user)
>>> print(token.key)
```

3. **Use the token in API requests:**
```bash
curl -H "Authorization: Token <your-token>" http://127.0.0.1:8000/api/advanced/blogposts/
```

---

## 📖 Learning Path

### Step 1: Basics
Start with the `basics` app to understand:
- How serializers convert data
- Different ways to create API views
- Basic CRUD operations

**Try:**
```bash
# List all students
GET http://127.0.0.1:8000/api/basics/students-fbv/

# Create a student
POST http://127.0.0.1:8000/api/basics/students-fbv/
{
    "name": "John Doe",
    "email": "john@example.com",
    "age": 20,
    "grade": "A"
}
```

### Step 2: Intermediate
Move to `intermediate` to learn:
- ViewSets and Routers (less code, more power)
- Handling relationships
- Custom actions

**Try:**
```bash
# List books with automatic filtering
GET http://127.0.0.1:8000/api/intermediate/books/?is_available=true&search=django

# Get reviews for a book
GET http://127.0.0.1:8000/api/intermediate/books/1/reviews/
```

### Step 3: Advanced
Explore `advanced` for:
- Authentication and permissions
- Advanced filtering
- Custom pagination

**Try:**
```bash
# Create a blog post (requires authentication)
POST http://127.0.0.1:8000/api/advanced/blogposts/
Headers: Authorization: Token <your-token>
{
    "title": "My First Post",
    "slug": "my-first-post",
    "content": "This is my first blog post...",
    "status": "draft",
    "tags": "django, python, tutorial"
}
```

### Step 4: Expert
Master `expert` level:
- Nested writes
- Bulk operations
- Custom throttling
- Transactions

**Try:**
```bash
# Create a company with nested departments and employees
POST http://127.0.0.1:8000/api/expert/companies/
{
    "name": "Tech Corp",
    "description": "A tech company",
    "founded_year": 2020,
    "headquarters": "San Francisco",
    "website": "https://techcorp.com"
}

# Then create department with employees
POST http://127.0.0.1:8000/api/expert/departments/
{
    "company": 1,
    "name": "Engineering",
    "budget": 1000000,
    "employees": [
        {
            "user": {"username": "dev1", "email": "dev1@techcorp.com"},
            "employee_id": "EMP001",
            "position": "Senior Developer",
            "salary": 120000,
            "hire_date": "2020-01-15"
        }
    ]
}
```

---

## 🎯 Key Concepts Explained

### Serializers
**Purpose:** Convert complex data types (Django models) to/from JSON

**Types:**
- `ModelSerializer` - Auto-generates from model (most common)
- `Serializer` - Manual control (for complex cases)

### ViewSets vs Views
- **Views:** More explicit, one view per action
- **ViewSets:** Combine related views, less code, use with Routers

### Authentication vs Permissions
- **Authentication:** "Who are you?" (Token, Session, etc.)
- **Permissions:** "What can you do?" (IsAuthenticated, IsOwner, etc.)

### Filtering
- **DjangoFilterBackend:** Filter by exact field values
- **SearchFilter:** Search across multiple fields
- **OrderingFilter:** Sort results

### Pagination
- **PageNumberPagination:** `?page=2`
- **LimitOffsetPagination:** `?limit=10&offset=20`
- **CursorPagination:** For large datasets (most efficient)

### Throttling
Rate limiting to prevent abuse:
- Per user
- Per IP
- Per action
- Custom scopes

---

## 📝 Code Examples

### Custom Permission
```python
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
```

### Custom Action
```python
@action(detail=True, methods=['post'])
def like(self, request, pk=None):
    post = self.get_object()
    post.likes_count += 1
    post.save()
    return Response({'likes_count': post.likes_count})
```

### Writable Nested Serializer
```python
def create(self, validated_data):
    tasks_data = validated_data.pop('tasks', [])
    with transaction.atomic():
        project = Project.objects.create(**validated_data)
        for task_data in tasks_data:
            Task.objects.create(project=project, **task_data)
    return project
```

---

## 🧪 Testing the API

### Using cURL:
```bash
# GET request
curl http://127.0.0.1:8000/api/basics/students-fbv/

# POST request
curl -X POST http://127.0.0.1:8000/api/basics/students-fbv/ \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com","age":20,"grade":"A"}'

# With authentication
curl -H "Authorization: Token <your-token>" \
  http://127.0.0.1:8000/api/advanced/blogposts/
```

### Using Python requests:
```python
import requests

# Get token (after creating one)
token = "your-token-here"
headers = {"Authorization": f"Token {token}"}

# Make authenticated request
response = requests.get(
    "http://127.0.0.1:8000/api/advanced/blogposts/",
    headers=headers
)
print(response.json())
```

### Using Browsable API:
Visit any endpoint in your browser - DRF provides an interactive HTML interface!

---

## 📚 Additional Resources

- [DRF Official Documentation](https://www.django-rest-framework.org/)
- [Django Documentation](https://docs.djangoproject.com/)
- [DRF Tutorial](https://www.django-rest-framework.org/tutorial/quickstart/)

---

## 🎓 Project Features

✅ **4 Progressive Levels** - From basics to expert  
✅ **Comprehensive Examples** - Real-world patterns  
✅ **Well-Documented Code** - Inline comments explaining concepts  
✅ **Best Practices** - Query optimization, transactions, security  
✅ **Production-Ready Patterns** - Authentication, permissions, throttling  

---

## 🤝 Contributing

This is a tutorial project. Feel free to:
- Experiment with the code
- Add your own examples
- Modify and extend the concepts

---

## 📄 License

This project is for educational purposes.

---

## 🎉 Happy Learning!

Start with the basics and work your way up. Each level introduces new concepts that build upon the previous ones. Take your time to understand each concept before moving to the next level.

**Remember:** The best way to learn is by doing. Try modifying the code, breaking things, and fixing them!

