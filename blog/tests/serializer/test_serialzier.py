from django.test import TestCase
from rest_framework.exceptions import ValidationError
from blog.models import Tag as Tag
from blog.seralziers import TagSerializers as   TagSerializer, BlogItemsSeriazler
import io
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.exceptions import ValidationError


class TagSerializerTest(TestCase):
    def setUp(self):
        # Setup any data needed for the tests
        self.valid_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=open('/home/azamat/Desktop/full_crm/sitebac/crmSiteBackend/media/banner/images/logosts_utFgGsN_1.webp', 'rb').read(), 
            content_type='image/webp'
        )
        self.blog_item_data = {
            "title": "The Great Gatsby",
            "content": "fdfdfdfdfdf",
             "image": self.valid_image,
             "tag": []
        }
        self.invalid_blog_item_data = {
            "title": "The Great Gatsby",
            "content": "fdfdfdfdfdf",
             "image": self.valid_image,
             "tag": []
        }
        


          

    def test_blog_item_serializer_valid_data(self):
        serializer = BlogItemsSeriazler(data=self.blog_item_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        self.assertEqual(serializer.validated_data['title'], 'The Great Gatsby')
        self.assertEqual(serializer.validated_data['content'], 'fdfdfdfdfdf')
        self.assertEqual(serializer.validated_data['image'], self.valid_image)
        self.assertEqual(serializer.validated_data['tag'], [])