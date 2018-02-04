import time
from django.test import TestCase,  Client
from django.core.files.uploadedfile import SimpleUploadedFile
from pins.models import Category, Pin


class CategoryModelTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_category_save(self):
        category = Category.objects.create(title='Category One')
        self.assertEqual(str(category.title), 'Category One')
        self.assertEqual(category.slug, 'category-one') # slug autosave


class PinModelTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_pin_save(self):
        category = Category.objects.create(title='Amsterdam')
        title = '1935 a view of the leidseplein in amsterdam'
        path = '/home/matt/Documents/Explorer/media/ImageTest/4904742524.jpg'
        image = SimpleUploadedFile(name='4904742524.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        note = 'a short description about the image'
        Pin.objects.create(title=title, image=image, note=note, category=category)
        pin = Pin.objects.get(slug='1935-a-view-of-the-leidseplein-in-amsterdam')
        self.assertEqual(pin.slug, '1935-a-view-of-the-leidseplein-in-amsterdam')























