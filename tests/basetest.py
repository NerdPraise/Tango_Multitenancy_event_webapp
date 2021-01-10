from rest_framework.test import APITestCase

from django.apps import apps
from django.shortcuts import reverse

Company = apps.get_model('tenant_calendar', 'Company')
Calendar = apps.get_model('tenant_calendar', 'Calendar')
User = apps.get_model('tenant_calendar', 'User')
ConferenceRoom = apps.get_model('tenant_calendar', 'ConferenceRoom')


class CalendarAPITestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
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

    def setUp(self):
        # Log in user
        url = reverse('calendar:token_obtain_pair')
        response = self.client.post(
            url, {'username': 'nobody',  'password': 'nobody'}, format='json')
        access = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)

    def tearDown(self):
        self.client.credentials()

    @classmethod
    def tearDownClass(cls):
        User.objects.filter(email='nobody@nobody.niks').delete()
        User.objects.filter(email='admin@admin.admin').delete()
