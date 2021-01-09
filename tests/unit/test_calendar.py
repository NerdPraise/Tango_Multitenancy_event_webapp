from rest_framework import status

from django.shortcuts import reverse

from tests.basetest import CalendarAPITestCase


class ConferenceTestcase(CalendarAPITestCase):
    valid_event_data_with_location = {
        "user": "1",
        "event_name": "Management",
        "meeting_agenda": "Some words",
        "start_time": "2018-06-29 08:16",
        "end_time": "2018-06-29 08:19",
        "participants": [
            "admin@admin.admin"],
        "location":  {
            "name": "Room A",
            "address": "some place",
            "company_i": 1
        }
    }

    valid_event_data_without_location = {
        "user": "1",
        "event_name": "Management",
        "meeting_agenda": "Info about work",
        "start_time": "2018-06-29 08:16",
        "end_time": "2018-06-29 08:19",
        "participants": [
            "admin@admin.admin"],
    }

    def test_user_can_create_events(self):
        # Log in user
        url = reverse('calendar:token_obtain_pair')
        response = self.client.post(
            url, {'username': 'nobody',  'password': 'nobody'}, format='json')
        access = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)

        url = reverse('calendar:calendar')

        # With the location set
        response = self.client.post(
            url, self.valid_event_data_with_location, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data['event_name'],
            self.valid_event_data_with_location['event_name'])

        # Without the location set
        response = self.client.post(
            url, self.valid_event_data_without_location, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data['event_name'],
            self.valid_event_data_without_location['event_name'])

    def test_user_can_search_events(self):
        # Log in user
        url = reverse('calendar:token_obtain_pair')
        response = self.client.post(
            url, {'username': 'nobody',  'password': 'nobody'}, format='json')
        access = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)

        url = reverse('calendar:calendar')

        # create calendar event
        response = self.client.post(
            url, self.valid_event_data_without_location, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data['event_name'],
            self.valid_event_data_without_location['event_name'])

        search_url = url + '?search=Management'
        response = self.client.get(search_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['event_name'], 'Management')
