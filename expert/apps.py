"""
EXPERT APP CONFIGURATION

What is AppConfig?
AppConfig is Django's way of configuring an application. It's like a settings file
for your app that runs when Django starts up.

Real-life example:
Like a startup checklist - when a company (Django) starts, each department (app)
has its own setup procedures (AppConfig) that need to run.
"""

from django.apps import AppConfig


class ExpertConfig(AppConfig):
    """
    Configuration for the Expert app
    
    What it does:
    - Sets the default auto field type for models
    - Defines the app name
    - Registers signals when app is ready
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'expert'
    
    def ready(self):
        """
        Called when Django starts and the app is ready
        
        What it does:
        Imports and registers signal handlers. This ensures signals are
        connected when the app loads.
        
        Real-life example:
        Like plugging in devices when you start your computer - signals
        need to be "plugged in" (registered) before they can work.
        """
        # Import signals to register them
        # This is like connecting event listeners - they won't work until connected
        import expert.signals  # noqa

