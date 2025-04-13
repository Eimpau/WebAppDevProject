from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model
from django.conf import settings
import os

def create_default_superuser(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(is_superuser=True).exists():
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@localhost")
        print("Creating default superuser...")
        User.objects.create_superuser(username=username, password=password, email=email)

post_migrate.connect(create_default_superuser)
