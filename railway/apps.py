"""Django apps module"""

from django.apps import AppConfig


class RailwayConfig(AppConfig):
    """Class used to configure the railway application"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'railway'
