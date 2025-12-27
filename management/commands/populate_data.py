"""
Management Command: Populate Database with Mock Data

This command populates the database with realistic mock data for testing and demonstration.
Like filling a library with books, or a school with students - makes the API more interesting!

Usage:
    python manage.py populate_data
    
Real-life example:
Like a movie set designer - they fill empty rooms with furniture and props
to make it look realistic. This command does the same for your database!
"""

import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from faker import Faker

# Import all models
from basics.models import Student, Course
from intermediate.models import Author, Category, Book, Review
from advanced.models import BlogPost, Comment, UserProfile
from expert.models import Company, Department, Employee, Project, Task
from rest_framework.authtoken.models import Token

fake = Faker()


class Command(BaseCommand):
    help = 'Populate database with realistic mock data for all apps'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--students',
            type=int,
            default=50,
            help='Number of students to create (default: 50)'
        )
        parser.add_argument(
            '--books',
            type=int,
            default=100,
            help='Number of books to create (default: 100)'
        )
        parser.add_argument(
            '--blogposts',
            type=int,
            default=50,
            help='Number of blog posts to create (default: 50)'
        )
        parser.add_argument(
            '--companies',
            type=int,
            default=10,
            help='Number of companies to create (default: 10)'
        )
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🎬 Starting data population...'))
        self.stdout.write('This is like filling an empty city with people, buildings, and activities!')
        
        # Clear existing data (optional - comment out if you want to keep existing data)
        # self.stdout.write('Clearing existing data...')
        # Student.objects.all().delete()
        # Course.objects.all().delete()
        
        # Populate each app
        self.populate_basics(options['students'])
        self.populate_intermediate(options['books'])
        self.populate_advanced(options['blogposts'])
        self.populate_expert(options['companies'])
        
        self.stdout.write(self.style.SUCCESS('\n✅ Data population complete!'))
        self.stdout.write('Your API now has realistic data to work with!')
        self.stdout.write('Visit http://127.0.0.1:8000/api/docs/ to see the Swagger documentation!')
    
    def populate_basics(self, num_students):
        """Populate basics app with students and courses"""
        self.stdout.write('\n📚 Populating Basics App...')
        
        # Create courses first
        course_titles = [
            'Introduction to Python', 'Django Web Development', 'REST API Design',
            'Database Design', 'Frontend Development', 'DevOps Fundamentals',
            'Machine Learning Basics', 'Data Structures', 'Algorithms', 'Software Engineering'
        ]
        
        courses = []
        for title in course_titles:
            course = Course.objects.create(
                title=title,
                description=fake.text(max_nb_chars=200),
                instructor=fake.name(),
                duration_hours=random.randint(20, 80),
                price=random.uniform(49.99, 299.99),
                is_active=random.choice([True, True, True, False])  # Mostly active
            )
            courses.append(course)
            self.stdout.write(f'  ✓ Created course: {title}')
        
        # Create students
        grades = ['A', 'B', 'C', 'D', 'F']
        for i in range(num_students):
            student = Student.objects.create(
                name=fake.name(),
                email=fake.unique.email(),
                age=random.randint(18, 25),
                grade=random.choice(grades)
            )
            if i % 10 == 0:
                self.stdout.write(f'  ✓ Created {i+1} students...')
        
        self.stdout.write(self.style.SUCCESS(f'  ✅ Created {num_students} students and {len(courses)} courses'))
    
    def populate_intermediate(self, num_books):
        """Populate intermediate app with authors, categories, books, and reviews"""
        self.stdout.write('\n📖 Populating Intermediate App...')
        
        # Create categories
        category_names = [
            'Fiction', 'Non-Fiction', 'Science', 'Technology', 'History',
            'Biography', 'Mystery', 'Romance', 'Fantasy', 'Business'
        ]
        categories = []
        for name in category_names:
            category = Category.objects.create(
                name=name,
                description=fake.text(max_nb_chars=100),
                slug=name.lower().replace(' ', '-')
            )
            categories.append(category)
        
        # Create users and authors
        authors = []
        for i in range(20):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password='testpass123'
            )
            author = Author.objects.create(
                user=user,
                bio=fake.text(max_nb_chars=200),
                birth_date=fake.date_of_birth(minimum_age=25, maximum_age=80),
                website=fake.url()
            )
            authors.append(author)
            if i % 5 == 0:
                self.stdout.write(f'  ✓ Created {i+1} authors...')
        
        # Create books
        book_titles = [
            'The Art of Programming', 'Web Development Mastery', 'Data Science Essentials',
            'Cloud Computing Guide', 'Mobile App Development', 'Cybersecurity Fundamentals',
            'AI and Machine Learning', 'Blockchain Technology', 'DevOps Handbook',
            'Software Architecture Patterns'
        ]
        
        books = []
        for i in range(num_books):
            author = random.choice(authors)
            book = Book.objects.create(
                title=random.choice(book_titles) if i < len(book_titles) else fake.sentence(nb_words=4).replace('.', ''),
                description=fake.text(max_nb_chars=500),
                author=author,
                isbn=fake.isbn13(),
                publication_date=fake.date_between(start_date='-10y', end_date='today'),
                price=random.uniform(9.99, 49.99),
                pages=random.randint(100, 800),
                is_available=random.choice([True, True, True, False])
            )
            # Add random categories
            book.categories.add(*random.sample(categories, random.randint(1, 3)))
            books.append(book)
            
            # Create some reviews for each book
            if random.random() > 0.3:  # 70% of books have reviews
                num_reviews = random.randint(1, 5)
                for _ in range(num_reviews):
                    reviewer = User.objects.order_by('?').first()
                    if reviewer:
                        Review.objects.get_or_create(
                            book=book,
                            reviewer=reviewer,
                            defaults={
                                'rating': random.randint(1, 5),
                                'comment': fake.text(max_nb_chars=200)
                            }
                        )
            
            if i % 20 == 0:
                self.stdout.write(f'  ✓ Created {i+1} books...')
        
        self.stdout.write(self.style.SUCCESS(f'  ✅ Created {len(authors)} authors, {len(books)} books, and reviews'))
    
    def populate_advanced(self, num_blogposts):
        """Populate advanced app with blog posts, comments, and user profiles"""
        self.stdout.write('\n✍️  Populating Advanced App...')
        
        # Create users with profiles
        users = []
        for i in range(15):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password='testpass123'
            )
            UserProfile.objects.create(
                user=user,
                bio=fake.text(max_nb_chars=150),
                website=fake.url(),
                location=fake.city(),
                birth_date=fake.date_of_birth(minimum_age=20, maximum_age=60),
                is_verified=random.choice([True, False])
            )
            users.append(user)
            # Create token for some users
            if i < 5:
                Token.objects.get_or_create(user=user)
        
        # Create blog posts
        statuses = ['draft', 'published', 'archived']
        tags_list = [
            'django', 'python', 'rest-api', 'web-development', 'tutorial',
            'programming', 'backend', 'frontend', 'database', 'devops'
        ]
        
        blog_posts = []
        for i in range(num_blogposts):
            author = random.choice(users)
            status = random.choice(statuses)
            published_at = None
            if status == 'published':
                published_at = fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.utc)
            
            post = BlogPost.objects.create(
                title=fake.sentence(nb_words=6).replace('.', ''),
                slug=fake.slug(),
                content=fake.text(max_nb_chars=2000),
                author=author,
                status=status,
                tags=', '.join(random.sample(tags_list, random.randint(2, 5))),
                views_count=random.randint(0, 10000),
                likes_count=random.randint(0, 500),
                is_featured=random.choice([True, False, False, False]),  # 25% featured
                published_at=published_at
            )
            blog_posts.append(post)
            
            # Create comments for published posts
            if status == 'published' and random.random() > 0.4:
                num_comments = random.randint(2, 10)
                for _ in range(num_comments):
                    Comment.objects.create(
                        post=post,
                        author=random.choice(users),
                        content=fake.text(max_nb_chars=300),
                        is_approved=random.choice([True, True, True, False])  # Mostly approved
                    )
            
            if i % 10 == 0:
                self.stdout.write(f'  ✓ Created {i+1} blog posts...')
        
        self.stdout.write(self.style.SUCCESS(f'  ✅ Created {len(users)} users, {len(blog_posts)} blog posts, and comments'))
    
    def populate_expert(self, num_companies):
        """Populate expert app with companies, departments, employees, projects, and tasks"""
        self.stdout.write('\n🏢 Populating Expert App...')
        
        # Create companies
        company_names = [
            'TechCorp Solutions', 'Innovation Labs', 'Digital Dynamics',
            'Cloud Systems Inc', 'Data Analytics Pro', 'Web Services Co',
            'Mobile Apps Ltd', 'AI Innovations', 'Blockchain Tech', 'DevOps Experts'
        ]
        
        companies = []
        for i in range(num_companies):
            name = company_names[i] if i < len(company_names) else fake.company()
            company = Company.objects.create(
                name=name,
                description=fake.text(max_nb_chars=300),
                founded_year=random.randint(2000, 2020),
                headquarters=fake.city(),
                website=fake.url(),
                employee_count=0  # Will update after creating employees
            )
            companies.append(company)
        
        # Create departments and employees for each company
        department_names = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations']
        positions = [
            'Software Engineer', 'Senior Developer', 'Product Manager', 'Designer',
            'Data Analyst', 'DevOps Engineer', 'QA Engineer', 'Team Lead'
        ]
        
        all_employees = []
        for company in companies:
            # Create 2-4 departments per company
            departments = []
            num_depts = random.randint(2, 4)
            for dept_name in random.sample(department_names, num_depts):
                manager_user = User.objects.create_user(
                    username=fake.user_name(),
                    email=fake.email(),
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    password='testpass123'
                )
                dept = Department.objects.create(
                    company=company,
                    name=dept_name,
                    description=fake.text(max_nb_chars=150),
                    budget=random.uniform(100000, 1000000),
                    manager=manager_user
                )
                departments.append(dept)
            
            # Create employees for each department
            for dept in departments:
                num_employees = random.randint(3, 8)
                for j in range(num_employees):
                    user = User.objects.create_user(
                        username=fake.user_name(),
                        email=fake.email(),
                        first_name=fake.first_name(),
                        last_name=fake.last_name(),
                        password='testpass123'
                    )
                    employee = Employee.objects.create(
                        department=dept,
                        user=user,
                        employee_id=f'EMP{company.id:03d}{dept.id:02d}{j+1:03d}',
                        position=random.choice(positions),
                        salary=random.uniform(40000, 150000),
                        hire_date=fake.date_between(start_date='-5y', end_date='today'),
                        is_active=random.choice([True, True, True, False])
                    )
                    all_employees.append(employee)
                    company.employee_count += 1
                company.save()
        
        # Create projects
        project_names = [
            'Website Redesign', 'Mobile App Development', 'API Integration',
            'Cloud Migration', 'Data Analytics Platform', 'E-commerce System',
            'CRM Implementation', 'Security Audit', 'Performance Optimization'
        ]
        
        project_statuses = ['planning', 'active', 'on_hold', 'completed', 'cancelled']
        projects = []
        for company in companies:
            num_projects = random.randint(2, 5)
            for i in range(num_projects):
                dept = random.choice(company.departments.all())
                manager = random.choice([e.user for e in all_employees if e.department == dept] + [None])
                
                project = Project.objects.create(
                    name=random.choice(project_names) if i < len(project_names) else fake.sentence(nb_words=3).replace('.', ''),
                    description=fake.text(max_nb_chars=400),
                    company=company,
                    department=dept,
                    manager=manager,
                    start_date=fake.date_between(start_date='-2y', end_date='today'),
                    end_date=fake.date_between(start_date='today', end_date='+1y') if random.random() > 0.3 else None,
                    budget=random.uniform(50000, 500000),
                    status=random.choice(project_statuses)
                )
                
                # Assign some employees to project
                dept_employees = [e for e in all_employees if e.department == dept]
                if dept_employees:
                    project.employees.add(*random.sample(dept_employees, min(random.randint(2, 5), len(dept_employees))))
                
                # Create tasks for active projects
                if project.status in ['active', 'planning']:
                    task_titles = [
                        'Design database schema', 'Implement authentication', 'Write unit tests',
                        'Create API endpoints', 'Setup CI/CD pipeline', 'Write documentation',
                        'Code review', 'Deploy to staging', 'Performance testing'
                    ]
                    num_tasks = random.randint(3, 8)
                    for j in range(num_tasks):
                        assigned_employee = random.choice(dept_employees) if dept_employees else None
                        Task.objects.create(
                            project=project,
                            title=random.choice(task_titles) if j < len(task_titles) else fake.sentence(nb_words=4).replace('.', '),
                            description=fake.text(max_nb_chars=200),
                            assigned_to=assigned_employee,
                            priority=random.choice(['low', 'medium', 'high', 'critical']),
                            status=random.choice(['todo', 'in_progress', 'review', 'done']),
                            due_date=fake.date_between(start_date='today', end_date='+3m')
                        )
                
                projects.append(project)
        
        self.stdout.write(self.style.SUCCESS(
            f'  ✅ Created {len(companies)} companies, {Department.objects.count()} departments, '
            f'{len(all_employees)} employees, {len(projects)} projects, and tasks'
        ))

