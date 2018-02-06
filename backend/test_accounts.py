from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class UserAccountViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.authenticated, self.response = self.superuserLoggedIn(
            username='auser' ,
            email='auser1234@yahoo.com')

    def test_dashboard_template(self):
        response = self.client.get(reverse('backend:index'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'index.html')

    def test_superuser_can_login(self):
        response = self.client.get(reverse('backend:index'))
        self.assertTrue(self.authenticated)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('backend/index.html')
        self.assertIn('auser', str(response.content))

    def test_user_exists(self):
        self.save_user(username='buser', email='buser1234@yahoo.com')
        response = self.client.get(reverse('backend:index'))
        self.assertTrue(self.authenticated)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('index.html')
        # response = self.client.get(reverse('backend:index'))
        self.assertIn('buser', str(response.content))

    def test_superuser_can_edit_superuser(self):
        response = self.client.get(reverse('backend:index'))
        self.assertContains(response, '<a href="%s">Edit</a>' % reverse("backend:editUser", args=[1]), html=True)
        self.assertTrue(self.authenticated)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('index.html')
        self.assertIn('auser', str(response.content))
        self.client.post('/backend/user/edit/1',
             data={'username':'auser', 'email':'auser5555@yahoo.com',
                   'is_superuser':True})
        response = self.client.get(reverse('backend:index'))
        self.assertTrue(self.authenticated)
        self.assertIn('auser', str(response.content))
        self.assertIn('auser5555@yahoo.com', str(response.content))

    def test_superuser_can_create_superuser(self):
        response = self.client.get(reverse('backend:index'))
        self.assertContains(response, '<a href="%s">Create Superuser</a>' % reverse("backend:createUser"), html=True)
        self.assertIn('Create Superuser', str(response.content))
        self.assertTrue(self.authenticated)
        self.client.post('/backend/user/create/', data={'username': 'some_user',
                               'email':'superuser2@yahoo.com',
                               'password1':'passphrase', 'password2':'passphrase',
                               'is_superuser': True})
        response = self.client.get(reverse('backend:index'))
        self.assertIn('some_user', str(response.content))

    def test_superuser_can_edit_active_user(self):
        self.save_user(username='buser', email='buser1234@yahoo.com')
        response = self.client.get(reverse('backend:index'))
        self.assertTrue(self.authenticated)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('index.html')
        self.assertIn('buser', str(self.client.get(reverse('backend:index')).content))
        self.assertIn('buser1234@yahoo.com', str(self.client.get(reverse('backend:index')).content))
        response = self.client.get(reverse('backend:index'))
        self.assertContains(response, '<a href="%s">Edit Active User</a>' % reverse("backend:editUser", args=[2]), html=True)
        self.assertIn('Edit', str(self.client.get(reverse('backend:index')).content))
        self.client.post('/backend/user/edit/2',
             data={'username':'buser', 'email':'buser5555@yahoo.com', 'password':'passphrase'})
        self.assertIn('buser5555@yahoo.com', str(self.client.get(reverse('backend:index')).content))

    def test_superuser_can_delete_active_user(self):
        self.save_user(username='buser', email='buser1234@yahoo.com')
        response = self.client.get(reverse('backend:index'))
        self.assertTrue(self.authenticated)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('index.html')
        response = self.client.get(reverse('backend:index'))
        self.assertIn('buser', str(response.content))
        self.assertIn('buser1234@yahoo.com', str(response.content))
        self.assertContains(response, '<a href="%s">Delete</a>' % reverse("backend:deleteUser", args=[1]), html=True)
        self.client.post('/backend/user/delete/1')
        response = self.client.get(reverse('backend:index'))
        self.assertNotIn('buser1234@yahoo.com', str(response.content))

    def save_user(self, username, email):
        user = self.create_user(email, username)
        user.save()

    def create_user(self, email, username):
        user = User(username=username, email=email, is_superuser=False,  is_active=True)
        user.set_password('passphrase')
        return user

    def superuserLoggedIn(self, username, email):
        self.create_superuser(username=username, email=email)
        login, response = self.loggedIn(username=username, email=email)
        return login, response

    def loggedIn(self, username, email):
        response = self.client.get('/account/login/')
        login = self.client.login(username=username, email=email, password='passphrase')
        return login, response

    def create_superuser(self, username, email):
        user = User(username=username, email=email, is_superuser=True, is_active=True)
        user.set_password('passphrase')  # can't set above because of hashing
        user.save()                      # needed to save to temporary test db
