# Testing

## 🧪 Testing in DRF

### What is API Testing?

**Definition:** API testing verifies that your API endpoints work correctly, handle errors properly, and behave as expected.

**Real-life example:**
Like testing a vending machine - you insert coins (send requests), press buttons (call endpoints), and check if you get the right product (correct responses).

### APITestCase

**Definition:** `APITestCase` is Django's test case class extended for API testing. It provides an API client and authentication helpers.

**Real-life example:**
Like a specialized testing toolkit for APIs - includes everything you need to test web services.

**Setup:**
```python
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Student

class StudentAPITestCase(APITestCase):
    def setUp(self):
        """Runs before each test - sets up test data"""
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test data
        self.student = Student.objects.create(
            name='John Doe',
            age=20,
            email='john@example.com'
        )
```

### APIClient

**Definition:** `APIClient` is a test client that simulates HTTP requests to your API without running a server.

**Real-life example:**
Like a fake browser that can make requests to your API for testing purposes.

**Example:**
```python
# Import APIClient - test client for making API requests
# APIClient: Simulates HTTP requests without running server
from rest_framework.test import APIClient
# Import status codes for assertions
from rest_framework import status

class StudentAPITestCase(APITestCase):
    """
    APITestCase: Base test case for API testing
    - Provides self.client (APIClient instance)
    - Provides authentication helpers
    - Automatically uses test database
    - Alternative: Django's TestCase (but no API client)
    - Difference: APITestCase has API-specific helpers, TestCase is generic
    """
    
    def setUp(self):
        """
        setUp(): Runs before each test method
        - Sets up test data
        - Creates test fixtures
        - Called automatically by test framework
        """
        # self.client: APIClient instance (provided by APITestCase)
        # Used to make HTTP requests to API
        # Alternative: Use requests library (but requires running server)
        # Difference: APIClient is faster, no server needed
        self.client = APIClient()  # Create API client
        
        # Create test user for authentication tests
        # User.objects.create_user(): Creates user with hashed password
        # Alternative: User.objects.create() (but password not hashed)
        # Difference: create_user() hashes password, create() doesn't
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_list_students(self):
        """
        test_list_students(): Test GET endpoint
        - Tests that list endpoint returns correct data
        - Checks status code and response structure
        """
        # self.client.get(): Makes GET request
        # '/api/students/': URL path (relative to test server)
        # Returns Response object with status_code and data
        response = self.client.get('/api/students/')
        
        # self.assertEqual(): Asserts two values are equal
        # response.status_code: HTTP status code (200, 404, etc.)
        # status.HTTP_200_OK: DRF constant for 200 status
        # Alternative: assert response.status_code == 200 (less readable)
        # Difference: status constants are more readable and maintainable
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # response.data: Parsed response body (dict/list)
        # Automatically deserialized from JSON
        # Alternative: response.json() (manual parsing)
        # Difference: data is already parsed, json() requires manual call
        self.assertEqual(len(response.data), 1)
    
    def test_create_student(self):
        """
        test_create_student(): Test POST endpoint
        - Tests that create endpoint accepts data and creates resource
        - Checks status code and database state
        """
        # Test data dictionary
        # Matches serializer field names
        data = {
            'name': 'Jane Doe',
            'age': 22,
            'email': 'jane@example.com'
        }
        
        # self.client.post(): Makes POST request
        # '/api/students/': URL path
        # data: Request body (automatically serialized to JSON)
        # format='json': Content-Type header set to application/json
        # Alternative: format='multipart' (for file uploads)
        # Difference: json is for API data, multipart is for forms/files
        response = self.client.post('/api/students/', data, format='json')
        
        # Assert 201 Created status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Assert database state changed
        # Student.objects.count(): Returns number of Student objects
        # Should be 2 (1 from setUp + 1 from POST)
        # Alternative: Check response.data for created object
        # Difference: count() checks database, response.data checks API response
        self.assertEqual(Student.objects.count(), 2)
```

**HTTP Methods:**
```python
# GET request
response = self.client.get('/api/students/')

# POST request
response = self.client.post('/api/students/', data, format='json')

# PUT request
response = self.client.put('/api/students/1/', data, format='json')

# PATCH request
response = self.client.patch('/api/students/1/', data, format='json')

# DELETE request
response = self.client.delete('/api/students/1/')

# OPTIONS request
response = self.client.options('/api/students/')
```

### Authentication Testing

**Definition:** Testing endpoints that require authentication.

**Example:**
```python
from rest_framework.test import APIClient
from django.contrib.auth.models import User

class SecureAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_unauthenticated_access(self):
        """Test that unauthenticated requests are rejected"""
        response = self.client.get('/api/secure-endpoint/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_authenticated_access(self):
        """Test that authenticated requests succeed"""
        # Force authentication
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/secure-endpoint/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

**Token Authentication Testing:**
```python
from rest_framework.authtoken.models import Token

class TokenAuthTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
    
    def test_token_authentication(self):
        """Test authentication with token"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/protected/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

**JWT Authentication Testing:**
```python
from rest_framework_simplejwt.tokens import RefreshToken

class JWTAuthTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
    
    def test_jwt_authentication(self):
        """Test authentication with JWT"""
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )
        response = self.client.get('/api/protected/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

### Permission Testing

**Definition:** Testing that permissions work correctly - different users have different access levels.

**Example:**
```python
class PermissionTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create regular user
        self.user = User.objects.create_user(
            username='user',
            password='pass123'
        )
        
        # Create admin user
        self.admin = User.objects.create_user(
            username='admin',
            password='admin123',
            is_staff=True
        )
        
        self.student = Student.objects.create(
            name='Test Student',
            email='test@example.com'
        )
    
    def test_user_cannot_delete(self):
        """Test that regular users cannot delete"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/students/{self.student.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_admin_can_delete(self):
        """Test that admins can delete"""
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f'/api/students/{self.student.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_owner_can_update(self):
        """Test that owners can update their own objects"""
        # Assuming student has owner field
        self.student.owner = self.user
        self.student.save()
        
        self.client.force_authenticate(user=self.user)
        data = {'name': 'Updated Name'}
        response = self.client.patch(
            f'/api/students/{self.student.id}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

**Object-Level Permission Testing:**
```python
class ObjectPermissionTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create_user('owner', 'pass')
        self.other = User.objects.create_user('other', 'pass')
        
        self.post = Post.objects.create(
            title='Test Post',
            author=self.owner
        )
    
    def test_owner_can_update(self):
        """Owner can update their post"""
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(
            f'/api/posts/{self.post.id}/',
            {'title': 'Updated'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_other_cannot_update(self):
        """Other users cannot update"""
        self.client.force_authenticate(user=self.other)
        response = self.client.patch(
            f'/api/posts/{self.post.id}/',
            {'title': 'Hacked'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
```

### Serializer Testing

**Definition:** Testing serializers independently to ensure they validate and transform data correctly.

**Example:**
```python
from rest_framework.test import APITestCase
from .serializers import StudentSerializer
from .models import Student

class SerializerTestCase(APITestCase):
    def setUp(self):
        self.student_data = {
            'name': 'John Doe',
            'age': 20,
            'email': 'john@example.com'
        }
    
    def test_serializer_valid_data(self):
        """Test serializer with valid data"""
        serializer = StudentSerializer(data=self.student_data)
        self.assertTrue(serializer.is_valid())
    
    def test_serializer_invalid_age(self):
        """Test serializer validation"""
        invalid_data = self.student_data.copy()
        invalid_data['age'] = -5  # Invalid age
        
        serializer = StudentSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('age', serializer.errors)
    
    def test_serializer_create(self):
        """Test serializer creates object"""
        serializer = StudentSerializer(data=self.student_data)
        self.assertTrue(serializer.is_valid())
        student = serializer.save()
        self.assertIsInstance(student, Student)
        self.assertEqual(student.name, 'John Doe')
    
    def test_serializer_update(self):
        """Test serializer updates object"""
        student = Student.objects.create(**self.student_data)
        
        update_data = {'name': 'Jane Doe'}
        serializer = StudentSerializer(
            instance=student,
            data=update_data,
            partial=True
        )
        self.assertTrue(serializer.is_valid())
        updated_student = serializer.save()
        self.assertEqual(updated_student.name, 'Jane Doe')
    
    def test_serializer_to_representation(self):
        """Test serializer output format"""
        student = Student.objects.create(**self.student_data)
        serializer = StudentSerializer(student)
        data = serializer.data
        
        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertEqual(data['name'], 'John Doe')
```

### Mocking External APIs

**Definition:** Mocking replaces external API calls with fake responses during testing.

**Real-life example:**
Like using a fake phone instead of calling real numbers during testing - you control the response.

**Using unittest.mock:**
```python
from unittest.mock import patch, Mock
from rest_framework.test import APITestCase

class ExternalAPITestCase(APITestCase):
    @patch('myapp.services.payment_gateway.charge_card')
    def test_payment_with_mock(self, mock_charge):
        """Test payment with mocked external API"""
        # Mock the external API response
        mock_charge.return_value = {
            'success': True,
            'transaction_id': '12345'
        }
        
        # Make request
        data = {'amount': 100, 'card': '1234567890'}
        response = self.client.post('/api/payments/', data, format='json')
        
        # Verify
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_charge.assert_called_once_with(amount=100, card='1234567890')
    
    @patch('requests.get')
    def test_external_api_call(self, mock_get):
        """Test external API call with mock"""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {'data': 'test'}
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Make request that triggers external API call
        response = self.client.get('/api/external-data/')
        
        # Verify
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_get.assert_called_once()
```

**Using responses library:**
```bash
pip install responses
```

```python
import responses
from rest_framework.test import APITestCase

class ExternalAPITestCase(APITestCase):
    @responses.activate
    def test_external_api(self):
        """Test external API with responses library"""
        # Mock external API endpoint
        responses.add(
            responses.GET,
            'https://api.external.com/data',
            json={'result': 'success'},
            status=200
        )
        
        # Make request
        response = self.client.get('/api/fetch-external/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

### Complete Test Example

**Real Project Example:**
```python
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Book, Author

class BookAPITestCase(APITestCase):
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.admin = User.objects.create_user(
            username='admin',
            password='admin123',
            is_staff=True
        )
        
        # Create token
        self.token = Token.objects.create(user=self.user)
        
        # Create test data
        self.author = Author.objects.create(name='John Doe')
        self.book = Book.objects.create(
            title='Test Book',
            author=self.author,
            price=29.99
        )
    
    def test_list_books_unauthenticated(self):
        """Anyone can list books"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_book_unauthenticated_fails(self):
        """Unauthenticated users cannot create books"""
        data = {'title': 'New Book', 'author': self.author.id}
        response = self.client.post('/api/books/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_book_authenticated(self):
        """Authenticated users can create books"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {
            'title': 'New Book',
            'author': self.author.id,
            'price': 19.99
        }
        response = self.client.post('/api/books/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
    
    def test_update_book_permission(self):
        """Only owners or admins can update"""
        # Regular user cannot update
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.patch(
            f'/api/books/{self.book.id}/',
            {'title': 'Updated'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Admin can update
        admin_token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + admin_token.key)
        response = self.client.patch(
            f'/api/books/{self.book.id}/',
            {'title': 'Updated'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_book_admin_only(self):
        """Only admins can delete"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        admin_token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + admin_token.key)
        response = self.client.delete(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
```

### Best Practices

1. **Test isolation:** Each test should be independent
2. **Use setUp:** Prepare test data in setUp method
3. **Test both success and failure cases**
4. **Test edge cases:** Boundary conditions, empty data, etc.
5. **Mock external dependencies:** Don't call real external APIs
6. **Use descriptive test names:** `test_user_cannot_delete_others_post`
7. **Keep tests fast:** Use database transactions when possible
8. **Test serializers separately:** Faster than full API tests

---

## 🎓 Advanced Interview Topics (4+ Years Experience)

### Test Coverage Strategies

**1. Coverage Analysis:**
```python
# Install: pip install coverage
# Run: coverage run --source='.' manage.py test
# Report: coverage report
# HTML: coverage html

# .coveragerc
[run]
source = myapp
omit = */migrations/*, */tests/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
```

**2. Property-Based Testing:**
```python
# Install: pip install hypothesis
from hypothesis import given, strategies as st

class StudentSerializerTest(APITestCase):
    @given(
        name=st.text(min_size=1, max_size=100),
        age=st.integers(min_value=1, max_value=120)
    )
    def test_serializer_accepts_valid_data(self, name, age):
        """Test with randomly generated valid data"""
        data = {'name': name, 'age': age, 'email': 'test@example.com'}
        serializer = StudentSerializer(data=data)
        self.assertTrue(serializer.is_valid())
```

### Advanced Mocking

**1. Mocking External APIs:**
```python
from unittest.mock import patch, Mock
import requests

class ExternalAPITest(APITestCase):
    @patch('myapp.services.requests.get')
    def test_external_api_integration(self, mock_get):
        """Mock external API calls"""
        # Configure mock response
        mock_response = Mock()
        mock_response.json.return_value = {'status': 'success'}
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Test code that uses external API
        response = self.client.get('/api/external-data/')
        self.assertEqual(response.status_code, 200)
        
        # Verify API was called
        mock_get.assert_called_once()
```

**2. Mocking Database Queries:**
```python
from unittest.mock import patch

class DatabaseMockTest(APITestCase):
    @patch('myapp.models.Student.objects.filter')
    def test_custom_queryset(self, mock_filter):
        """Mock database queries"""
        # Configure mock
        mock_queryset = Mock()
        mock_queryset.all.return_value = [Mock(name='Test')]
        mock_filter.return_value = mock_queryset
        
        # Test
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, 200)
```

### Performance Testing

**1. Load Testing:**
```python
from django.test import TransactionTestCase
import time

class PerformanceTest(TransactionTestCase):
    def test_list_performance(self):
        """Test that list endpoint is fast"""
        # Create test data
        for i in range(1000):
            Student.objects.create(name=f'Student {i}')
        
        start = time.time()
        response = self.client.get('/api/students/')
        duration = time.time() - start
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(duration, 1.0)  # Should complete in < 1 second
```

**2. Query Count Testing:**
```python
from django.test.utils import override_settings
from django.db import connection

class QueryCountTest(APITestCase):
    @override_settings(DEBUG=True)
    def test_n_plus_one_prevention(self):
        """Test that N+1 queries are prevented"""
        # Create test data
        author = Author.objects.create(name='John')
        for i in range(10):
            Book.objects.create(title=f'Book {i}', author=author)
        
        initial_queries = len(connection.queries)
        response = self.client.get('/api/books/')
        queries_executed = len(connection.queries) - initial_queries
        
        # Should be 2 queries (1 for books, 1 for authors with select_related)
        self.assertLessEqual(queries_executed, 2)
        self.assertEqual(response.status_code, 200)
```

### Integration Testing

**1. Testing with Real Database:**
```python
from django.test import TransactionTestCase

class IntegrationTest(TransactionTestCase):
    """Use TransactionTestCase for database transactions"""
    
    def test_complex_workflow(self):
        """Test complete user workflow"""
        # 1. Create user
        user_data = {'username': 'test', 'password': 'pass'}
        response = self.client.post('/api/users/', user_data)
        user_id = response.data['id']
        
        # 2. Login
        response = self.client.post('/api/login/', user_data)
        token = response.data['token']
        
        # 3. Create resource with authentication
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        resource_data = {'name': 'Test Resource'}
        response = self.client.post('/api/resources/', resource_data)
        
        self.assertEqual(response.status_code, 201)
```

### Test Fixtures

**1. Using Fixtures:**
```python
# fixtures/students.json
[
    {
        "model": "myapp.student",
        "pk": 1,
        "fields": {
            "name": "John Doe",
            "age": 20
        }
    }
]

# In test
class StudentTest(APITestCase):
    fixtures = ['students.json']  # Load fixtures
    
    def test_list_students(self):
        response = self.client.get('/api/students/')
        self.assertEqual(len(response.data), 1)
```

**2. Factory Pattern:**
```python
# Install: pip install factory_boy
import factory

class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student
    
    name = factory.Sequence(lambda n: f'Student {n}')
    age = factory.Faker('random_int', min=18, max=65)
    email = factory.LazyAttribute(lambda obj: f'{obj.name.lower()}@example.com')

# In test
class StudentTest(APITestCase):
    def setUp(self):
        self.students = StudentFactory.create_batch(10)
    
    def test_list(self):
        response = self.client.get('/api/students/')
        self.assertEqual(len(response.data), 10)
```

### Contract Testing

**1. API Contract Testing:**
```python
class APIContractTest(APITestCase):
    def test_response_schema(self):
        """Test that response matches expected schema"""
        response = self.client.get('/api/students/1/')
        
        # Verify required fields exist
        self.assertIn('id', response.data)
        self.assertIn('name', response.data)
        self.assertIn('age', response.data)
        
        # Verify field types
        self.assertIsInstance(response.data['id'], int)
        self.assertIsInstance(response.data['name'], str)
        self.assertIsInstance(response.data['age'], int)
        
        # Verify field constraints
        self.assertGreaterEqual(response.data['age'], 0)
```

### Test Organization

**1. Test Structure:**
```python
# tests/
#   __init__.py
#   test_models.py      # Model tests
#   test_serializers.py # Serializer tests
#   test_views.py       # View tests
#   test_permissions.py # Permission tests
#   test_integration.py # Integration tests
#   factories.py        # Test factories
#   fixtures/           # Test fixtures
```

**2. Test Tags:**
```python
# Mark slow tests
from django.test import tag

@tag('slow')
class SlowTest(APITestCase):
    def test_complex_operation(self):
        # Long-running test
        pass

# Run only fast tests: python manage.py test --exclude-tag=slow
# Run only slow tests: python manage.py test --tag=slow
```

---

*This guide covers essential and advanced testing patterns. Master these for senior Django REST Framework positions.*

