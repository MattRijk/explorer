from django.test import TestCase
from backend.forms import EditUserForm


class UserFormTest(TestCase):

    def test_UserEditForm_valid(self):
        form = EditUserForm(data={'username':'juser', 'email':'juser@gmail.com'})
        self.assertTrue(form.is_valid())

