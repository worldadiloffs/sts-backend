from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from account.models import User
from django.contrib.auth import get_user_model
from extensions import code_generator 

user = get_user_model()

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import Client

class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/ru/sts/account/register/"  # register URL nomini to'g'ri qo'ying
        data_set = {
        "otp": "123456",
        "errors": False,
        "message": "",
        # "sms_provayder": response.json()

    }

    def test_valid_phone_number(self):
        data = {'phone': '998990167647'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("send", response.data['message'])

    def test_invalid_phone_number(self):
        data = {'phone': ''}  # Yoki boshqa noto'g'ri qiymat
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone', response.data)