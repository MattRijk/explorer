from django.test import TestCase,  Client
from pins.models import Category



class PinsModelTestCase(TestCase): pass


class PinViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home_page_template(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'home.html')

class CategoryModelTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_category_save(self):
        category = Category.objects.create(title='Category One')
        self.assertEqual(str(category.title), 'Category One')
        self.assertEqual(category.slug, 'category-one')

















