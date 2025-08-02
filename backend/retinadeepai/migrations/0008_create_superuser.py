import logging
import os
from django.db import migrations

logger = logging.getLogger(__name__)

def generate_superuser(apps, schema_editor):
    from django.contrib.auth import get_user_model

    USERNAME = os.environ.get('ADMIN_DJANGO_USERNAME', 'admin')
    PASSWORD = os.environ.get('ADMIN_DJANGO_PASSWORD', 'adminadmin')
    EMAIL = os.environ.get('ADMIN_DJANGO_EMAIL', 'admin@mail.ru')

    user = get_user_model()

    if not user.objects.filter(username=USERNAME, email=EMAIL).exists():
        logger.info("Creating new superuser")
        admin = user.objects.create_superuser(
           username=USERNAME, password=PASSWORD, email=EMAIL
        )
        admin.save()
    else:
        logger.info("Superuser already created!")


class Migration(migrations.Migration):

    dependencies = [
        ('retinadeepai', '0007_retinalabelmark_is_visible'),
    ]

    operations = [migrations.RunPython(generate_superuser)]
