from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.core import mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

User = get_user_model()

class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='old_password',
            registration='1234567'
        )
        self.change_password_url = reverse('change-password')
        self.reset_request_url = reverse('password-reset')
        self.reset_confirm_url = reverse('password-reset-confirm')

    def test_change_password_success(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'old_password': 'old_password',
            'new_password': 'new_password123'
        }
        response = self.client.post(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password123'))

    def test_change_password_wrong_old(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'old_password': 'wrong_password',
            'new_password': 'new_password123'
        }
        response = self.client.post(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_reset_request(self):
        data = {'email': 'test@example.com'}
        response = self.client.post(self.reset_request_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Redefinição de Senha', mail.outbox[0].subject)

    def test_password_reset_confirm_success(self):
        token = default_token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        
        data = {
            'uidb64': uid,
            'token': token,
            'new_password': 'new_reset_password123'
        }
        response = self.client.post(self.reset_confirm_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_reset_password123'))

    def test_password_reset_confirm_invalid_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        data = {
            'uidb64': uid,
            'token': 'invalid-token',
            'new_password': 'new_reset_password123'
        }
        response = self.client.post(self.reset_confirm_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
