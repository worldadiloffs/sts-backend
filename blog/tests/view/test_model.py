from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from blog.models import Tag 



class TagTest(TestCase):
    tag_1 = Tag.objects.create(title="Tag 1")
    tag_2 = Tag.objects.create(title="Tag 2")


    def test_tag_create(self):
        self.assertCountEqual(self.tag_1)






