from django.test import TestCase
from blog.models import Tag 
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from extensions.code_generator import otp_generator, get_client_ip
from rest_framework.response import Response

from account.send_otp import send_otp


class BookTestAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        

    def test_get_tag(self):
        # Make the GET request
        response = self.client.get(reverse('blog:tag-list'))
        
        # Check the status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the response data
        self.assertEqual(len(response.data), 1)


        # Check that the data structure matches what you expect
        expected_data = {"data":"success", "errors": False, "message": ""},
        data = response.data
    
        
        self.assertEqual(data, expected_data)