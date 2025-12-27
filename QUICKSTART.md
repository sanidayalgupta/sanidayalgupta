# Quick Start Guide

## 🚀 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Admin User
```bash
python manage.py createsuperuser
```

### 4. Create API Token (Optional but Recommended)
```bash
python manage.py shell
```
```python
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
user = User.objects.first()  # or get by username
token, created = Token.objects.get_or_create(user=user)
print(f"Your token: {token.key}")
```

### 5. Run Server
```bash
python manage.py runserver
```

### 6. Test the API

**Open in browser:**
- http://127.0.0.1:8000/api/basics/students-fbv/
- http://127.0.0.1:8000/api/intermediate/books/
- http://127.0.0.1:8000/api/advanced/blogposts/
- http://127.0.0.1:8000/api/expert/companies/

**Or use cURL:**
```bash
# Basic GET
curl http://127.0.0.1:8000/api/basics/students-fbv/

# Create a student
curl -X POST http://127.0.0.1:8000/api/basics/students-fbv/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com","age":22,"grade":"A"}'
```

## 📍 API Endpoints Overview

### Basics (No Auth Required)
- `GET/POST /api/basics/students-fbv/`
- `GET/PUT/PATCH/DELETE /api/basics/students-fbv/<id>/`
- `GET/POST /api/basics/courses/`

### Intermediate (No Auth Required)
- `GET/POST /api/intermediate/books/`
- `GET /api/intermediate/books/<id>/reviews/`
- `GET/POST /api/intermediate/authors/`

### Advanced (Auth Required)
- `GET/POST /api/advanced/blogposts/` (Token auth)
- `POST /api/advanced/blogposts/<id>/like/`
- `GET/POST /api/advanced/comments/`

### Expert (Auth Required)
- `GET/POST /api/expert/companies/`
- `POST /api/expert/employees/bulk_create/`
- `GET /api/expert/projects/<id>/progress/`

## 🔑 Using Authentication

For advanced/expert endpoints, include your token:

```bash
curl -H "Authorization: Token <your-token>" \
  http://127.0.0.1:8000/api/advanced/blogposts/
```

Or in Python:
```python
import requests
headers = {"Authorization": "Token <your-token>"}
response = requests.get("http://127.0.0.1:8000/api/advanced/blogposts/", headers=headers)
```

## 📖 Learning Order

1. **Start with Basics** - Understand serializers and views
2. **Move to Intermediate** - Learn ViewSets and relationships
3. **Explore Advanced** - Master authentication and permissions
4. **Master Expert** - Handle complex nested operations

Happy coding! 🎉

