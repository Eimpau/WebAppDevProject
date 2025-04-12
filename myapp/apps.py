from django.apps import AppConfig


class MyAppConfig(AppConfig): # Define the configuration for the app named 'myapp'
    default_auto_field = 'django.db.models.BigAutoField'  # Set the default primary key field type for models in this app
    name = 'myapp' # Specify the name of the app 
