# Serializers

## 📝 Serializers

### Serializer

**Definition:** Serializers convert complex data types (Django models) to/from JSON. They're like translators.

**Real-life example:**
Like a translator between languages - converts Python objects to JSON (and vice versa).

**Example:**
```python
# Import serializers module from DRF
# serializers: DRF's serialization framework
from rest_framework import serializers

# Serializer: Base serializer class (manual field definition)
# - Full control over fields and validation
# - Must implement create() and update() methods
# - Alternative: ModelSerializer (automatic field generation)
# - Difference: Serializer requires manual field definition, ModelSerializer auto-generates from model
class StudentSerializer(serializers.Serializer):
    # CharField: Text field with max length validation
    # max_length: Maximum characters allowed (enforced at validation)
    name = serializers.CharField(max_length=100)
    
    # IntegerField: Integer number field
    # Validates that value is an integer
    age = serializers.IntegerField()
    
    # EmailField: Email format validation
    # Automatically validates email format (regex-based)
    # Alternative: CharField with custom validator
    email = serializers.EmailField()
    
    def create(self, validated_data):
        """
        create(): Called when serializer.save() is used for new objects
        validated_data: Dictionary of validated field values (already checked)
        Returns: Created model instance
        
        This method is REQUIRED for serializers.Serializer
        Alternative: Use ModelSerializer which provides this automatically
        """
        # **validated_data: Unpacks dictionary as keyword arguments
        # Student.objects.create(): Creates and saves model instance in one step
        # Alternative: student = Student(**validated_data); student.save()
        return Student.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        update(): Called when serializer.save(instance=obj) is used for existing objects
        instance: Existing model instance to update
        validated_data: Dictionary of validated field values
        Returns: Updated model instance
        
        This method is REQUIRED for serializers.Serializer
        Alternative: Use ModelSerializer which provides this automatically
        """
        # validated_data.get(): Gets value from dict, returns existing value if key missing
        # This pattern preserves existing values if not provided in update
        # Alternative: instance.name = validated_data['name'] (raises KeyError if missing)
        instance.name = validated_data.get('name', instance.name)
        instance.age = validated_data.get('age', instance.age)
        instance.email = validated_data.get('email', instance.email)
        
        # instance.save(): Saves changes to database
        # Only modified fields are updated (Django tracks changes)
        instance.save()
        return instance

# Alternative: Using ModelSerializer (simpler, less control)
# class StudentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = ['name', 'age', 'email']
#     # create() and update() are automatically provided
```

### ModelSerializer

**Definition:** ModelSerializer automatically generates serializer fields from a model.

**Real-life example:**
Like an automatic translator - you just point to the model, and it translates automatically.

**Example:**
```python
# Import serializers module
from rest_framework import serializers
# Import model to serialize
from .models import Student

# ModelSerializer: Automatically generates fields from model
# - Automatically handles create() and update()
# - Automatically validates based on model field types
# - Alternative: Serializer (manual control, more code)
# - Difference: ModelSerializer is model-aware, Serializer is generic
class StudentSerializer(serializers.ModelSerializer):
    """
    ModelSerializer automatically:
    1. Generates fields from model
    2. Provides create() method
    3. Provides update() method
    4. Validates based on model field constraints
    """
    
    # Meta class: Configuration for ModelSerializer
    # Required attributes: model, fields (or exclude)
    class Meta:
        # model: Django model class to serialize
        model = Student
        
        # fields: List of model fields to include in serializer
        # Alternative: fields = '__all__' (includes all fields)
        # Alternative: exclude = ['password'] (excludes specific fields)
        # Difference: fields is explicit, exclude is implicit
        fields = ['id', 'name', 'email', 'age']
        
        # Automatically handles create() and update()
        # No need to implement these methods
    
    # Optional: Add extra fields not in model
    # SerializerMethodField: Read-only field computed from model instance
    # - Read-only by default (not included in validated_data)
    # - Requires get_<field_name> method
    # - Alternative: Property on model, or computed in to_representation()
    full_name = serializers.SerializerMethodField()
    
    def get_full_name(self, obj):
        """
        get_full_name(): Method to compute SerializerMethodField value
        obj: Model instance being serialized
        Returns: Computed value for full_name field
        
        Method name MUST be get_<field_name>()
        Called during serialization (model → JSON)
        """
        # obj: The model instance (Student object)
        # Access model fields directly
        return f"{obj.first_name} {obj.last_name}"

# Alternative: Using property on model
# class Student(models.Model):
#     @property
#     def full_name(self):
#         return f"{self.first_name} {self.last_name}"
# 
# # In serializer:
# class StudentSerializer(serializers.ModelSerializer):
#     full_name = serializers.ReadOnlyField()  # Uses model property
#     class Meta:
#         model = Student
#         fields = ['id', 'name', 'full_name']
```

### Fields & Field Types

**Definition:** Fields define what data can be stored and how it's validated.

**Common Field Types:**
```python
CharField(max_length=100)              # Text
IntegerField()                          # Number
FloatField()                           # Decimal number
DecimalField(max_digits=10, decimal_places=2)  # Money
EmailField()                           # Email format
BooleanField()                         # True/False
DateField()                            # Date
DateTimeField()                        # Date and time
TimeField()                            # Time
URLField()                             # URL
UUIDField()                            # UUID
FileField()                            # File upload
ImageField()                           # Image upload
ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])  # Choices
```

**Example:**
```python
class StudentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, required=True)
    age = serializers.IntegerField(min_value=0, max_value=120)
    email = serializers.EmailField()
    is_active = serializers.BooleanField(default=True)
    birth_date = serializers.DateField()
    grade = serializers.ChoiceField(choices=['A', 'B', 'C', 'D'])
    
    class Meta:
        model = Student
        fields = '__all__'
```

### read_only, write_only

**Definition:**
- **read_only** - Field appears in responses but not in requests
- **write_only** - Field appears in requests but not in responses

**Real-life example:**
- **read_only** = Like a display-only screen (you can see but not change)
- **write_only** = Like a password field (you enter but don't see back)

**Example:**
```python
class StudentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)  # Auto-generated, never sent in POST
    password = serializers.CharField(write_only=True)  # Never returned in response
    created_at = serializers.DateTimeField(read_only=True)  # Auto-set, read-only
    
    class Meta:
        model = Student
        fields = ['id', 'name', 'password', 'created_at']
```

**Real Project Example:**
```python
class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 
                  'confirm_password', 'date_joined']
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return data
```

### Validation

**Definition:** Validation ensures data is correct before saving.

**Types:**
1. **Field-level** - Validates individual fields
2. **Object-level** - Validates entire object

**Field-level Validation:**
```python
class StudentSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField()
    email = serializers.EmailField()
    
    def validate_age(self, value):
        """Field-level validation for age"""
        if value < 5 or value > 100:
            raise serializers.ValidationError("Age must be between 5 and 100")
        return value
    
    def validate_email(self, value):
        """Field-level validation for email"""
        if Student.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
```

**Object-level Validation:**
```python
class StudentSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField()
    grade = serializers.CharField()
    
    def validate(self, data):
        """Object-level validation"""
        age = data.get('age')
        grade = data.get('grade')
        
        # Minors need good grades
        if age < 18 and grade not in ['A', 'B']:
            raise serializers.ValidationError(
                "Minors must have grade A or B"
            )
        
        return data
```

**Custom Validators:**
```python
from rest_framework import serializers

def validate_phone_number(value):
    """Custom validator function"""
    if not value.startswith('+'):
        raise serializers.ValidationError("Phone must start with +")
    if len(value) < 10:
        raise serializers.ValidationError("Phone too short")
    return value

class StudentSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(validators=[validate_phone_number])
    
    class Meta:
        model = Student
        fields = ['name', 'phone']
```

### SerializerMethodField

**Definition:** SerializerMethodField allows you to add computed fields that aren't in the model.

**Real-life example:**
Like a calculated field - not stored, but computed when needed (like "full name" = first + last).

**Example:**
```python
class StudentSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    is_adult = serializers.SerializerMethodField()
    
    def get_full_name(self, obj):
        """Method name must start with get_"""
        return f"{obj.first_name} {obj.last_name}"
    
    def get_is_adult(self, obj):
        """Computed field based on age"""
        return obj.age >= 18
    
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'full_name', 
                  'age', 'is_adult']
```

**Real Project Example:**
```python
class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    
    def get_total_price(self, obj):
        """Calculate total from order items"""
        return sum(item.price * item.quantity for item in obj.items.all())
    
    def get_status_display(self, obj):
        """Human-readable status"""
        status_map = {
            'P': 'Pending',
            'S': 'Shipped',
            'D': 'Delivered',
            'C': 'Cancelled'
        }
        return status_map.get(obj.status, 'Unknown')
    
    class Meta:
        model = Order
        fields = ['id', 'status', 'status_display', 'total_price']
```

### Dynamic Fields in Serializers

**Definition:** Dynamic fields allow you to include/exclude fields based on context or request.

**Example:**
```python
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        """Dynamically modify fields"""
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        
        if fields:
            # Remove fields not in the fields list
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

# Usage:
# serializer = StudentSerializer(student, fields=['id', 'name'])
```

**Real Project Example:**
```python
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        request = kwargs.get('context', {}).get('request')
        super().__init__(*args, **kwargs)
        
        # Hide price for non-authenticated users
        if request and not request.user.is_authenticated:
            self.fields.pop('price')
            self.fields.pop('cost')
```

### Conditional Serialization

**Definition:** Conditional serialization shows different fields based on conditions.

**Example:**
```python
class StudentSerializer(serializers.ModelSerializer):
    detailed_info = serializers.SerializerMethodField()
    
    def get_detailed_info(self, obj):
        """Only include detailed info for admins"""
        request = self.context.get('request')
        if request and request.user.is_staff:
            return {
                'address': obj.address,
                'phone': obj.phone,
                'emergency_contact': obj.emergency_contact
            }
        return None
    
    class Meta:
        model = Student
        fields = ['id', 'name', 'detailed_info']
```

### Nested Serializers

**Definition:** Nested serializers include related objects within a serializer.

**Real-life example:**
Like a product page showing the product AND manufacturer info together.

**Example:**
```python
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio']

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)  # Nested, read-only
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author']

# Response:
# {
#   "id": 1,
#   "title": "Django Guide",
#   "author": {
#     "id": 1,
#     "name": "John Doe",
#     "bio": "Expert developer"
#   }
# }
```

### Writable Nested Serializers

**Definition:** Writable nested serializers allow creating related objects along with the main object.

**Real-life example:**
Like ordering a pizza with toppings - you specify both in one order.

**Example:**
```python
from django.db import transaction

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']

class ProjectCreateSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)  # Nested and writable
    
    class Meta:
        model = Project
        fields = ['name', 'description', 'tasks']
    
    def create(self, validated_data):
        tasks_data = validated_data.pop('tasks')
        
        with transaction.atomic():
            project = Project.objects.create(**validated_data)
            for task_data in tasks_data:
                Task.objects.create(project=project, **task_data)
        
        return project

# Usage:
# POST /projects/
# {
#   "name": "New Project",
#   "tasks": [
#     {"title": "Task 1", "description": "Do something"},
#     {"title": "Task 2", "description": "Do something else"}
#   ]
# }
```

### to_representation()

**Definition:** `to_representation()` controls how data is serialized (model → JSON).

**Real-life example:**
Like formatting data before showing it - you control exactly how it looks.

**Example:**
```python
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'age', 'created_at']
    
    def to_representation(self, instance):
        """Customize output format"""
        representation = super().to_representation(instance)
        
        # Format date
        representation['created_at'] = instance.created_at.strftime('%Y-%m-%d')
        
        # Add computed field
        representation['age_group'] = 'Adult' if instance.age >= 18 else 'Minor'
        
        # Remove field conditionally
        if not self.context.get('request').user.is_staff:
            representation.pop('internal_notes', None)
        
        return representation
```

**Real Project Example:**
```python
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Format currency
        data['total'] = f"${instance.total:.2f}"
        
        # Include nested items count
        data['items_count'] = instance.items.count()
        
        # Add human-readable status
        data['status_label'] = instance.get_status_display()
        
        return data
```

### create() & update() Overrides

**Definition:** Override `create()` and `update()` to customize how objects are saved.

**Example:**
```python
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'email', 'age']
    
    def create(self, validated_data):
        """Custom create logic"""
        # Add default values
        validated_data['created_by'] = self.context['request'].user
        
        # Set initial status
        validated_data['status'] = 'active'
        
        # Create student
        student = Student.objects.create(**validated_data)
        
        # Send welcome email
        send_welcome_email(student.email)
        
        return student
    
    def update(self, instance, validated_data):
        """Custom update logic"""
        # Update fields
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.age = validated_data.get('age', instance.age)
        
        # Track who updated
        instance.updated_by = self.context['request'].user
        instance.updated_at = timezone.now()
        
        instance.save()
        return instance
```

**Real Project Example:**
```python
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    
    class Meta:
        model = Order
        fields = ['customer', 'items', 'shipping_address']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        
        with transaction.atomic():
            # Create order
            order = Order.objects.create(
                customer=user,
                order_number=self.generate_order_number(),
                **validated_data
            )
            
            # Create order items
            total = 0
            for item_data in items_data:
                item = OrderItem.objects.create(order=order, **item_data)
                total += item.price * item.quantity
            
            # Update total
            order.total = total
            order.save()
            
            # Create payment record
            Payment.objects.create(order=order, amount=total)
        
        return order
    
    def generate_order_number(self):
        return f"ORD-{timezone.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
```

---

## 🎓 Advanced Interview Topics (4+ Years Experience)

### Serializer Performance Optimization

**1. Using `only()` and `defer()` in Serializers:**
```python
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
    
    def to_representation(self, instance):
        # Optimize queryset to only fetch needed fields
        # This reduces memory and database load
        representation = super().to_representation(instance)
        return representation

# In ViewSet, optimize queryset:
class StudentViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        # Only fetch fields needed by serializer
        return Student.objects.only('id', 'name', 'email', 'age')
    
    # Or defer heavy fields
    def get_queryset(self):
        return Student.objects.defer('biography', 'large_text_field')
```

**2. Serializer Caching:**
```python
from django.core.cache import cache

class StudentSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        # Cache serialized representation
        cache_key = f'student_serialized_{instance.id}'
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        representation = super().to_representation(instance)
        cache.set(cache_key, representation, 3600)  # 1 hour
        return representation
```

### Advanced Serializer Patterns

**1. Polymorphic Serializers:**
```python
# Handle different types in same serializer
class ContentSerializer(serializers.Serializer):
    content_type = serializers.CharField()
    
    def to_representation(self, instance):
        # Route to appropriate serializer based on type
        if instance.content_type == 'article':
            return ArticleSerializer(instance).data
        elif instance.content_type == 'video':
            return VideoSerializer(instance).data
        return super().to_representation(instance)
```

**2. Dynamic Field Selection:**
```python
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        # Get fields parameter from context
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        
        if fields:
            # Remove fields not in requested list
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

# Usage:
# serializer = StudentSerializer(student, fields=['id', 'name'])
```

**3. Serializer Inheritance:**
```python
# Base serializer with common fields
class BaseStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'email']

# Extended serializer with additional fields
class DetailedStudentSerializer(BaseStudentSerializer):
    courses = CourseSerializer(many=True, read_only=True)
    statistics = serializers.SerializerMethodField()
    
    class Meta(BaseStudentSerializer.Meta):
        fields = BaseStudentSerializer.Meta.fields + ['courses', 'statistics']
```

### Serializer Validation Best Practices

**1. Cross-Field Validation:**
```python
class OrderSerializer(serializers.ModelSerializer):
    def validate(self, data):
        """Object-level validation"""
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError({
                'end_date': 'End date must be after start date'
            })
        
        return data
```

**2. Conditional Validation:**
```python
class StudentSerializer(serializers.ModelSerializer):
    def validate_age(self, value):
        """Age validation based on grade"""
        request = self.context.get('request')
        grade = self.initial_data.get('grade')
        
        if grade == 'kindergarten' and value > 6:
            raise serializers.ValidationError(
                "Kindergarten students must be 6 or younger"
            )
        return value
```

### Serializer Testing

**1. Testing Serialization:**
```python
from rest_framework.test import APITestCase
from .serializers import StudentSerializer

class StudentSerializerTest(APITestCase):
    def test_serialization(self):
        student = Student.objects.create(name='John', age=20)
        serializer = StudentSerializer(student)
        self.assertEqual(serializer.data['name'], 'John')
        self.assertEqual(serializer.data['age'], 20)
    
    def test_deserialization(self):
        data = {'name': 'Jane', 'age': 22, 'email': 'jane@test.com'}
        serializer = StudentSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        student = serializer.save()
        self.assertEqual(student.name, 'Jane')
    
    def test_validation(self):
        data = {'name': 'Test', 'age': 200}  # Invalid age
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('age', serializer.errors)
```

### Serializer vs Model Methods

**When to Use Serializer Methods:**
- ✅ Data transformation for API (formatting, calculations)
- ✅ Conditional fields based on user/context
- ✅ Combining multiple model fields

**When to Use Model Methods:**
- ✅ Business logic that's used in multiple places
- ✅ Database-level calculations
- ✅ Logic that doesn't depend on request context

**Example:**
```python
# Model method (reusable)
class Student(models.Model):
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

# Serializer method (API-specific)
class StudentSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()
    
    def get_display_name(self, obj):
        # Can access request context
        request = self.context.get('request')
        if request and request.user.is_staff:
            return f"{obj.full_name} (ID: {obj.id})"
        return obj.full_name
```

### Serializer Performance Comparison

**Serializer vs ModelSerializer vs HyperlinkedModelSerializer:**

| Feature | Serializer | ModelSerializer | HyperlinkedModelSerializer |
|---------|-----------|----------------|---------------------------|
| Field Definition | Manual | Auto from model | Auto from model |
| URL Fields | Manual | Primary key | Hyperlinks |
| Code Amount | More | Less | Less |
| Flexibility | High | Medium | Low |
| Use Case | Complex logic | Standard CRUD | RESTful APIs |

---

*This guide covers essential and advanced serializer patterns. Master these for senior Django REST Framework positions.*

