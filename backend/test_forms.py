from django.test import TestCase
from backend.forms import EditUserForm, EditCategoryForm


class UserFormTest(TestCase):

    def test_UserEditForm_valid(self):
        form = EditUserForm(data={'username':'juser', 'email':'juser@gmail.com'})
        self.assertTrue(form.is_valid())

class CategoryFormTest(TestCase):

    def test_CategoryEditForm_valid(self):
        form = EditCategoryForm(data={'title':'category two'})
        self.assertTrue(form.is_valid())