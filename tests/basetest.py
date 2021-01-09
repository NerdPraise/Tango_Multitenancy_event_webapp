from rest_framework.test import APITestCase

from django.apps import apps
from django.shortcuts import reverse

Company = apps.get_model('tenant_calendar', 'Company')
Calendar = apps.get_model('tenant_calendar', 'Calendar')
User = apps.get_model('tenant_calendar', 'User')
ConferenceRoom = apps.get_model('tenant_calendar', 'ConferenceRoom')


class CalendarAPITestCase(APITestCase):
    def setUp(self):
        company_i = Company.objects.create(name='Some company')
        ConferenceRoom.objects.create(
            name='Room A', address='some place', company_i=company_i)
        user = User.objects.create_user(
            username='admin', email='admin@admin.admin', password='admin',
            company_i=company_i
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()

        user = User.objects.create_user(
            username='nobody', email='nobody@nobody.niks', password='nobody',
            company_i=company_i
        )
        user.is_staff = False
        user.is_superuser = False
        user.save()

    def tearDown(self):
        User.objects.filter(email='nobody@nobody.niks').delete()
        User.objects.filter(email='admin@admin.admin').delete()
