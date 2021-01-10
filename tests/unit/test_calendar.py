from rest_framework import status

from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from tests.basetest import CalendarAPITestCase


User = get_user_model()


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
        """
        User can search through events in their company
        """
        url = reverse('calendar:calendar')

        # create calendar event
        response = self.client.post(
            url, self.valid_event_data_without_location, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data['event_name'],
            self.valid_event_data_without_location['event_name'])

        user = User.objects.get(username='nobody')
        search_url = url + '?search=Management'
        response = self.client.get(search_url)

        # Any part of the list would have the query among
        data = response.data[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['event_name'], 'Management')
        self.assertEqual(data['company_i'], user.company_i.name)
