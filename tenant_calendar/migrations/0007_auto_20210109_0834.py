# Generated by Django 3.1.5 on 2021-01-09 07:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_calendar', '0006_auto_20210108_1944'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conferenceroom',
            old_name='Address',
            new_name='address',
        ),
        migrations.AlterField(
            model_name='calendar',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
    ]
