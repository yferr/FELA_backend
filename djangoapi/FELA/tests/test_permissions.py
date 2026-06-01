"""
tests/test_permissions.py

Tests for the IsOwnerOrSuperuser permission class and ownership enforcement
across all FELA endpoints.

Run via:
    python manage.py test FELA.tests.test_permissions
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from FELA.models import Country, Agency, Event, City

User = get_user_model()


class BaseTestCase(TestCase):
    """Shared setup for all permission tests."""

    def setUp(self):
        self.client = APIClient()

        # Superuser — full access to everything
        self.superuser = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@test.com',
            is_approved=True
        )

        # Approved user who owns the records
        self.owner = User.objects.create_user(
            username='owner',
            password='pass123',
            email='owner@test.com',
            is_approved=True
        )

        # Another approved user who does NOT own the records
        self.other_user = User.objects.create_user(
            username='other',
            password='pass123',
            email='other@test.com',
            is_approved=True
        )

        # User who has not been approved yet
        self.unapproved = User.objects.create_user(
            username='unapproved',
            password='pass123',
            email='unapproved@test.com',
            is_approved=False
        )

        # Record owned by self.owner
        self.country = Country.objects.create(
            country='TestLand',
            lat=10.0,
            lon=20.0,
            created_by=self.owner
        )

        # Legacy record — no owner (simulates data loaded before ownership)
        self.legacy_country = Country.objects.create(
            country='LegacyLand',
            lat=0.0,
            lon=0.0,
            created_by=None
        )


# ===========================================================================
# READ (public)
# ===========================================================================

class PublicReadTest(BaseTestCase):

    def test_anonymous_can_list_countries(self):
        response = self.client.get('/FELA/countries/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_can_retrieve_country(self):
        response = self.client.get(f'/FELA/countries/{self.country.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ===========================================================================
# CREATE
# ===========================================================================

class CreatePermissionTest(BaseTestCase):

    def test_approved_owner_can_create_country(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post('/FELA/countries/', {
            'country': 'NewLand', 'lat': 5.0, 'lon': 10.0
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unapproved_user_cannot_create(self):
        self.client.force_authenticate(user=self.unapproved)
        response = self.client.post('/FELA/countries/', {
            'country': 'BlockedLand', 'lat': 1.0, 'lon': 1.0
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_cannot_create(self):
        response = self.client.post('/FELA/countries/', {
            'country': 'AnonLand', 'lat': 0.0, 'lon': 0.0
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_can_create(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post('/FELA/countries/', {
            'country': 'SuperLand', 'lat': 50.0, 'lon': 50.0
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# ===========================================================================
# created_by ASSIGNMENT
# ===========================================================================

class CreatedByAssignmentTest(BaseTestCase):

    def test_created_by_is_set_to_request_user(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post('/FELA/countries/', {
            'country': 'AutoLand', 'lat': 1.0, 'lon': 1.0
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = Country.objects.get(country='AutoLand')
        self.assertEqual(created.created_by, self.owner)

    def test_client_cannot_override_created_by(self):
        """Even if the client sends created_by, it must be ignored."""
        self.client.force_authenticate(user=self.owner)
        response = self.client.post('/FELA/countries/', {
            'country': 'ManipLand',
            'lat': 1.0,
            'lon': 1.0,
            'created_by': self.superuser.pk  # attempt to spoof ownership
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = Country.objects.get(country='ManipLand')
        # Must be owner, NOT superuser
        self.assertEqual(created.created_by, self.owner)

    def test_created_by_in_response_is_username_string(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post('/FELA/countries/', {
            'country': 'StringLand', 'lat': 2.0, 'lon': 2.0
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # created_by in response should be a username string, not an integer ID
        self.assertEqual(response.data.get('created_by'), 'owner')


# ===========================================================================
# EDIT (PUT / PATCH)
# ===========================================================================

class EditPermissionTest(BaseTestCase):

    def test_owner_can_patch_own_record(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(
            f'/FELA/countries/{self.country.pk}/',
            {'lat': 99.0}
        )
        print("DEBUG:", response.status_code)
        print("DEBUG DATA:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_user_cannot_patch_record(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.patch(
            f'/FELA/countries/{self.country.pk}/',
            {'lat': 99.0}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_can_patch_any_record(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.patch(
            f'/FELA/countries/{self.country.pk}/',
            {'lat': 99.0}
        )
        print("DEBUG:", response.status_code)
        print("DEBUG DATA:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_patch(self):
        response = self.client.patch(
            f'/FELA/countries/{self.country.pk}/',
            {'lat': 99.0}
        )
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# ===========================================================================
# LEGACY RECORDS (created_by = None)
# ===========================================================================

class LegacyRecordPermissionTest(BaseTestCase):

    def test_regular_user_cannot_edit_legacy_record(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(
            f'/FELA/countries/{self.legacy_country.pk}/',
            {'lat': 50.0}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_other_user_cannot_edit_legacy_record(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.patch(
            f'/FELA/countries/{self.legacy_country.pk}/',
            {'lat': 50.0}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_can_edit_legacy_record(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.patch(
            f'/FELA/countries/{self.legacy_country.pk}/',
            {'lat': 50.0}
        )
        print("DEBUG:", response.status_code)
        print("DEBUG DATA:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_user_cannot_delete_legacy_record(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(
            f'/FELA/countries/{self.legacy_country.pk}/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_can_delete_legacy_record(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(
            f'/FELA/countries/{self.legacy_country.pk}/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# ===========================================================================
# DELETE
# ===========================================================================

class DeletePermissionTest(BaseTestCase):

    def test_owner_can_delete_own_record(self):
        country = Country.objects.create(
            country='DeleteMe', lat=1.0, lon=1.0, created_by=self.owner
        )
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(f'/FELA/countries/{country.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_other_user_cannot_delete_record(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(f'/FELA/countries/{self.country.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_can_delete_any_record(self):
        country = Country.objects.create(
            country='SuperDelete', lat=1.0, lon=1.0, created_by=self.owner
        )
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(f'/FELA/countries/{country.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_anonymous_cannot_delete(self):
        response = self.client.delete(f'/FELA/countries/{self.country.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# ===========================================================================
# AGENCY endpoint
# ===========================================================================

class AgencyPermissionTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.agency = Agency.objects.create(
            name='TestAgency',
            created_by=self.owner
        )

    def test_owner_can_edit_agency(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(
            f'/FELA/agencies/{self.agency.pk}/',
            {'long_name': 'Updated Name'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_user_cannot_edit_agency(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.patch(
            f'/FELA/agencies/{self.agency.pk}/',
            {'long_name': 'Hacked'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
