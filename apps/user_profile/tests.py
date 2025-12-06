"""
Comprehensive tests for User Profile API.
"""
import pytest
from datetime import date, timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import UserProfile


class UserProfileAPITestCase(APITestCase):
    """
    Test cases for User Profile API endpoints.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.client = APIClient()
        self.list_url = reverse('userprofile-list')

        # Create test profiles
        self.profile1 = UserProfile.objects.create(
            email='john.doe@example.com',
            first_name='John',
            last_name='Doe',
            phone_number='+1234567890',
            city='New York',
            state='NY',
            country='USA',
        )

        self.profile2 = UserProfile.objects.create(
            email='jane.smith@example.com',
            first_name='Jane',
            last_name='Smith',
            phone_number='+1987654321',
            city='Los Angeles',
            state='CA',
            country='USA',
        )

        self.valid_payload = {
            'email': 'test.user@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '+1555555555',
            'address_line1': '123 Test St',
            'city': 'Test City',
            'state': 'TC',
            'postal_code': '12345',
            'country': 'USA',
            'date_of_birth': '1990-01-01',
            'bio': 'This is a test user profile.',
        }

    def test_create_profile_success(self):
        """
        Test creating a new user profile successfully.
        """
        response = self.client.post(self.list_url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserProfile.objects.count(), 3)
        self.assertEqual(response.data['email'], 'test.user@example.com')
        self.assertIn('id', response.data)
        self.assertIn('created_at', response.data)

    def test_create_profile_duplicate_email(self):
        """
        Test creating a profile with duplicate email fails.
        """
        invalid_payload = self.valid_payload.copy()
        invalid_payload['email'] = 'john.doe@example.com'  # Already exists

        response = self.client.post(self.list_url, invalid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_create_profile_invalid_email(self):
        """
        Test creating a profile with invalid email fails.
        """
        invalid_payload = self.valid_payload.copy()
        invalid_payload['email'] = 'invalid-email'

        response = self.client.post(self.list_url, invalid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_profile_future_birth_date(self):
        """
        Test creating a profile with future birth date fails.
        """
        invalid_payload = self.valid_payload.copy()
        invalid_payload['date_of_birth'] = (date.today() + timedelta(days=1)).isoformat()

        response = self.client.post(self.list_url, invalid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_profiles(self):
        """
        Test listing all user profiles.
        """
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_profile(self):
        """
        Test retrieving a specific user profile.
        """
        detail_url = reverse('userprofile-detail', args=[self.profile1.id])
        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'john.doe@example.com')
        self.assertEqual(response.data['full_name'], 'John Doe')

    def test_update_profile(self):
        """
        Test updating a user profile.
        """
        detail_url = reverse('userprofile-detail', args=[self.profile1.id])
        update_payload = {
            'first_name': 'Johnny',
            'city': 'Boston',
        }

        response = self.client.patch(detail_url, update_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Johnny')
        self.assertEqual(response.data['city'], 'Boston')
        # Ensure other fields remain unchanged
        self.assertEqual(response.data['last_name'], 'Doe')

    def test_delete_profile_soft_delete(self):
        """
        Test deleting (soft delete) a user profile.
        """
        detail_url = reverse('userprofile-detail', args=[self.profile1.id])
        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify soft delete (profile still exists but is inactive)
        self.profile1.refresh_from_db()
        self.assertFalse(self.profile1.is_active)

    def test_search_profiles(self):
        """
        Test searching profiles by name or email.
        """
        response = self.client.get(self.list_url, {'search': 'john'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['email'], 'john.doe@example.com')

    def test_filter_profiles_by_state(self):
        """
        Test filtering profiles by state.
        """
        response = self.client.get(self.list_url, {'state': 'NY'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['state'], 'NY')

    def test_active_profiles_endpoint(self):
        """
        Test the active profiles custom endpoint.
        """
        # Deactivate one profile
        self.profile2.is_active = False
        self.profile2.save()

        active_url = reverse('userprofile-active')
        response = self.client.get(active_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['email'], 'john.doe@example.com')

    def test_search_by_email_endpoint(self):
        """
        Test the search by email custom endpoint.
        """
        search_url = reverse('userprofile-search-by-email')
        response = self.client.get(search_url, {'email': 'john.doe@example.com'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'john.doe@example.com')

    def test_search_by_email_not_found(self):
        """
        Test search by email returns 404 for non-existent email.
        """
        search_url = reverse('userprofile-search-by-email')
        response = self.client.get(search_url, {'email': 'nonexistent@example.com'})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_reactivate_profile(self):
        """
        Test reactivating a deactivated profile.
        """
        # Deactivate profile
        self.profile1.is_active = False
        self.profile1.save()

        reactivate_url = reverse('userprofile-reactivate', args=[self.profile1.id])
        response = self.client.post(reactivate_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile1.refresh_from_db()
        self.assertTrue(self.profile1.is_active)
