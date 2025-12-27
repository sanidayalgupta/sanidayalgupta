# Swagger/OpenAPI Documentation Guide

## 🎉 Swagger Documentation is Now Available!

Your DRF Tutorial API now has beautiful, interactive API documentation powered by **drf-spectacular**.

## 📍 Access Points

### 1. Swagger UI (Interactive)
**URL:** http://127.0.0.1:8000/api/docs/

This is the main interactive documentation where you can:
- Browse all API endpoints
- See request/response schemas
- Test endpoints directly in the browser
- View authentication requirements
- See example requests and responses

**Real-life example:**
Like an interactive restaurant menu where you can see pictures, descriptions, prices,
and even place orders directly!

### 2. ReDoc (Clean Documentation)
**URL:** http://127.0.0.1:8000/api/redoc/

Alternative documentation view that's cleaner and more readable.
Great for printing or sharing with team members.

### 3. OpenAPI Schema (JSON/YAML)
**URL:** http://127.0.0.1:8000/api/schema/

Raw OpenAPI schema that can be imported into:
- Postman
- Insomnia
- Other API testing tools
- Code generators

## 🎯 Features

### Organized by Tags
Endpoints are organized into 4 categories:
- **Basics** - Level 1: Basic CRUD operations
- **Intermediate** - Level 2: ViewSets and relationships
- **Advanced** - Level 3: Authentication and permissions
- **Expert** - Level 4: Caching and advanced patterns

### Try It Out!
Click on any endpoint to:
1. See detailed description
2. View required/optional parameters
3. See example request body
4. Test the endpoint directly
5. View response examples

### Authentication
For protected endpoints:
1. Click "Authorize" button at top
2. Enter your token: `Token <your-token>`
3. Or use session authentication by logging in

## 📊 Current Data Status

After running `populate_data`, you now have:
- ✅ **30 Students** - Ready to test basics endpoints
- ✅ **10 Courses** - Available for course endpoints
- ✅ **20 Authors** - For intermediate app
- ✅ **50 Books** - With reviews and categories
- ✅ **15 Users** - With profiles and tokens
- ✅ **30 Blog Posts** - With comments
- ✅ **5 Companies** - With departments, employees, projects, and tasks

## 🚀 Quick Start

1. **Start the server:**
   ```bash
   python manage.py runserver
   ```

2. **Visit Swagger:**
   Open http://127.0.0.1:8000/api/docs/ in your browser

3. **Try an endpoint:**
   - Expand "Basics" section
   - Click on "GET /api/basics/students-fbv/"
   - Click "Try it out"
   - Click "Execute"
   - See the response!

4. **Test authenticated endpoints:**
   - Click "Authorize" at top
   - Get a token from admin panel or create one
   - Enter: `Token <your-token>`
   - Now you can test protected endpoints

## 📝 Example: Testing an Endpoint

### Step 1: Open Swagger
Visit http://127.0.0.1:8000/api/docs/

### Step 2: Find an Endpoint
Navigate to "Basics" → "POST /api/basics/students-fbv/"

### Step 3: Try It Out
1. Click "Try it out" button
2. Enter request body:
   ```json
   {
     "name": "John Doe",
     "email": "john@example.com",
     "age": 20,
     "grade": "A"
   }
   ```
3. Click "Execute"

### Step 4: See Response
You'll see:
- Status code (201 Created)
- Response body with the created student
- Response headers

## 🔑 Getting an API Token

### Method 1: Admin Panel
1. Visit http://127.0.0.1:8000/admin/
2. Go to "Tokens" under "AUTHENTICATION AND AUTHORIZATION"
3. Create a token for your user

### Method 2: Django Shell
```python
python manage.py shell
>>> from rest_framework.authtoken.models import Token
>>> from django.contrib.auth.models import User
>>> user = User.objects.first()
>>> token, created = Token.objects.get_or_create(user=user)
>>> print(token.key)
```

### Method 3: Use Existing User
If you ran `populate_data`, some users already have tokens created.

## 🎨 Swagger Features Explained

### Request Body Examples
Swagger automatically generates example request bodies based on your serializers.
Like a form that's already filled out with sample data!

### Response Schemas
See exactly what the API will return before you call it.
Like seeing a preview of a product before buying.

### Authentication
Swagger handles authentication automatically once you authorize.
Like a keycard that works for all doors after you swipe it once.

### Filtering & Pagination
See all available query parameters for filtering and pagination.
Like advanced search options in an online store.

## 📚 Documentation Sections

### Basics Endpoints
- Student CRUD operations
- Course management
- Function-based and class-based views

### Intermediate Endpoints
- Book management with ViewSets
- Author and category relationships
- Custom actions (reviews, available books)

### Advanced Endpoints
- Blog post management (requires auth)
- Comment system
- User profiles
- Filtering and pagination examples

### Expert Endpoints
- Company management
- Department and employee hierarchies
- Project and task management
- Bulk operations
- Caching examples

## 💡 Tips

1. **Use the search box** - Quickly find endpoints by name
2. **Check the schema** - Click "Schema" to see detailed field descriptions
3. **Try different methods** - Each endpoint shows all available HTTP methods
4. **View examples** - Swagger shows example requests and responses
5. **Export schema** - Download OpenAPI schema for other tools

## 🎓 Learning with Swagger

Swagger makes learning DRF easier because:
- ✅ See all endpoints in one place
- ✅ Understand request/response formats
- ✅ Test without writing code
- ✅ Learn by doing (interactive)
- ✅ See real examples with your data

---

**Happy API Exploring!** 🚀

Visit http://127.0.0.1:8000/api/docs/ to get started!

