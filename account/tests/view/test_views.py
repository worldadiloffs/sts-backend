from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from django.core.cache import cache

from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()

class VerifyOtpTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('verify-otp')  # Replace 'verify-otp' with your actual URL name
        self.register_url = reverse('register')  # Replace'register' with your actual URL name
        self.phone = '+998901234567'
        self.otp = '123456'

        # Cache OTP and phone for testing
        ip = '127.0.0.1'  # Mocking IP address
        cache.set(f"{ip}-for-authentication", self.phone, timeout=300)
        cache.set(self.phone, self.otp, timeout=300)
        
        # Creating a test user
        

    def test_register_success(self):
        data = {
            "phone": self.phone,
        }
        
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_verify_otp_success(self):
        data = {
            "code": self.otp,
        }
        
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user = User.objects.create_user(phone=self.phone)
        self.user.save()
        token = RefreshToken.for_user(self.user)
        self.assertEqual(response.data["access"], str(token.access_token))
        self.assertIn("access", response.data)