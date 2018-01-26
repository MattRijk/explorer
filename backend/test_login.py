from django.test import TestCase, Client
from django.contrib.auth.models import User


class SuperUserLoginTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.superUserName = 'auser'
        self.superUserEmail = 'auser1234@yahoo.com'

    def test_dashboard_template(self):
        response = self.client.get('/backend/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'index.html')

    def test_superuser_can_login_to_dashboard(self):
        login, response = self.superuserLoggedIn(username= self.superUserName,
                                                    email= self.superUserEmail)
        self.assertEqual(200, response.status_code)
        self.assertTrue(login)
        self.assertTemplateUsed('index.html')

    def test_username_exists_on_dashboard(self):
        login, response = self.superuserLoggedIn(username= self.superUserName,
                                                    email= self.superUserEmail)
        self.save_active_user(username='buser', email='buser1234@yahoo.com')
        self.assertEqual(200, response.status_code)
        self.assertTrue(login)
        self.assertTemplateUsed('index.html')

        response = self.client.get('/backend/')
        self.assertIn('buser', str(response.content))

    def test_superuser_can_edit_active_user_on_dashboard(self):
        login, response = self.superuserLoggedIn(username= self.superUserName,
                                                    email= self.superUserEmail)
        self.save_active_user(username='buser', email='buser1234@yahoo.com')
        self.assertEqual(200, response.status_code)
        self.assertTrue(login)
        self.assertTemplateUsed('index.html')
        response = self.client.get('/backend/')
        self.assertIn('buser', str(response.content))
        self.assertIn('buser1234@yahoo.com', str(response.content))
        self.assertIn('Edit', str(response.content))
        self.client.post('/backend/user/edit/2',
             data={'username':'buser', 'email':'buser5555@yahoo.com', 'password':'passphrase'})
        response = self.client.get('/backend/')
        self.assertIn('buser5555@yahoo.com', str(response.content))

    def test_superuser_can_delete_active_user_on_dashboard(self):
        login, response = self.superuserLoggedIn(username= self.superUserName,
                                                    email= self.superUserEmail)
        self.save_active_user(username='buser', email='buser1234@yahoo.com')
        self.assertEqual(200, response.status_code)
        self.assertTrue(login)
        self.assertTemplateUsed('index.html')
        response = self.client.get('/backend/')
        self.assertIn('buser', str(response.content))
        self.assertIn('buser1234@yahoo.com', str(response.content))
        self.assertIn('Delete', str(response.content))
        self.client.post('/backend/user/delete/2')
        response = self.client.get('/backend/')
        self.assertNotIn('buser1234@yahoo.com', str(response.content))

    def save_active_user(self, username, email):
        user = self.create_active_user(email, username)
        user.save()

    def create_active_user(self, email, username):
        user = User(username=username, email=email, is_active=True)
        user.set_password('passphrase')
        return user

    def superuserLoggedIn(self, username, email):
        self.create_superuser(username=username, email=email)
        login, response = self.loggedIn(username=username, email=email)
        return login, response

    def loggedIn(self, username, email):
        response = self.client.get('/login/')
        login = self.client.login(username=username, email=email, password='passphrase')
        return login, response

    def create_superuser(self, username, email):
        user = User(username=username, email=email, is_superuser=True)
        user.set_password('passphrase')  # can't set above because of hashing
        user.save()                      # needed to save to temporary test db





