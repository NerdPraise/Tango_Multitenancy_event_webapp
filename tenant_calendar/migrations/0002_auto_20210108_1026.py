# Generated by Django 3.1.5 on 2021-01-08 09:26

from django.db import migrations
from django.conf import settings


def create_initial_company(apps, schema_editor):
    Company = apps.get_model('tenant_calendar', 'Company')
    Company.objects.create(
        id=1,
        name=settings.DEFAULT_COMPANY_NAME,
    )


def revert_create(apps, schema_editor):
    Company = apps.get_model('tenant_calendar', 'Company')
    Company.objects.get(id=1).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_calendar', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_company, revert_create)
    ]
