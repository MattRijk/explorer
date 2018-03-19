from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from pins.models import Category

CATEGORY_IMAGE_TEST_PATH = '/home/matt/Documents/Explorer/ImageTest/categories/'

class HomePageViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_success(self):
        response = self.client.get(reverse('home_page'))
        self.assertIn('home page', str(response.content))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'home.html')

    def test_category_list_exist_on_home_page(self):
        path = '%scategory_one.jpg' % CATEGORY_IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='category_one.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        description='a short category description'
        Category.objects.create(title='category one', image=image, description=description)
        path = '%scategory_two.jpg' % CATEGORY_IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='category_two.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        Category.objects.create(title='category two', image=image, description=description)
        response = self.client.get(reverse('home_page'))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, 'category one')
        self.assertContains(response, 'category two')
        self.assertIn('category one', [category.title for category in
                                       response.context['categories']])

    def test_all_image_link_on_home_page(self):
        response = self.client.get(reverse('home_page'))
        self.assertContains(response,'<a href="%s">All Images</a>' % reverse("pins:all_images"), html=True)
















