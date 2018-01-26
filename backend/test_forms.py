from datetime import datetime
from django.test import TestCase
from backend.forms import EditUserForm, CreateUserForm



class UserFormTest(TestCase):

    def test_UserEditForm_valid(self):
        form = EditUserForm(data={'username':'auser', 'email':'auser@gmail.com',
                                   'is_superuser':True, 'is_active':True, 'is_staff':True})
        self.assertTrue(form.is_valid())


    def test_CreateUserForm_valid(self):
        form = CreateUserForm(data={'username':'auser', 'email':'auser@gmail.com',
                                    'password1':'passphrase', 'password2':'passphrase',
                                   'is_superuser':True, 'is_active':True, 'is_staff':True})
        self.assertTrue(form.is_valid())

