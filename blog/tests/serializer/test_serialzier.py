from django.test import TestCase
from rest_framework.exceptions import ValidationError
from blog.models import Tag as Tag
from blog.seralziers import TagSerializers as   TagSerializer, BlogItemsSeriazler

class TagSerializerTest(TestCase):
    def setUp(self):
        # Setup any data needed for the tests
        self.valid_data = {
            'title': 'The Great Gatsby'
           
        }
        self.invalid_data = {
            'title': 1111
          
        }
        self.blog_item_data = {
            "ttile": "The Great Gatsby",
             "image": "https://sts-hik.uz/media/products/imgs/DS-2CE76H0T-ITPF_2.jpg",
        }
        self.blog_item_errror_data = {
            "title": 1111,
        }
        self.Tag = Tag.objects.create(**self.valid_data)

    def test_serializer_valid_data(self):
        serializer = TagSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['title'], 'The Great Gatsby')
     

    def test_serializer_invalid_data(self):
        serializer = TagSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
      

    def test_serializer_save(self):
        serializer = TagSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        Tag_instance = serializer.save()
        self.assertEqual(Tag_instance.title, 'The Great Gatsby')
      

    def test_serializer_output(self):
        serializer = TagSerializer(self.Tag)
        expected_data = {
            'id': self.Tag.id,
            'title': 'The Great Gatsby',
          
        }
        self.assertEqual(serializer.data, expected_data)

    def test_validation_error(self):
        with self.assertRaises(ValidationError):
            serializer = TagSerializer(data=self.invalid_data)
            if not serializer.is_valid():
                raise ValidationError(serializer.errors)
            

    def test_blog_item_serializer_valid_data(self):
        serializer = BlogItemsSeriazler(data=self.blog_item_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['title'], 'The Great Gatsby')
        self.assertEqual(serializer.validated_data['image'], self.valid_data['image'])
            

    
