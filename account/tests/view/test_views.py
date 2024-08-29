from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


class TestRegisterAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("account:register")
        self.data = {
            "phone": "+998931234567",
        }
        self.data_invalid = {
            "phone": "99893123456",
        }

    def test_create_user_success(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_invalid_data(self):
        response = self.client.post(self.url, self.data_invalid)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("phone", response.json()["non_field_errors"][0])

    def test_create_user_duplicate_phone(self):
        self.client.post(self.url, self.data)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("phone", response.json()["phone"][0])

    def test_create_user_with_wrong_format_phone(self):
        self.data["phone"] = "9989312345678"
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("phone", response.json()["phone"][0])
    
