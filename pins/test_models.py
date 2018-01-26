from django.test import TestCase,  Client
from pins.models import Category


class CategoryModelTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_category_save(self):
        category = Category.objects.create(title='Category One')
        self.assertEqual(str(category.title), 'Category One')
        self.assertEqual(category.slug, 'category-one') # slug autosave

















