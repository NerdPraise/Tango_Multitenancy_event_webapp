from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Company(models.Model):
    name = models.CharField(max_length=50, verbose_name='Comapny\'s name')
    uuid = models.UUIDField(default=uuid4, editable=False)

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return f'{self.name}'


class CompanyMixin(models.Model):
    company_i = models.ForeignKey(
        to=Company, on_delete=models.PROTECT)

    class Meta:
        abstract = True


class User(CompanyMixin, AbstractUser):
    company_id = models.UUIDField(editable=False, null=False)
    full_name = models.CharField(max_length=50, verbose_name='Full Name')
    default_timezone = models.CharField(
        max_length=30, verbose_name='time zone')

    def __str__(self):
        return f'{self.full_name}'

    def save(self, *args, **kwargs):
        if not self.id:
            if not self.company_i_id:
                # Safe case for Superuser creation
                self.company_i = Company.objects.get(
                    name=settings.DEFAULT_COMPANY_NAME)
            self.full_name = f'{self.first_name} +{self.last_name}'
            self.company_id = self.company_i.uuid
        super().save(*args, **kwargs)


class ConferenceRoom(CompanyMixin):
    user = models.OneToOneField(
        'User', on_delete=models.SET_NULL, null=True, verbose_name='Manager')
    name = models.CharField(max_length=30, verbose_name='Conference room')
    Address = models.TextField()


class Calendar(CompanyMixin):
    user = models.OneToOneField(
        'User', on_delete=models.CASCADE, verbose_name='Owner',
        related_name='owner')
    event_name = models.CharField(max_length=30, verbose_name='Event name')
    meeting_agenda = models.TextField()
    start_time = models.DateTimeField(verbose_name="Start time")
    end_time = models.DateTimeField(verbose_name="End time")
    participants = models.ManyToManyField(
        'User', related_name="participants_list")
    location = models.OneToOneField(
        'ConferenceRoom', on_delete=models.SET_NULL, null=True, blank=True)
