"""
EXPERT: Multiple Database Handling - The Database Router

What is Multiple Database Handling?
Multiple database handling allows you to use more than one database in a Django project.
Different models can be stored in different databases, or you can route read/write operations
to different databases for performance or organizational reasons.

Real-life example:
Like a company with multiple warehouses:
- Main warehouse (default DB) - stores most products
- Archive warehouse (archive DB) - stores old/rarely accessed items
- Analytics warehouse (analytics DB) - stores reports and statistics

This router demonstrates:
1. Database routing - Deciding which database to use
2. Read/write splitting - Reads from one DB, writes to another
3. Model-specific routing - Different models in different DBs
4. Migration handling - Which DB to migrate

Use cases:
- Separating user data from analytics data
- Using read replicas for better performance
- Archiving old data to separate database
- Multi-tenant applications
"""


class ExpertDatabaseRouter:
    """
    Database Router for Expert App - Routes models to appropriate databases
    
    What it does:
    This router decides which database should be used for each model and operation.
    Think of it as a traffic director - it tells each request which database to use.
    
    Real-life example:
    Like a postal sorting system - letters go to different sorting centers
    based on their destination. This router sends database operations to
    different databases based on the model.
    """
    
    # Define which models should use which database
    # This is like a routing table - tells the system where to send each model
    expert_models = {
        'company',
        'department',
        'employee',
        'project',
        'task'
    }
    
    def db_for_read(self, model, **hints):
        """
        Suggest which database should be used for read operations
        
        What it does:
        Returns the database name to use for reading data from this model.
        If None, uses the default database.
        
        Real-life example:
        Like a librarian - when you ask for a book, they know which section
        (database) to look in.
        
        Parameters:
        - model: The model class being queried
        - **hints: Additional hints about the operation
        
        Returns:
        - Database name (string) or None for default
        """
        # Example: Route expert models to a separate database
        # In production, you might route to a read replica for performance
        if model._meta.app_label == 'expert':
            # Uncomment to use separate database for expert app:
            # return 'expert_db'
            pass
        
        # Return None to use default database
        return None
    
    def db_for_write(self, model, **hints):
        """
        Suggest which database should be used for write operations
        
        What it does:
        Returns the database name to use for writing data to this model.
        This is where you'd implement write/read splitting.
        
        Real-life example:
        Like a filing system - when you need to file a document, you know
        which filing cabinet (database) to put it in.
        
        Parameters:
        - model: The model class being written to
        - **hints: Additional hints about the operation
        
        Returns:
        - Database name (string) or None for default
        """
        # Example: Route expert models to separate database
        if model._meta.app_label == 'expert':
            # Uncomment to use separate database:
            # return 'expert_db'
            pass
        
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        """
        Determine if a relationship between two objects should be allowed
        
        What it does:
        Returns True if relations between obj1 and obj2 should be allowed,
        False if the relation should be prevented, or None if the router
        has no opinion.
        
        Real-life example:
        Like a security guard - they decide if two people (objects) can
        interact with each other, even if they're in different areas (databases).
        
        Parameters:
        - obj1: First model instance
        - obj2: Second model instance
        - **hints: Additional hints
        
        Returns:
        - True/False/None
        """
        # Allow relations if both objects are in the same app
        if obj1._meta.app_label == obj2._meta.app_label:
            return True
        
        # Allow relations between expert and other apps (if needed)
        if obj1._meta.app_label == 'expert' or obj2._meta.app_label == 'expert':
            return True
        
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Determine if migrations should be run on a database
        
        What it does:
        Returns True if the migration operation should be run on the database,
        False if it should be skipped, or None if the router has no opinion.
        
        Real-life example:
        Like a construction manager - they decide which buildings (databases)
        need which renovations (migrations).
        
        Parameters:
        - db: Database alias
        - app_label: Name of the app
        - model_name: Name of the model (optional)
        - **hints: Additional hints
        
        Returns:
        - True/False/None
        """
        # Run expert app migrations on expert database (if it exists)
        if app_label == 'expert':
            # If expert_db exists, run migrations there
            # Otherwise, use default
            # return db == 'expert_db' or db == 'default'
            return db == 'default'
        
        # Other apps use default database
        if db == 'default':
            return True
        
        return None


# ============================================================================
# Example: Using Multiple Databases in Settings
# ============================================================================
"""
To use multiple databases, add this to settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'expert_db': {  # Separate database for expert app
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'expert_db.sqlite3',
    },
    'analytics_db': {  # Read-only replica for analytics
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'analytics',
        'USER': 'analytics_user',
        'PASSWORD': 'password',
        'HOST': 'analytics-server.example.com',
        'OPTIONS': {
            'options': '-c default_transaction_isolation=read committed'
        }
    }
}

# Add router to settings
DATABASE_ROUTERS = ['expert.database_router.ExpertDatabaseRouter']

# Then use in code:
# Company.objects.using('expert_db').all()  # Explicit database
# Company.objects.all()  # Uses router to decide
"""

