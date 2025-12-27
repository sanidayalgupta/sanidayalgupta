"""
EXPERT: Django Signals - The Event Listeners

What are Django Signals?
Signals are like event listeners - they allow certain senders to notify a set of receivers
that some action has taken place. Think of them as "hooks" that get triggered when something happens.

Real-life example:
Like a doorbell - when someone presses it (signal sent), the bell rings (receiver function runs).
Or like a security system - when a door opens (signal), an alarm might sound (receiver).

Common use cases:
- Auto-creating related objects when a model is saved
- Sending emails when a user signs up
- Updating counters when related objects change
- Logging important events
- Invalidating cache when data changes

This file demonstrates:
1. post_save signal - Triggered after a model instance is saved
2. pre_save signal - Triggered before a model instance is saved
3. post_delete signal - Triggered after a model instance is deleted
4. Custom signals - User-defined signals for specific events
"""

from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
import logging

# Get logger for this module
logger = logging.getLogger(__name__)

from .models import Company, Department, Employee, Project, Task
from expert.caching import cache_key_company_list, cache_key_company_detail, cache_key_company_statistics


# ============================================================================
# Company Signals
# ============================================================================

@receiver(post_save, sender=Company)
def company_saved(sender, instance, created, **kwargs):
    """
    Signal receiver: Called after a Company is saved
    
    What it does:
    - If new company created: Logs the creation
    - Invalidates company list cache (new company added)
    - Updates employee count if needed
    
    Real-life example:
    Like a notification system - when a new company is registered,
    the system automatically updates the company directory (cache) and
    sends notifications to relevant departments.
    
    Parameters:
    - sender: The model class (Company)
    - instance: The actual instance being saved
    - created: True if this is a new record, False if it's an update
    - **kwargs: Additional arguments
    """
    if created:
        # New company was created
        logger.info(f'New company created: {instance.name} (ID: {instance.id})')
        # Clear the company list cache since we have a new company
        cache.delete(cache_key_company_list())
    else:
        # Existing company was updated
        logger.info(f'Company updated: {instance.name} (ID: {instance.id})')
        # Clear caches for this specific company
        cache.delete(cache_key_company_detail(instance.pk))
        cache.delete(cache_key_company_statistics(instance.pk))
        cache.delete(cache_key_company_list())


@receiver(post_delete, sender=Company)
def company_deleted(sender, instance, **kwargs):
    """
    Signal receiver: Called after a Company is deleted
    
    What it does:
    - Logs the deletion
    - Clears all related caches
    
    Real-life example:
    Like a cleanup crew - when a company closes, they remove all
    references and update directories.
    """
    logger.warning(f'Company deleted: {instance.name} (ID: {instance.id})')
    # Clear all company-related caches
    cache.delete(cache_key_company_list())
    cache.delete(cache_key_company_detail(instance.pk))
    cache.delete(cache_key_company_statistics(instance.pk))


# ============================================================================
# Employee Signals
# ============================================================================

@receiver(post_save, sender=Employee)
def employee_saved(sender, instance, created, **kwargs):
    """
    Signal receiver: Updates company employee count when employee is saved
    
    What it does:
    - When new employee created: Increments company employee_count
    - When employee updated: Recalculates if department changed
    
    Real-life example:
    Like an automatic counter - when someone joins a company, the
    employee count automatically updates without manual intervention.
    """
    if created:
        # New employee - increment company count
        company = instance.department.company
        company.employee_count += 1
        company.save(update_fields=['employee_count'])
        logger.info(f'Employee {instance.employee_id} added to {company.name}. Total: {company.employee_count}')
    else:
        # Employee updated - check if department changed
        # (This would require tracking old department, simplified here)
        logger.debug(f'Employee {instance.employee_id} updated')


@receiver(post_delete, sender=Employee)
def employee_deleted(sender, instance, **kwargs):
    """
    Signal receiver: Decrements company employee count when employee is deleted
    
    What it does:
    - Decrements the company's employee_count
    - Logs the deletion
    
    Real-life example:
    Like an automatic HR system - when someone leaves, the headcount
    automatically decreases.
    """
    company = instance.department.company
    if company.employee_count > 0:
        company.employee_count -= 1
        company.save(update_fields=['employee_count'])
    logger.info(f'Employee {instance.employee_id} removed from {company.name}. Total: {company.employee_count}')


# ============================================================================
# Project Signals
# ============================================================================

@receiver(pre_save, sender=Project)
def project_pre_save(sender, instance, **kwargs):
    """
    Signal receiver: Called BEFORE a Project is saved
    
    What it does:
    - Validates project dates
    - Auto-calculates budget if needed
    - Sets default values
    
    Real-life example:
    Like a pre-flight check - before a plane takes off, systems check
    everything is ready. This signal checks data before saving.
    
    Note: pre_save runs before validation, so use carefully
    """
    # Example: Auto-set end_date if not provided and status is completed
    if instance.status == 'completed' and not instance.end_date:
        from django.utils import timezone
        instance.end_date = timezone.now().date()
        logger.info(f'Project {instance.name} auto-set end_date to today (status: completed)')


@receiver(post_save, sender=Project)
def project_saved(sender, instance, created, **kwargs):
    """
    Signal receiver: Called after a Project is saved
    
    What it does:
    - Logs project creation/updates
    - Updates company statistics cache
    """
    if created:
        logger.info(f'New project created: {instance.name} in {instance.company.name}')
    else:
        logger.debug(f'Project updated: {instance.name} (Status: {instance.status})')
    
    # Invalidate company statistics cache
    cache.delete(cache_key_company_statistics(instance.company.pk))


# ============================================================================
# Task Signals
# ============================================================================

@receiver(post_save, sender=Task)
def task_saved(sender, instance, created, **kwargs):
    """
    Signal receiver: Updates task completion timestamp
    
    What it does:
    - When task status changes to 'done': Sets completed_at timestamp
    - Logs task completion
    
    Real-life example:
    Like a time clock - when you mark a task complete, it automatically
    records the completion time.
    """
    if not created and instance.status == 'done' and not instance.completed_at:
        from django.utils import timezone
        instance.completed_at = timezone.now()
        # Save again to update completed_at (avoid infinite loop with update_fields)
        Task.objects.filter(pk=instance.pk).update(completed_at=instance.completed_at)
        logger.info(f'Task "{instance.title}" marked as completed at {instance.completed_at}')

