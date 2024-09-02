from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from account.models import User
from django.contrib.auth import get_user_model

user = get_user_model()





class RegisterTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.user = {
            "phone": "998990167647"
        }
        