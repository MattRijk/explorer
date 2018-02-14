from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from pins.models import Category, Pin

class HomePageViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_success(self):
        response = self.client.get(reverse('home_page'))
        self.assertIn('home page', str(response.content))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'home.html')

    def test_category_list_exist_on_home_page(self):
        Category.objects.create(title='category one')
        Category.objects.create(title='category two')
        response = self.client.get(reverse('home_page'))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, 'category one')
        self.assertContains(response, 'category two')
        self.assertIn('category one', [category.title for category in
                                       response.context['categories']])

    def test_all_image_link_on_home_page(self):
        response = self.client.get(reverse('home_page'))
        self.assertContains(response,'<a href="%s">All Images</a>' % reverse("pins:all_images"), html=True)
















