# api/signals.py
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model
from django.dispatch import receiver

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(is_superuser=True).exists():
        email = 'admin@example.com'
        name = 'admin'
        password = 'admin'
        User.objects.create_superuser(email=email, name=name, password=password)
        print('Successfully created new superuser')
    else:
        print('Superuser already exists')