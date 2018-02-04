from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from pins.models import Category, Pin


class CategoryViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_category_list(self):
        Category.objects.create(title='Category One')
        Category.objects.create(title='Category Two')
        response = self.client.get(reverse('homepage'))
        self.assertIn('Category One', str(response.content))
        self.assertIn('Category Two', str(response.content))

class PinViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home_page_template(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'home.html')

