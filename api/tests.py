from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Profile

User = get_user_model()

class ProfileAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser', 
            password='testpassword',
            )
        cls.admin_user = User.objects.create_superuser(
            username='adminuser', 
            password='adminpassword'
            )
        cls.profile = Profile.objects.create(
            user=cls.user, 
            bio='Test bio', 
            location='Test location',
        )

    #### Unauthenticated
    def test_list_unauthenticated(self):
        response = self.client.get(reverse('profile_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_cannot_create(self):
        response = self.client.post(
            reverse('profile_list'), 
            {'user': self.user.id, 'bio': 'New bio', 'location': 'New location'}
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_update(self):
        response = self.client.put(
            reverse('profile_detail', args=[self.profile.id]), 
            {'user': self.user.id, 'bio': 'Updated bio', 'location': 'Updated location'}
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_unauthenticated_user_cannot_delete(self):
        response = self.client.delete(reverse('profile_detail', args=[self.profile.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #### Authenticated
    def test_authenticated_user_can_create_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('profile_list'), 
            {'user': self.user.id, 'bio': 'New bio', 'location': 'New location'}
            )
        # print('content:', response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Profile.objects.count(), 2)

    def test_authenticated_user_can_update_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            reverse('profile_detail', args=[self.profile.id]), 
            {'user': self.user.id, 'bio': 'Updated bio', 'location': 'Updated location'}
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, 'Updated bio')
        self.assertEqual(self.profile.location, 'Updated location')

    def test_authenticated_user_can_delete_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('profile_detail', args=[self.profile.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Profile.objects.filter(id=self.profile.id).exists())

    ##### Admin
    def test_admin_user_can_create_profile(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(
            reverse('profile_list'), 
            {'user': self.user.id, 'bio': 'New bio', 'location': 'New location'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Profile.objects.count(), 2)

    def test_admin_user_can_update_profile(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(
            reverse('profile_list'), 
            {'user': self.user.id, 'bio': 'New bio', 'location': 'New location'}
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.put(
            reverse('profile_detail', args=[response.data['user']]), 
            {'user': self.user.id, 'bio': 'Updated bio', 'location': 'Updated location'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, 'Updated bio')
        self.assertEqual(self.profile.location, 'Updated location')

    def test_admin_user_can_delete_profile(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(
            reverse('profile_list'), 
            {'user': self.user.id, 'bio': 'New bio', 'location': 'New location'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.delete(reverse('profile_detail', args=[response.data['user']]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Profile.objects.filter(id=self.profile.id).exists())