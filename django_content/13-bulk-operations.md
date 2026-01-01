# Bulk Operations

## 📦 Bulk Operations in DRF

### What are Bulk Operations?

**Definition:** Bulk operations allow creating, updating, or deleting multiple objects in a single API request.

**Real-life example:**
Like buying multiple items at once instead of one transaction per item - more efficient.

### Bulk Create APIs

**Definition:** Creating multiple objects in one request.

**Basic Bulk Create:**
```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    @action(detail=False, methods=['post'], url_path='bulk-create')
    def bulk_create(self, request):
        """Bulk create students"""
        serializer = StudentSerializer(data=request.data, many=True)
        if serializer.is_valid():
            with transaction.atomic():
                students = serializer.save()
            return Response(
                StudentSerializer(students, many=True).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

**Using bulk_create() for Performance:**
```python
from django.db import transaction

class StudentBulkCreateView(APIView):
    def post(self, request):
        """Bulk create using bulk_create() for better performance"""
        students_data = request.data
        
        # Validate all data first
        serializer = StudentSerializer(data=students_data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Create objects
        students = [
            Student(**data) for data in serializer.validated_data
        ]
        
        with transaction.atomic():
            created_students = Student.objects.bulk_create(students)
        
        return Response(
            StudentSerializer(created_students, many=True).data,
            status=status.HTTP_201_CREATED
        )
```

**Real Project Example:**
```python
class OrderItemBulkCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, order_id):
        """Bulk create order items"""
        order = Order.objects.get(id=order_id)
        
        items_data = request.data.get('items', [])
        serializer = OrderItemSerializer(data=items_data, many=True)
        
        if serializer.is_valid():
            items = [
                OrderItem(order=order, **item_data)
                for item_data in serializer.validated_data
            ]
            
            with transaction.atomic():
                created_items = OrderItem.objects.bulk_create(items)
                # Recalculate order total
                order.total = sum(item.price * item.quantity for item in created_items)
                order.save()
            
            return Response(
                OrderItemSerializer(created_items, many=True).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### Bulk Update APIs

**Definition:** Updating multiple objects in one request.

**Basic Bulk Update:**
```python
class StudentViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['put', 'patch'], url_path='bulk-update')
    def bulk_update(self, request):
        """Bulk update students"""
        students_data = request.data  # List of student data with IDs
        
        # Get IDs
        ids = [item.get('id') for item in students_data]
        students = Student.objects.filter(id__in=ids)
        
        # Update each student
        updated_students = []
        with transaction.atomic():
            for student_data in students_data:
                student_id = student_data.pop('id')
                student = students.get(id=student_id)
                serializer = StudentSerializer(
                    student,
                    data=student_data,
                    partial=True
                )
                if serializer.is_valid():
                    updated_student = serializer.save()
                    updated_students.append(updated_student)
                else:
                    return Response(
                        {'id': student_id, 'errors': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        
        return Response(
            StudentSerializer(updated_students, many=True).data,
            status=status.HTTP_200_OK
        )
```

**Using bulk_update() for Performance:**
```python
from django.db import transaction

class StudentBulkUpdateView(APIView):
    def patch(self, request):
        """Bulk update using bulk_update()"""
        updates_data = request.data  # [{'id': 1, 'field': 'value'}, ...]
        
        # Validate all updates
        students_to_update = []
        ids = [item['id'] for item in updates_data]
        students = {s.id: s for s in Student.objects.filter(id__in=ids)}
        
        for update_data in updates_data:
            student_id = update_data.pop('id')
            student = students.get(student_id)
            if not student:
                return Response(
                    {'error': f'Student {student_id} not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Update fields
            for field, value in update_data.items():
                setattr(student, field, value)
            students_to_update.append(student)
        
        with transaction.atomic():
            Student.objects.bulk_update(
                students_to_update,
                fields=[field for field in updates_data[0].keys() if field != 'id']
            )
        
        return Response(
            StudentSerializer(students_to_update, many=True).data,
            status=status.HTTP_200_OK
        )
```

### Upsert APIs (Create or Update)

**Definition:** Upsert creates objects if they don't exist, or updates them if they do.

**Basic Upsert:**
```python
class StudentUpsertView(APIView):
    def post(self, request):
        """Create or update students"""
        students_data = request.data
        
        results = {'created': [], 'updated': []}
        
        with transaction.atomic():
            for student_data in students_data:
                student_id = student_data.get('id')
                
                if student_id:
                    # Update existing
                    try:
                        student = Student.objects.get(id=student_id)
                        serializer = StudentSerializer(
                            student,
                            data=student_data,
                            partial=True
                        )
                        if serializer.is_valid():
                            updated_student = serializer.save()
                            results['updated'].append(updated_student.id)
                    except Student.DoesNotExist:
                        return Response(
                            {'error': f'Student {student_id} not found'},
                            status=status.HTTP_404_NOT_FOUND
                        )
                else:
                    # Create new
                    serializer = StudentSerializer(data=student_data)
                    if serializer.is_valid():
                        created_student = serializer.save()
                        results['created'].append(created_student.id)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(results, status=status.HTTP_200_OK)
```

**Using update_or_create():**
```python
class StudentUpsertView(APIView):
    def post(self, request):
        """Upsert using update_or_create()"""
        students_data = request.data
        results = []
        
        with transaction.atomic():
            for student_data in students_data:
                # Use email as unique identifier
                email = student_data.pop('email')
                student, created = Student.objects.update_or_create(
                    email=email,
                    defaults=student_data
                )
                results.append({
                    'id': student.id,
                    'created': created,
                    'updated': not created
                })
        
        return Response(results, status=status.HTTP_200_OK)
```

### Partial Updates

**Definition:** Partial updates allow updating only specified fields (covered in PATCH method, but here's bulk version).

**Bulk Partial Update:**
```python
class StudentBulkPartialUpdateView(APIView):
    def patch(self, request):
        """Bulk partial update - only update provided fields"""
        updates = request.data  # [{'id': 1, 'age': 25}, {'id': 2, 'grade': 'A'}]
        
        ids = [item['id'] for item in updates]
        students = Student.objects.filter(id__in=ids)
        
        updated_students = []
        with transaction.atomic():
            for update_data in updates:
                student_id = update_data.pop('id')
                student = students.get(id=student_id)
                
                # Update only provided fields
                for field, value in update_data.items():
                    setattr(student, field, value)
                student.save()
                updated_students.append(student)
        
        return Response(
            StudentSerializer(updated_students, many=True).data,
            status=status.HTTP_200_OK
        )
```

### Soft Delete

**Definition:** Soft delete marks objects as deleted without actually removing them from the database.

**Implementation:**
```python
# models.py
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-id']
    
    def soft_delete(self):
        """Soft delete this object"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
    
    class Manager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_deleted=False)
    
    objects = Manager()
    all_objects = models.Manager()  # Access all objects including deleted

# views.py
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()  # Automatically excludes deleted
    serializer_class = StudentSerializer
    
    def perform_destroy(self, instance):
        """Override to use soft delete"""
        instance.soft_delete()
    
    @action(detail=False, methods=['post'], url_path='bulk-delete')
    def bulk_soft_delete(self, request):
        """Bulk soft delete"""
        ids = request.data.get('ids', [])
        
        with transaction.atomic():
            Student.objects.filter(id__in=ids).update(
                is_deleted=True,
                deleted_at=timezone.now()
            )
        
        return Response(
            {'deleted_count': len(ids)},
            status=status.HTTP_200_OK
        )
```

### Hard Delete

**Definition:** Hard delete permanently removes objects from the database.

**Bulk Hard Delete:**
```python
class StudentViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['delete'], url_path='bulk-delete-permanent')
    def bulk_hard_delete(self, request):
        """Bulk hard delete (permanent)"""
        ids = request.data.get('ids', [])
        
        with transaction.atomic():
            deleted_count, _ = Student.objects.filter(id__in=ids).delete()
        
        return Response(
            {'deleted_count': deleted_count},
            status=status.HTTP_204_NO_CONTENT
        )
```

### Restore APIs

**Definition:** Restore APIs recover soft-deleted objects.

**Implementation:**
```python
class StudentViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['post'], url_path='restore')
    def restore(self, request, pk=None):
        """Restore a soft-deleted student"""
        student = Student.all_objects.get(id=pk, is_deleted=True)
        student.is_deleted = False
        student.deleted_at = None
        student.save()
        
        return Response(
            StudentSerializer(student).data,
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['post'], url_path='bulk-restore')
    def bulk_restore(self, request):
        """Bulk restore soft-deleted students"""
        ids = request.data.get('ids', [])
        
        with transaction.atomic():
            restored = Student.all_objects.filter(
                id__in=ids,
                is_deleted=True
            ).update(
                is_deleted=False,
                deleted_at=None
            )
        
        return Response(
            {'restored_count': restored},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'], url_path='deleted')
    def list_deleted(self, request):
        """List soft-deleted students"""
        deleted_students = Student.all_objects.filter(is_deleted=True)
        serializer = StudentSerializer(deleted_students, many=True)
        return Response(serializer.data)
```

### Complete Example

**Real Project Example:**
```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'], url_path='bulk-create')
    def bulk_create(self, request):
        """Bulk create products"""
        serializer = ProductSerializer(data=request.data, many=True)
        if serializer.is_valid():
            with transaction.atomic():
                products = serializer.save(created_by=request.user)
            return Response(
                ProductSerializer(products, many=True).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['patch'], url_path='bulk-update')
    def bulk_update(self, request):
        """Bulk update products"""
        updates = request.data
        ids = [item['id'] for item in updates]
        products = Product.objects.filter(id__in=ids)
        
        updated_products = []
        with transaction.atomic():
            for update_data in updates:
                product_id = update_data.pop('id')
                product = products.get(id=product_id)
                serializer = ProductSerializer(product, data=update_data, partial=True)
                if serializer.is_valid():
                    updated_product = serializer.save(updated_by=request.user)
                    updated_products.append(updated_product)
                else:
                    return Response(
                        {'id': product_id, 'errors': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        
        return Response(
            ProductSerializer(updated_products, many=True).data,
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['post'], url_path='bulk-delete')
    def bulk_delete(self, request):
        """Bulk soft delete products"""
        ids = request.data.get('ids', [])
        with transaction.atomic():
            Product.objects.filter(id__in=ids).update(
                is_deleted=True,
                deleted_at=timezone.now(),
                deleted_by=request.user
            )
        return Response({'deleted_count': len(ids)}, status=status.HTTP_200_OK)
```

### Best Practices

1. **Use transactions:** Ensure atomicity
2. **Validate all data first:** Check before creating/updating
3. **Use bulk_create/bulk_update:** Better performance for large datasets
4. **Limit batch size:** Prevent timeouts on large batches
5. **Return meaningful responses:** Include created/updated/deleted counts
6. **Handle errors gracefully:** Provide clear error messages
7. **Use soft delete:** Easier to recover from mistakes
8. **Add permissions:** Control who can perform bulk operations

