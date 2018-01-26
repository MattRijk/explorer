from django.test import TestCase
from backend.forms import EditUserForm


class UserFormTest(TestCase):

    def test_UserForm_valid(self):
        form =  EditUserForm(data={'username':'auser', 'email':'auser@gmail.com'})
        self.assertTrue(form.is_valid())

