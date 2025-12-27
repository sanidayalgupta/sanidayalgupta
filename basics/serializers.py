"""
BASICS: Serializers - The Data Translators

Think of serializers as translators between two languages:
- Python/Django objects (like a Student model) ↔ JSON (what web browsers understand)

Real-life example:
Imagine you're at a restaurant. The menu (model) is in the kitchen's language (Python).
The waiter (serializer) translates it to your language (JSON) so you can understand it.
When you order, the waiter translates your order back to the kitchen.

Key Concepts:
1. ModelSerializer - Like an automatic translator (does most work for you)
2. Serializer - Like a manual translator (you control everything)
3. Validation - Like a bouncer checking IDs before entry
4. Field types - Different data formats (text, numbers, dates, etc.)
"""

from rest_framework import serializers
from .models import Student, Course


class StudentSerializer(serializers.ModelSerializer):
    """
    ModelSerializer - The Automatic Translator
    
    This is like having a smart assistant that automatically translates
    your Student model into JSON format. You just tell it which fields
    to include, and it handles the rest!
    
    Real-life example:
    Like Google Translate - you give it the source (model) and destination
    format (JSON), and it does the translation automatically.
    """
    class Meta:
        model = Student
        # These are the fields that will be converted to/from JSON
        # Like telling the translator which parts of the document to translate
        fields = ['id', 'name', 'email', 'age', 'grade', 'created_at', 'updated_at']
        # Read-only fields are like "display only" - can see but can't change
        # Like a museum exhibit - you can look but can't touch
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_age(self, value):
        """
        Custom validation for age - The Age Checker
        
        This is like a bouncer at a club checking if you're old enough.
        If age is not between 5 and 100, it rejects the entry.
        
        Real-life example:
        Like a website asking "Are you 18+?" - it validates before allowing access.
        """
        if value < 5 or value > 100:
            raise serializers.ValidationError("Age must be between 5 and 100")
        return value
    
    def validate_email(self, value):
        """
        Custom validation for email - The Duplicate Checker
        
        This checks if someone else already used this email.
        Like checking if a username is already taken when signing up.
        
        Real-life example:
        When you try to create a Gmail account, it checks if the email
        is already in use. Same concept here!
        """
        if Student.objects.filter(email=value).exists() and self.instance is None:
            raise serializers.ValidationError("A student with this email already exists.")
        return value


class CourseSerializer(serializers.ModelSerializer):
    """
    Course Serializer - Another Automatic Translator Example
    
    This one uses '__all__' which means "translate everything from the model".
    Like saying "translate the entire document" instead of specific pages.
    
    Real-life example:
    Like a photocopier that copies the entire document automatically,
    instead of selecting specific pages.
    """
    class Meta:
        model = Course
        fields = '__all__'  # Include all model fields - like "translate everything"
        read_only_fields = ['id', 'created_at']


class StudentManualSerializer(serializers.Serializer):
    """
    Manual Serializer - The Custom Translator
    
    This is like hiring a professional translator who translates word-by-word
    exactly how you want. You have full control over every detail.
    
    Use this when you need:
    - Fields not in the model (like calculated fields)
    - Complex validation logic (like checking multiple conditions)
    - Custom serialization (like formatting dates in a specific way)
    
    Real-life example:
    Like a legal document translator - you need precise control over
    every word, not automatic translation.
    """
    # Define each field manually - like specifying each word to translate
    name = serializers.CharField(max_length=100)  # Text field, max 100 characters
    email = serializers.EmailField()  # Must be a valid email format
    age = serializers.IntegerField(min_value=5, max_value=100)  # Number between 5-100
    grade = serializers.CharField(max_length=10)  # Text field, max 10 characters
    
    def create(self, validated_data):
        """
        Create a new Student - The Birth Certificate Maker
        
        This method creates a new student record in the database.
        Like filling out a birth certificate - you provide the information,
        and it creates the official record.
        
        Real-life example:
        Like registering a new user account - you provide details,
        and the system creates your profile.
        """
        return Student.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update existing Student - The Record Updater
        
        This method updates an existing student's information.
        Like updating your driver's license when you move - you keep
        the same ID but change the address.
        
        Real-life example:
        Like editing your Facebook profile - you update some fields
        but keep your account the same.
        """
        # Only update fields that are provided (like only changing what you want)
        instance.name = validated_data.get('name', instance.name)  # If new name provided, use it; otherwise keep old
        instance.email = validated_data.get('email', instance.email)
        instance.age = validated_data.get('age', instance.age)
        instance.grade = validated_data.get('grade', instance.grade)
        instance.save()  # Save changes to database
        return instance
    
    def validate(self, data):
        """
        Object-level validation - The Final Checker
        
        This validates the entire object, not just individual fields.
        Like a final inspection before approving something - checks
        if everything makes sense together.
        
        Real-life example:
        Like a loan application - they check individual details (income, credit score)
        AND the overall picture (does it all make sense together?).
        """
        # Check if student is under 18 AND doesn't have grade A or B
        # Like a rule: "Minors must have good grades"
        if data.get('age', 0) < 18 and data.get('grade', '') not in ['A', 'B']:
            raise serializers.ValidationError(
                "Students under 18 must have grade A or B"
            )
        return data

