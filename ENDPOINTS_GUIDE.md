# Complete Endpoints Guide with Payloads

## 📚 Table of Contents
1. [Basics Endpoints](#basics-endpoints)
2. [Intermediate Endpoints](#intermediate-endpoints)
3. [Advanced Endpoints](#advanced-endpoints)
4. [Expert Endpoints](#expert-endpoints)
5. [Authentication](#authentication)

---

## 🔵 Basics Endpoints

### What are Basics Endpoints?
**Basics endpoints** demonstrate fundamental DRF concepts: serializers, function-based views, class-based views, and generic views. These are the building blocks of any REST API.

### 1. List Students (Function-Based View)

**Endpoint:** `GET /api/basics/students-fbv/`

**What it does:** Retrieves a list of all students using a function-based view.

**Request:**
```bash
GET http://127.0.0.1:8000/api/basics/students-fbv/
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "age": 20,
    "grade": "A",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

**cURL:**
```bash
curl http://127.0.0.1:8000/api/basics/students-fbv/
```

---

### 2. Create Student (Function-Based View)

**Endpoint:** `POST /api/basics/students-fbv/`

**What it does:** Creates a new student record using a function-based view with validation.

**Request:**
```bash
POST http://127.0.0.1:8000/api/basics/students-fbv/
Content-Type: application/json
```

**Payload:**
```json
{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "age": 22,
  "grade": "B"
}
```

**Response (201 Created):**
```json
{
  "id": 2,
  "name": "Jane Smith",
  "email": "jane@example.com",
  "age": 22,
  "grade": "B",
  "created_at": "2024-01-15T11:00:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

**cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/basics/students-fbv/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "age": 22,
    "grade": "B"
  }'
```

**Python requests:**
```python
import requests

url = "http://127.0.0.1:8000/api/basics/students-fbv/"
data = {
    "name": "Jane Smith",
    "email": "jane@example.com",
    "age": 22,
    "grade": "B"
}
response = requests.post(url, json=data)
print(response.json())
```

---

### 3. Get Student Detail

**Endpoint:** `GET /api/basics/students-fbv/{id}/`

**What it does:** Retrieves a specific student by ID.

**Request:**
```bash
GET http://127.0.0.1:8000/api/basics/students-fbv/1/
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "age": 20,
  "grade": "A",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

---

### 4. Update Student (PUT - Full Update)

**Endpoint:** `PUT /api/basics/students-fbv/{id}/`

**What it does:** Fully updates a student record. All fields must be provided.

**Request:**
```bash
PUT http://127.0.0.1:8000/api/basics/students-fbv/1/
Content-Type: application/json
```

**Payload:**
```json
{
  "name": "John Updated",
  "email": "john.updated@example.com",
  "age": 21,
  "grade": "A+"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "John Updated",
  "email": "john.updated@example.com",
  "age": 21,
  "grade": "A+",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T12:00:00Z"
}
```

**cURL:**
```bash
curl -X PUT http://127.0.0.1:8000/api/basics/students-fbv/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Updated",
    "email": "john.updated@example.com",
    "age": 21,
    "grade": "A+"
  }'
```

---

### 5. Partial Update Student (PATCH)

**Endpoint:** `PATCH /api/basics/students-fbv/{id}/`

**What it does:** Partially updates a student. Only provided fields are updated.

**Request:**
```bash
PATCH http://127.0.0.1:8000/api/basics/students-fbv/1/
Content-Type: application/json
```

**Payload (only update grade):**
```json
{
  "grade": "A+"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "age": 20,
  "grade": "A+",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T12:30:00Z"
}
```

**cURL:**
```bash
curl -X PATCH http://127.0.0.1:8000/api/basics/students-fbv/1/ \
  -H "Content-Type: application/json" \
  -d '{"grade": "A+"}'
```

---

### 6. Delete Student

**Endpoint:** `DELETE /api/basics/students-fbv/{id}/`

**What it does:** Deletes a student record.

**Request:**
```bash
DELETE http://127.0.0.1:8000/api/basics/students-fbv/1/
```

**Response:** `204 No Content` (empty body)

**cURL:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/basics/students-fbv/1/
```

---

### 7. List Courses (Generic View)

**Endpoint:** `GET /api/basics/courses/`

**What it does:** Lists all courses using a generic view (ListCreateAPIView).

**Request:**
```bash
GET http://127.0.0.1:8000/api/basics/courses/
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Introduction to Python",
    "description": "Learn Python fundamentals",
    "instructor": "Dr. Smith",
    "duration_hours": 40,
    "price": "99.99",
    "is_active": true,
    "created_at": "2024-01-10T09:00:00Z"
  }
]
```

---

### 8. Create Course

**Endpoint:** `POST /api/basics/courses/`

**What it does:** Creates a new course.

**Request:**
```bash
POST http://127.0.0.1:8000/api/basics/courses/
Content-Type: application/json
```

**Payload:**
```json
{
  "title": "Advanced Django",
  "description": "Master Django framework",
  "instructor": "Jane Doe",
  "duration_hours": 60,
  "price": "199.99",
  "is_active": true
}
```

**Response (201 Created):**
```json
{
  "id": 2,
  "title": "Advanced Django",
  "description": "Master Django framework",
  "instructor": "Jane Doe",
  "duration_hours": 60,
  "price": "199.99",
  "is_active": true,
  "created_at": "2024-01-15T13:00:00Z"
}
```

---

## 🟡 Intermediate Endpoints

### What are Intermediate Endpoints?
**Intermediate endpoints** use ViewSets and Routers, which automatically generate multiple endpoints from a single class. They also demonstrate model relationships (ForeignKey, ManyToMany).

### 1. List Books

**Endpoint:** `GET /api/intermediate/books/`

**What it does:** Lists all books with pagination. Supports filtering, searching, and ordering.

**Request:**
```bash
GET http://127.0.0.1:8000/api/intermediate/books/
```

**Query Parameters:**
- `page` - Page number (default: 1)
- `page_size` - Items per page
- `is_available` - Filter by availability (true/false)
- `author` - Filter by author ID
- `categories` - Filter by category ID
- `search` - Search in title, description, ISBN
- `ordering` - Order by field (e.g., `-created_at`, `price`)

**Example with filters:**
```bash
GET http://127.0.0.1:8000/api/intermediate/books/?is_available=true&search=django&ordering=-created_at
```

**Response (Paginated):**
```json
{
  "count": 50,
  "next": "http://127.0.0.1:8000/api/intermediate/books/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "The Art of Programming",
      "author_name": "John Smith",
      "categories": ["Technology", "Programming"],
      "price": "29.99",
      "is_available": true,
      "publication_date": "2023-01-15"
    }
  ]
}
```

---

### 2. Create Book

**Endpoint:** `POST /api/intermediate/books/`

**What it does:** Creates a new book with relationships to author and categories.

**Request:**
```bash
POST http://127.0.0.1:8000/api/intermediate/books/
Content-Type: application/json
```

**Payload:**
```json
{
  "title": "Django REST Framework Guide",
  "description": "Complete guide to building APIs with DRF",
  "author": 1,
  "categories": [1, 3],
  "isbn": "9781234567890",
  "publication_date": "2024-01-15",
  "price": "39.99",
  "pages": 400,
  "is_available": true
}
```

**Response (201 Created):**
```json
{
  "id": 51,
  "title": "Django REST Framework Guide",
  "description": "Complete guide to building APIs with DRF",
  "author": 1,
  "categories": [1, 3],
  "isbn": "9781234567890",
  "publication_date": "2024-01-15",
  "price": "39.99",
  "pages": 400,
  "is_available": true,
  "created_at": "2024-01-15T14:00:00Z"
}
```

---

### 3. Get Book Detail

**Endpoint:** `GET /api/intermediate/books/{id}/`

**What it does:** Retrieves detailed book information with nested relationships.

**Request:**
```bash
GET http://127.0.0.1:8000/api/intermediate/books/1/
```

**Response:**
```json
{
  "id": 1,
  "title": "The Art of Programming",
  "description": "A comprehensive guide...",
  "author": {
    "id": 1,
    "user": {
      "id": 1,
      "username": "author1",
      "email": "author1@example.com"
    },
    "bio": "Experienced programmer",
    "books_count": 5
  },
  "categories": [
    {"id": 1, "name": "Technology", "slug": "technology"},
    {"id": 3, "name": "Programming", "slug": "programming"}
  ],
  "isbn": "9781234567890",
  "publication_date": "2023-01-15",
  "price": "29.99",
  "pages": 300,
  "is_available": true,
  "average_rating": 4.5,
  "reviews_count": 10,
  "created_at": "2023-01-10T09:00:00Z"
}
```

---

### 4. Custom Action: Get Book Reviews

**Endpoint:** `GET /api/intermediate/books/{id}/reviews/`

**What it does:** Custom action to get all reviews for a specific book.

**Request:**
```bash
GET http://127.0.0.1:8000/api/intermediate/books/1/reviews/
```

**Response:**
```json
[
  {
    "id": 1,
    "book": 1,
    "book_title": "The Art of Programming",
    "reviewer": 2,
    "reviewer_name": "reader1",
    "rating": 5,
    "comment": "Excellent book!",
    "created_at": "2024-01-12T10:00:00Z"
  }
]
```

---

### 5. Custom Action: Add Review

**Endpoint:** `POST /api/intermediate/books/{id}/add_review/`

**What it does:** Custom action to add a review to a book.

**Request:**
```bash
POST http://127.0.0.1:8000/api/intermediate/books/1/add_review/
Content-Type: application/json
Authorization: Token <your-token>
```

**Payload:**
```json
{
  "rating": 5,
  "comment": "Great book, highly recommended!"
}
```

**Response (201 Created):**
```json
{
  "id": 2,
  "book": 1,
  "book_title": "The Art of Programming",
  "reviewer": 3,
  "reviewer_name": "current_user",
  "rating": 5,
  "comment": "Great book, highly recommended!",
  "created_at": "2024-01-15T15:00:00Z"
}
```

---

### 6. Custom Action: Available Books

**Endpoint:** `GET /api/intermediate/books/available/`

**What it does:** Collection-level custom action to get only available books.

**Request:**
```bash
GET http://127.0.0.1:8000/api/intermediate/books/available/
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "The Art of Programming",
    "author_name": "John Smith",
    "categories": ["Technology"],
    "price": "29.99",
    "is_available": true
  }
]
```

---

## 🔴 Advanced Endpoints

### What are Advanced Endpoints?
**Advanced endpoints** demonstrate authentication, permissions, advanced filtering, pagination, and file uploads. These require authentication tokens.

### 1. List Blog Posts

**Endpoint:** `GET /api/advanced/blogposts/`

**What it does:** Lists blog posts with advanced filtering, searching, and pagination.

**Request:**
```bash
GET http://127.0.0.1:8000/api/advanced/blogposts/
```

**Query Parameters:**
- `page` - Page number
- `status` - Filter by status (draft, published, archived)
- `is_featured` - Filter featured posts (true/false)
- `author` - Filter by author ID
- `author_username` - Search by author username
- `created_after` - Posts created after date (YYYY-MM-DD)
- `views_min` - Minimum views count
- `search` - Search in title, content, tags
- `ordering` - Order by field

**Example:**
```bash
GET http://127.0.0.1:8000/api/advanced/blogposts/?status=published&is_featured=true&ordering=-views_count
```

**Response (Paginated):**
```json
{
  "count": 30,
  "next": "http://127.0.0.1:8000/api/advanced/blogposts/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Getting Started with Django",
      "slug": "getting-started-with-django",
      "author": 1,
      "author_name": "admin",
      "status": "published",
      "is_featured": true,
      "views_count": 1500,
      "likes_count": 45,
      "comments_count": 12,
      "published_at": "2024-01-10T09:00:00Z",
      "created_at": "2024-01-10T08:00:00Z"
    }
  ]
}
```

---

### 2. Create Blog Post (Requires Authentication)

**Endpoint:** `POST /api/advanced/blogposts/`

**What it does:** Creates a new blog post. Requires authentication token.

**Request:**
```bash
POST http://127.0.0.1:8000/api/advanced/blogposts/
Content-Type: application/json
Authorization: Token <your-token>
```

**Payload:**
```json
{
  "title": "My First Blog Post",
  "slug": "my-first-blog-post",
  "content": "This is the content of my blog post...",
  "status": "draft",
  "tags": "django, python, tutorial",
  "is_featured": false
}
```

**Response (201 Created):**
```json
{
  "id": 31,
  "title": "My First Blog Post",
  "slug": "my-first-blog-post",
  "content": "This is the content of my blog post...",
  "author": 1,
  "author_name": "admin",
  "status": "draft",
  "tags": "django, python, tutorial",
  "views_count": 0,
  "likes_count": 0,
  "is_featured": false,
  "published_at": null,
  "created_at": "2024-01-15T16:00:00Z"
}
```

**cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/advanced/blogposts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <your-token>" \
  -d '{
    "title": "My First Blog Post",
    "slug": "my-first-blog-post",
    "content": "This is the content...",
    "status": "draft",
    "tags": "django, python"
  }'
```

---

### 3. Get Blog Post Detail

**Endpoint:** `GET /api/advanced/blogposts/{id}/`

**What it does:** Retrieves detailed blog post with nested comments.

**Request:**
```bash
GET http://127.0.0.1:8000/api/advanced/blogposts/1/
```

**Response:**
```json
{
  "id": 1,
  "title": "Getting Started with Django",
  "slug": "getting-started-with-django",
  "content": "Full content here...",
  "author": 1,
  "author_name": "admin",
  "author_email": "admin@example.com",
  "status": "published",
  "tags": "django, python, tutorial",
  "views_count": 1500,
  "likes_count": 45,
  "is_featured": true,
  "published_at": "2024-01-10T09:00:00Z",
  "comments": [
    {
      "id": 1,
      "post": 1,
      "post_title": "Getting Started with Django",
      "author": 2,
      "author_name": "reader1",
      "content": "Great post!",
      "is_approved": true,
      "created_at": "2024-01-11T10:00:00Z"
    }
  ],
  "approved_comments_count": 12,
  "created_at": "2024-01-10T08:00:00Z",
  "updated_at": "2024-01-10T09:00:00Z"
}
```

---

### 4. Custom Action: Like Post

**Endpoint:** `POST /api/advanced/blogposts/{id}/like/`

**What it does:** Increments the like count for a blog post. Requires authentication.

**Request:**
```bash
POST http://127.0.0.1:8000/api/advanced/blogposts/1/like/
Authorization: Token <your-token>
```

**Response:**
```json
{
  "likes_count": 46
}
```

---

### 5. Custom Action: My Posts

**Endpoint:** `GET /api/advanced/blogposts/my_posts/`

**What it does:** Gets all blog posts by the authenticated user.

**Request:**
```bash
GET http://127.0.0.1:8000/api/advanced/blogposts/my_posts/
Authorization: Token <your-token>
```

**Response (Paginated):**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "title": "My First Post",
      "status": "published",
      "views_count": 100
    }
  ]
}
```

---

### 6. Create Comment

**Endpoint:** `POST /api/advanced/comments/`

**What it does:** Creates a comment on a blog post. Requires authentication.

**Request:**
```bash
POST http://127.0.0.1:8000/api/advanced/comments/
Content-Type: application/json
Authorization: Token <your-token>
```

**Payload:**
```json
{
  "post": 1,
  "content": "This is a great article! Thanks for sharing."
}
```

**Response (201 Created):**
```json
{
  "id": 13,
  "post": 1,
  "post_title": "Getting Started with Django",
  "author": 3,
  "author_name": "commenter1",
  "content": "This is a great article! Thanks for sharing.",
  "is_approved": false,
  "is_edited": false,
  "created_at": "2024-01-15T17:00:00Z"
}
```

---

### 7. Approve Comment (Custom Permission)

**Endpoint:** `POST /api/advanced/comments/{id}/approve/`

**What it does:** Approves a comment. Only post author or admin can approve.

**Request:**
```bash
POST http://127.0.0.1:8000/api/advanced/comments/1/approve/
Authorization: Token <your-token>
```

**Response:**
```json
{
  "message": "Comment approved",
  "is_approved": true
}
```

---

## 🟣 Expert Endpoints

### What are Expert Endpoints?
**Expert endpoints** demonstrate advanced patterns: caching, throttling, nested writes, bulk operations, transactions, and complex relationships.

### 1. List Companies

**Endpoint:** `GET /api/expert/companies/`

**What it does:** Lists companies with caching enabled. First request hits database, subsequent requests use cache.

**Request:**
```bash
GET http://127.0.0.1:8000/api/expert/companies/
Authorization: Token <your-token>
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "TechCorp Solutions",
    "description": "Leading technology company",
    "founded_year": 2015,
    "headquarters": "San Francisco",
    "website": "https://techcorp.com",
    "employee_count": 150,
    "departments_count": 3,
    "employees_count": 150,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

---

### 2. Get Company Statistics

**Endpoint:** `GET /api/expert/companies/{id}/statistics/`

**What it does:** Returns aggregated statistics. Results are heavily cached.

**Request:**
```bash
GET http://127.0.0.1:8000/api/expert/companies/1/statistics/
Authorization: Token <your-token>
```

**Response:**
```json
{
  "total_departments": 3,
  "total_employees": 150,
  "total_projects": 8,
  "active_projects": 5,
  "total_budget": 2500000.00,
  "average_salary": 85000.50
}
```

---

### 3. Create Department with Nested Employees

**Endpoint:** `POST /api/expert/departments/`

**What it does:** Creates a department with nested employees in a single transaction.

**Request:**
```bash
POST http://127.0.0.1:8000/api/expert/departments/
Content-Type: application/json
Authorization: Token <your-token>
```

**Payload:**
```json
{
  "company": 1,
  "name": "Engineering",
  "description": "Software development team",
  "budget": 500000.00,
  "manager": 1,
  "employees": [
    {
      "user": {
        "username": "dev1",
        "email": "dev1@company.com",
        "first_name": "John",
        "last_name": "Developer"
      },
      "employee_id": "EMP001",
      "position": "Senior Developer",
      "salary": 120000.00,
      "hire_date": "2024-01-15"
    },
    {
      "user": {
        "username": "dev2",
        "email": "dev2@company.com",
        "first_name": "Jane",
        "last_name": "Engineer"
      },
      "employee_id": "EMP002",
      "position": "Developer",
      "salary": 90000.00,
      "hire_date": "2024-01-15"
    }
  ]
}
```

**Response (201 Created):**
```json
{
  "id": 15,
  "company": 1,
  "company_name": "TechCorp Solutions",
  "name": "Engineering",
  "description": "Software development team",
  "budget": "500000.00",
  "manager": 1,
  "manager_name": "Manager Name",
  "employees": [
    {
      "id": 83,
      "user": {
        "id": 200,
        "username": "dev1",
        "email": "dev1@company.com"
      },
      "employee_id": "EMP001",
      "position": "Senior Developer",
      "salary": "120000.00"
    }
  ],
  "created_at": "2024-01-15T18:00:00Z"
}
```

---

### 4. Bulk Create Employees

**Endpoint:** `POST /api/expert/employees/bulk_create/`

**What it does:** Creates multiple employees in a single request using transactions.

**Request:**
```bash
POST http://127.0.0.1:8000/api/expert/employees/bulk_create/
Content-Type: application/json
Authorization: Token <your-token>
```

**Payload:**
```json
{
  "employees": [
    {
      "department": 1,
      "user_id": 201,
      "employee_id": "EMP100",
      "position": "Developer",
      "salary": 80000.00,
      "hire_date": "2024-01-15"
    },
    {
      "department": 1,
      "user_id": 202,
      "employee_id": "EMP101",
      "position": "Designer",
      "salary": 75000.00,
      "hire_date": "2024-01-15"
    },
    {
      "department": 1,
      "user_id": 203,
      "employee_id": "EMP102",
      "position": "QA Engineer",
      "salary": 70000.00,
      "hire_date": "2024-01-15"
    }
  ]
}
```

**Response (201 Created):**
```json
[
  {
    "id": 84,
    "department": 1,
    "department_name": "Engineering",
    "user": {
      "id": 201,
      "username": "user201",
      "email": "user201@example.com"
    },
    "employee_id": "EMP100",
    "position": "Developer",
    "salary": "80000.00"
  },
  {
    "id": 85,
    "department": 1,
    "department_name": "Engineering",
    "user": {
      "id": 202,
      "username": "user202",
      "email": "user202@example.com"
    },
    "employee_id": "EMP101",
    "position": "Designer",
    "salary": "75000.00"
  }
]
```

---

### 5. Create Project with Nested Tasks

**Endpoint:** `POST /api/expert/projects/`

**What it does:** Creates a project with nested tasks in a transaction.

**Request:**
```bash
POST http://127.0.0.1:8000/api/expert/projects/
Content-Type: application/json
Authorization: Token <your-token>
```

**Payload:**
```json
{
  "name": "Website Redesign",
  "description": "Complete website redesign project",
  "company": 1,
  "department": 1,
  "manager": 1,
  "start_date": "2024-02-01",
  "end_date": "2024-06-01",
  "budget": 200000.00,
  "status": "planning",
  "tasks": [
    {
      "title": "Design mockups",
      "description": "Create initial design mockups",
      "priority": "high",
      "status": "todo",
      "due_date": "2024-02-15"
    },
    {
      "title": "Setup development environment",
      "description": "Configure dev, staging, and production",
      "priority": "medium",
      "status": "todo",
      "due_date": "2024-02-20"
    },
    {
      "title": "Implement frontend",
      "description": "Build React components",
      "priority": "high",
      "status": "todo",
      "due_date": "2024-04-01"
    }
  ]
}
```

**Response (201 Created):**
```json
{
  "id": 19,
  "name": "Website Redesign",
  "description": "Complete website redesign project",
  "company": 1,
  "company_name": "TechCorp Solutions",
  "department": 1,
  "department_name": "Engineering",
  "manager": 1,
  "manager_name": "Manager Name",
  "start_date": "2024-02-01",
  "end_date": "2024-06-01",
  "budget": "200000.00",
  "status": "planning",
  "tasks": [
    {
      "id": 50,
      "title": "Design mockups",
      "priority": "high",
      "status": "todo"
    }
  ],
  "created_at": "2024-01-15T19:00:00Z"
}
```

---

### 6. Get Project Progress

**Endpoint:** `GET /api/expert/projects/{id}/progress/`

**What it does:** Returns project progress statistics based on tasks.

**Request:**
```bash
GET http://127.0.0.1:8000/api/expert/projects/1/progress/
Authorization: Token <your-token>
```

**Response:**
```json
{
  "total_tasks": 10,
  "todo": 3,
  "in_progress": 4,
  "review": 2,
  "done": 1,
  "completion_percentage": 10.0
}
```

---

## 🔐 Authentication

### What is Authentication?
**Authentication** verifies who you are. In APIs, this is typically done using tokens or sessions.

### Getting a Token

**Method 1: Admin Panel**
1. Visit http://127.0.0.1:8000/admin/
2. Go to "Tokens" → "Add Token"
3. Select a user
4. Save to get the token

**Method 2: Django Shell**
```python
python manage.py shell
>>> from rest_framework.authtoken.models import Token
>>> from django.contrib.auth.models import User
>>> user = User.objects.first()
>>> token, created = Token.objects.get_or_create(user=user)
>>> print(token.key)
```

### Using Token in Requests

**Header Format:**
```
Authorization: Token <your-token-here>
```

**cURL Example:**
```bash
curl -H "Authorization: Token abc123def456" \
  http://127.0.0.1:8000/api/advanced/blogposts/
```

**Python requests:**
```python
import requests

headers = {"Authorization": "Token abc123def456"}
response = requests.get(
    "http://127.0.0.1:8000/api/advanced/blogposts/",
    headers=headers
)
```

**JavaScript (fetch):**
```javascript
fetch('http://127.0.0.1:8000/api/advanced/blogposts/', {
  headers: {
    'Authorization': 'Token abc123def456'
  }
})
```

---

## 📝 Common Response Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `204 No Content` - Deleted successfully (empty response)
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource doesn't exist
- `500 Internal Server Error` - Server error

---

## 🎯 Testing Tips

1. **Use Swagger UI**: http://127.0.0.1:8000/api/docs/ - Interactive testing
2. **Start with Basics**: Test simple endpoints first
3. **Check Responses**: Always verify response structure
4. **Handle Errors**: Check status codes and error messages
5. **Use Pagination**: For list endpoints, use page parameter
6. **Filter Smartly**: Use query parameters to filter results
7. **Test Authentication**: Get token first for protected endpoints

---

**Happy API Testing!** 🚀

For interactive testing, visit: http://127.0.0.1:8000/api/docs/

