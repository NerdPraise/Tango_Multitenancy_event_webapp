from rest_framework import status

from django.shortcuts import reverse

from tests.basetest import CalendarAPITestCase


class ConferenceTestcase(CalendarAPITestCase):
    valid_conference_data = {
        "name": "Conf room A",
        "address": "Somewhere"
    }

    def test_user_can_create_conference_room(self):
        """
        Logged in user should be able to create a conference room
        """
        # Log in user
        url = reverse('calendar:token_obtain_pair')
        response = self.client.post(
            url, {'username': 'nobody',  'password': 'nobody'}, format='json')
        access = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)

        url = reverse('calendar:conference-room')

        response = self.client.post(
            url, self.valid_conference_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'],
                         self.valid_conference_data['name'])

    def test_user_cant_create_room_no_login(self):
        """
        Anonymous user can't create a conference room
        """
        # Log out user from setup
        self.client.credentials()
        url = reverse('calendar:conference-room')

        response = self.client.post(
            url, self.valid_conference_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
