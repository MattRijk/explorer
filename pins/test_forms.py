from django.test import TestCase
from pins.forms import CategoryForm


class CategoryFormTest(TestCase):

    def test_CategoryEditForm_valid(self):
        form = CategoryForm(data={'title':'category one'})
        self.assertTrue(form.is_valid())