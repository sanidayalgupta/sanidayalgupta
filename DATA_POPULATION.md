# Data Population Guide

## 📊 Mock Data Generator

The project includes a management command to populate the database with realistic mock data,
similar to what Mockaroo provides, but integrated directly into Django.

## 🚀 Usage

### Basic Usage
```bash
python manage.py populate_data
```

This creates default amounts:
- 50 students
- 100 books
- 50 blog posts
- 10 companies

### Custom Amounts
```bash
python manage.py populate_data --students 100 --books 200 --blogposts 50 --companies 10
```

### Options
- `--students` - Number of students to create (default: 50)
- `--books` - Number of books to create (default: 100)
- `--blogposts` - Number of blog posts to create (default: 50)
- `--companies` - Number of companies to create (default: 10)

## 📦 What Gets Created

### Basics App
- **Students**: Random names, emails, ages, grades
- **Courses**: 10 predefined courses with descriptions, prices, durations

### Intermediate App
- **Categories**: 10 book categories (Fiction, Science, etc.)
- **Authors**: 20 authors with bios and websites
- **Books**: Books with ISBNs, prices, publication dates
- **Reviews**: Reviews for 70% of books (1-5 reviews each)

### Advanced App
- **Users**: 15 users with profiles
- **User Profiles**: Bios, websites, locations, verification status
- **Blog Posts**: Posts with different statuses (draft, published, archived)
- **Comments**: Comments on published posts (2-10 per post)
- **Tokens**: API tokens for first 5 users

### Expert App
- **Companies**: Companies with descriptions, headquarters, websites
- **Departments**: 2-4 departments per company (Engineering, Sales, etc.)
- **Employees**: 3-8 employees per department with positions and salaries
- **Projects**: 2-5 projects per company with budgets and statuses
- **Tasks**: 3-8 tasks per active project with priorities and due dates

## 🎲 Data Characteristics

### Realistic Data
All data is generated using **Faker** library, which creates:
- Realistic names, emails, addresses
- Proper date ranges
- Logical relationships
- Varied statuses and states

### Relationships
- Books are linked to authors and categories
- Reviews are linked to books and users
- Employees belong to departments
- Projects have tasks and assigned employees
- Comments belong to blog posts

### Variety
- Different statuses (active/inactive, published/draft)
- Various dates (past, present, future)
- Random ratings and counts
- Mixed approval states

## 🔄 Re-running

The command uses `get_or_create` for categories to avoid duplicates.
For other data, you can:
1. Clear existing data manually
2. Run the command again (will create more)
3. Use Django admin to manage data

## 📝 Example Output

```
Starting data population...
This is like filling an empty city with people, buildings, and activities!

[Basics] Populating Basics App...
  [OK] Created course: Introduction to Python
  [OK] Created course: Django Web Development
  ...
  [OK] Created 30 students and 10 courses

[Intermediate] Populating Intermediate App...
  [OK] Created 20 authors, 50 books, and reviews

[Advanced] Populating Advanced App...
  [OK] Created 15 users, 30 blog posts, and comments

[Expert] Populating Expert App...
  [OK] Created 5 companies, 14 departments, 82 employees, 18 projects, and tasks

[SUCCESS] Data population complete!
```

## 🎯 Use Cases

### Development
- Test API endpoints with realistic data
- See pagination in action
- Test filtering and searching
- Verify relationships work

### Learning
- Understand data structures
- See how relationships work
- Test different scenarios
- Explore API responses

### Demonstration
- Show API capabilities
- Demonstrate features
- Show realistic examples
- Test Swagger documentation

## 💡 Tips

1. **Start Small**: Use default amounts first, then increase if needed
2. **Check Swagger**: After populating, check Swagger docs to see the data
3. **Test Endpoints**: Use the populated data to test all endpoints
4. **Explore Relationships**: See how nested serializers work with real data
5. **Filter & Search**: Test filtering with the variety of data created

## 🔧 Customization

To customize the data generation, edit:
`basics/management/commands/populate_data.py`

You can:
- Change data ranges (ages, prices, dates)
- Add more categories or types
- Modify relationships
- Adjust variety and randomness

---

**Ready to populate?** Run:
```bash
python manage.py populate_data
```

Then visit http://127.0.0.1:8000/api/docs/ to see your data in action! 🚀

