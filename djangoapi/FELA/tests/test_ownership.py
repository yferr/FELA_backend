"""
tests/test_ownership.py

Integration tests verifying that ownership is correctly assigned and enforced
across the full Event creation flow (including nested presentations and speakers).

Run via:
    python manage.py test FELA.tests.test_ownership
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from FELA.models import Country, City, Agency, Event, Presentation, Speaker, EventAgency

User = get_user_model()


class EventOwnershipTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.superuser = User.objects.create_superuser(
            username='admin', password='admin123', email='admin@test.com', is_approved=True
        )
        self.user_a = User.objects.create_user(
            username='user_a', password='pass123', email='a@test.com', is_approved=True
        )
        self.user_b = User.objects.create_user(
            username='user_b', password='pass123', email='b@test.com', is_approved=True
        )

        # Pre-create geography
        self.country = Country.objects.create(
            country='Spain', lat=40.46, lon=-3.74, created_by=self.superuser
        )
        self.city = City.objects.create(
            country=self.country, city='Madrid',
            lat=40.41, lon=-3.70, created_by=self.superuser
        )
        self.agency = Agency.objects.create(
            name='FIG', created_by=self.superuser
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _create_event_payload(self, title='Test Event'):
        return {
            'date': '1-5 June 2025',
            'year': 2025,
            'type': 'Conference',
            'country': 'Spain',
            'city': 'Madrid',
            'event_title': title,
            'country_lat': 40.46,
            'country_lon': -3.74,
            'city_lat': 40.41,
            'city_lon': -3.70,
            'agencies': ['FIG'],
            'presentations': [
                {
                    'title': 'My Presentation',
                    'language': ['English'],
                    'speakers': [
                        {'name': 'John Doe', 'country': 'Spain', 'agency': 'FIG'}
                    ]
                }
            ]
        }

    # ------------------------------------------------------------------
    # create-complete endpoint
    # ------------------------------------------------------------------

    def test_create_complete_sets_created_by_on_event(self):
        self.client.force_authenticate(user=self.user_a)
        response = self.client.post(
            '/FELA/events/create-complete/',
            self._create_event_payload('Event A'),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        event = Event.objects.get(event_title='Event A')
        self.assertEqual(event.created_by, self.user_a)

    def test_create_complete_sets_created_by_on_presentation(self):
        self.client.force_authenticate(user=self.user_a)
        self.client.post(
            '/FELA/events/create-complete/',
            self._create_event_payload('Event B'),
            format='json'
        )
        presentation = Presentation.objects.filter(
            event__event_title='Event B'
        ).first()
        self.assertIsNotNone(presentation)
        self.assertEqual(presentation.created_by, self.user_a)

    def test_create_complete_sets_created_by_on_speaker(self):
        self.client.force_authenticate(user=self.user_a)
        self.client.post(
            '/FELA/events/create-complete/',
            self._create_event_payload('Event C'),
            format='json'
        )
        speaker = Speaker.objects.filter(name='John Doe').first()
        self.assertIsNotNone(speaker)
        self.assertEqual(speaker.created_by, self.user_a)

    def test_user_b_cannot_edit_user_a_event(self):
        # user_a creates event
        self.client.force_authenticate(user=self.user_a)
        self.client.post(
            '/FELA/events/create-complete/',
            self._create_event_payload('Event D'),
            format='json'
        )
        event = Event.objects.get(event_title='Event D')

        # user_b tries to edit
        self.client.force_authenticate(user=self.user_b)
        response = self.client.patch(
            f'/FELA/events/{event.pk}/',
            {'type': 'Workshop'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_a_can_edit_own_event(self):
        self.client.force_authenticate(user=self.user_a)
        self.client.post(
            '/FELA/events/create-complete/',
            self._create_event_payload('Event E'),
            format='json'
        )
        event = Event.objects.get(event_title='Event E')
        response = self.client.patch(
            f'/FELA/events/{event.pk}/',
            {'type': 'Workshop'},
            format='json'
        )
        print("DEBUG:", response.status_code)
        print("DEBUG DATA:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_superuser_can_edit_any_event(self):
        self.client.force_authenticate(user=self.user_a)
        self.client.post(
            '/FELA/events/create-complete/',
            self._create_event_payload('Event F'),
            format='json'
        )
        event = Event.objects.get(event_title='Event F')

        self.client.force_authenticate(user=self.superuser)
        response = self.client.patch(
            f'/FELA/events/{event.pk}/',
            {'type': 'Seminar'},
            format='json'
        )
        print("DEBUG:", response.status_code)
        print("DEBUG DATA:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_b_cannot_delete_user_a_event(self):
        self.client.force_authenticate(user=self.user_a)
        self.client.post(
            '/FELA/events/create-complete/',
            self._create_event_payload('Event G'),
            format='json'
        )
        event = Event.objects.get(event_title='Event G')

        self.client.force_authenticate(user=self.user_b)
        response = self.client.delete(f'/FELA/events/{event.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_delete_own_event(self):
        self.client.force_authenticate(user=self.user_a)
        self.client.post(
            '/FELA/events/create-complete/',
            self._create_event_payload('Event H'),
            format='json'
        )
        event = Event.objects.get(event_title='Event H')
        response = self.client.delete(f'/FELA/events/{event.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # ------------------------------------------------------------------
    # add-agency action (object-level permission on the event)
    # ------------------------------------------------------------------

    def test_user_b_cannot_add_agency_to_user_a_event(self):
        self.client.force_authenticate(user=self.user_a)
        self.client.post(
            '/FELA/events/create-complete/',
            self._create_event_payload('Event I'),
            format='json'
        )
        event = Event.objects.get(event_title='Event I')

        self.client.force_authenticate(user=self.user_b)
        response = self.client.post(
            f'/FELA/events/{event.pk}/add-agency/',
            {'agency_name': 'UN-GGIM'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_add_agency_to_own_event(self):
        self.client.force_authenticate(user=self.user_a)
        self.client.post(
            '/FELA/events/create-complete/',
            self._create_event_payload('Event J'),
            format='json'
        )
        event = Event.objects.get(event_title='Event J')
        response = self.client.post(
            f'/FELA/events/{event.pk}/add-agency/',
            {'agency_name': 'UN-GGIM'},
            format='json'
        )
        
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])
