"""
EXPERT: Context Managers - The Resource Managers

What are Context Managers?
Context managers are Python objects that define what happens when you enter and exit
a block of code using the `with` statement. They ensure proper setup and cleanup,
even if an error occurs.

Real-life example:
Like a library - when you enter (with statement starts), you get a book.
When you leave (with statement ends), you return it, even if something goes wrong.
Or like a safe - you open it (enter), do your work, and it automatically closes (exit).

Benefits:
- Automatic cleanup (like closing files, releasing locks)
- Exception safety (cleanup happens even if errors occur)
- Resource management (database connections, transactions)
- Code organization (clear setup/teardown)

This file demonstrates:
1. Custom context managers using class-based approach
2. Context managers using contextlib
3. Transaction context managers
4. Timing context managers
5. Logging context managers
"""

from contextlib import contextmanager
from django.db import transaction
import time
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# Class-based Context Manager
# ============================================================================

class DatabaseTransactionContext:
    """
    Context Manager: Ensures database operations happen in a transaction
    
    What it does:
    Wraps code in a database transaction. If code succeeds, commits.
    If an error occurs, rolls back automatically.
    
    Real-life example:
    Like a safety net - if anything goes wrong during your work,
    everything is undone (rolled back). If everything succeeds,
    changes are saved (committed).
    
    Usage:
        with DatabaseTransactionContext():
            # All database operations here are in one transaction
            employee1.save()
            employee2.save()
            # If any fails, both are rolled back
    
    Note: For most cases, use transaction.atomic() directly.
    This is a demonstration of custom context managers.
    """
    
    def __enter__(self):
        """
        Called when entering the 'with' block
        
        What it does:
        Starts a database transaction using transaction.atomic().
        This is like opening a safe - you're now inside and can make changes.
        """
        logger.debug('Starting database transaction')
        # Use transaction.atomic() which handles nesting properly
        self.atomic = transaction.atomic()
        return self.atomic.__enter__()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Called when exiting the 'with' block
        
        What it does:
        - If no error (exc_type is None): Commits the transaction
        - If error occurred: Rolls back the transaction
        This is like closing the safe - either save changes or discard them.
        
        Parameters:
        - exc_type: Exception type (None if no error)
        - exc_val: Exception value
        - exc_tb: Exception traceback
        
        Returns:
        - False: Re-raise the exception
        - True: Suppress the exception
        """
        result = self.atomic.__exit__(exc_type, exc_val, exc_tb)
        if exc_type is None:
            logger.debug('Transaction committed successfully')
        else:
            logger.error(f'Transaction rolled back due to error: {exc_type.__name__}')
        return result


# ============================================================================
# Function-based Context Manager (using contextlib)
# ============================================================================

@contextmanager
def timing_context(operation_name):
    """
    Context Manager: Measures how long code takes to execute
    
    What it does:
    Records the start time, executes code, then logs the duration.
    Useful for performance monitoring.
    
    Real-life example:
    Like a stopwatch - you start it, do something, and it tells you
    how long it took. Useful for tracking performance.
    
    Usage:
        with timing_context('create_employees'):
            # Code to measure
            create_multiple_employees()
        # Automatically logs: "create_employees took 2.5 seconds"
    """
    start_time = time.time()
    logger.info(f'Starting operation: {operation_name}')
    
    try:
        yield  # This is where your code executes
    finally:
        # This always runs, even if there's an error
        duration = time.time() - start_time
        logger.info(f'Operation "{operation_name}" completed in {duration:.2f} seconds')


@contextmanager
def cache_invalidation_context(cache_keys):
    """
    Context Manager: Invalidates cache keys after code execution
    
    What it does:
    Executes code, then invalidates specified cache keys.
    Ensures cache is cleared even if errors occur.
    
    Real-life example:
    Like a cleanup crew - after you finish work, they automatically
    clean up (invalidate cache), even if something went wrong.
    
    Usage:
        with cache_invalidation_context(['company_list', 'company_1']):
            # Modify company data
            company.save()
        # Cache automatically cleared after
    """
    try:
        yield  # Execute your code
    finally:
        # Always clear cache, even if error occurred
        from django.core.cache import cache
        for key in cache_keys:
            cache.delete(key)
            logger.debug(f'Cache key invalidated: {key}')


@contextmanager
def logging_context(operation_name, log_level=logging.INFO):
    """
    Context Manager: Adds structured logging around code execution
    
    What it does:
    Logs when operation starts, executes code, logs when it completes.
    If error occurs, logs the error.
    
    Real-life example:
    Like a security camera - it records when you enter (start),
    what happens (execution), and when you leave (end or error).
    
    Usage:
        with logging_context('bulk_create_employees'):
            # Your code here
            create_employees()
        # Logs: "Starting bulk_create_employees" and "Completed bulk_create_employees"
    """
    logger.log(log_level, f'[START] {operation_name}')
    start_time = time.time()
    
    try:
        yield
        duration = time.time() - start_time
        logger.log(log_level, f'[SUCCESS] {operation_name} completed in {duration:.2f}s')
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f'[ERROR] {operation_name} failed after {duration:.2f}s: {str(e)}', exc_info=True)
        raise  # Re-raise the exception


# ============================================================================
# Advanced: Nested Context Managers
# ============================================================================

@contextmanager
def transaction_with_timing(operation_name):
    """
    Context Manager: Combines transaction and timing
    
    What it does:
    Wraps code in a transaction AND measures execution time.
    Demonstrates combining multiple context managers.
    
    Real-life example:
    Like a comprehensive monitoring system - it both ensures data safety
    (transaction) and tracks performance (timing).
    
    Usage:
        with transaction_with_timing('create_project_with_tasks'):
            project = Project.objects.create(...)
            for task in tasks:
                Task.objects.create(project=project, ...)
        # Transaction committed AND timing logged
    
    Note: Use transaction.atomic() directly for nested transactions instead
    """
    # Use transaction.atomic() instead of custom context to avoid nesting issues
    with transaction.atomic():
        with timing_context(operation_name):
            yield


# ============================================================================
# Example Usage in Views
# ============================================================================
"""
Example: Using context managers in a view

from expert.context_managers import (
    DatabaseTransactionContext,
    timing_context,
    cache_invalidation_context,
    logging_context
)

class ProjectViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        # Combine multiple context managers
        with logging_context('create_project'), \
             timing_context('project_creation'), \
             DatabaseTransactionContext():
            
            # Create project
            project = Project.objects.create(...)
            
            # Create tasks
            for task_data in tasks_data:
                Task.objects.create(project=project, ...)
            
            # If anything fails, transaction rolls back automatically
            # Timing and logging still happen
        
        # Invalidate cache after successful creation
        with cache_invalidation_context(['project_list', f'project_{project.id}']):
            pass  # Cache already invalidated in finally block
        
        return Response(serializer.data)
"""

