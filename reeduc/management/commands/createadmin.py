from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

User = get_user_model()

class Command(BaseCommand):
    help = "Create default superuser if it doesn't exist"

    def handle(self, *args, **kwargs):
        username = config("ADMIN_USER")
        email = config("ADMIN_EMAIL")
        password = config("ADMIN_PASSWORD")

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' criado."))
        else:
            self.stdout.write(self.style.WARNING(f"Superuser '{username}' já existe."))
