from django.test import TestCase, Client
from django.contrib.auth.models import User
from pins.models import Category


class SuperUserLoginTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_dashboard_template(self):
        response = self.client.get('/backend/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'index.html')

    def test_superuser_can_login_to_dashboard(self):
        user = User(username='auser', is_superuser=True)
        user.set_password('passphrase')  # can't set above because of hashing
        user.save()  # needed to save to temporary test db
        response = self.client.get('/login/')
        login = self.client.login(username='auser', password='passphrase')
        self.assertEqual(200, response.status_code)
        self.assertTrue(login)
        self.assertTemplateUsed('index.html')

    def test_username_exists_on_dashboard(self):
        superUser = User(username='auser', is_superuser=True)
        superUser.set_password('passphrase')  # can't set above because of hashing
        superUser.save()  # needed to save to temporary test db

        active_user = User(username='buser', is_active=True)
        active_user.set_password('passphrase')
        active_user.save()

        response = self.client.get('/login/')
        login = self.client.login(username='auser', password='passphrase')

        self.assertEqual(200, response.status_code)
        self.assertTrue(login)
        self.assertTemplateUsed('index.html')
        response = self.client.get('/backend/')
        self.assertIn('buser', str(response.content))

    def test_superuser_can_edit_active_user_on_dashboard(self):

        # create superuser
        superUser = User(username='auser', email='auser1234@yahoo.com', is_superuser=True)
        superUser.set_password('passphrase')  # can't set above because of hashing
        superUser.save()  # needed to save to temporary test db

        # create user
        user = User(username='buser', email='buser1234@yahoo.com', is_active=True)
        user.set_password('passphrase')
        user.save()

        response = self.client.get('/login/')
        login = self.client.login(username='auser', password='passphrase')

        # superuser logged in
        self.assertEqual(200, response.status_code)
        self.assertTrue(login)
        self.assertTemplateUsed('index.html')

        # check backend: user exists
        response = self.client.get('/backend/')
        self.assertIn('buser', str(response.content))
        self.assertIn('buser1234@yahoo.com', str(response.content))

        # check if superuser can edit active users email
        self.assertIn('Edit', str(response.content))

        self.client.post('/backend/user/edit/2', data={'username': 'buser', 'email': 'buser5555@yahoo.com', 'password':'passphrase'})

        response = self.client.get('/backend/')
        self.assertIn('buser5555@yahoo.com', str(response.content))

    def test_superuser_can_delete_active_user_on_dashboard(self):

        # create superuser
        superUser = User(username='auser', email='auser1234@yahoo.com', is_superuser=True)
        superUser.set_password('passphrase')  # can't set above because of hashing
        superUser.save()  # needed to save to temporary test db

        # create user
        user = User(username='buser', email='buser1234@yahoo.com', is_active=True)
        user.set_password('passphrase')
        user.save()

        response = self.client.get('/login/')
        login = self.client.login(username='auser', password='passphrase')

        # superuser logged in
        self.assertEqual(200, response.status_code)
        self.assertTrue(login)
        self.assertTemplateUsed('index.html')

        # check backend: user exists
        response = self.client.get('/backend/')
        self.assertIn('buser', str(response.content))
        self.assertIn('buser1234@yahoo.com', str(response.content))

        # check if superuser can edit active users email
        self.assertIn('Delete', str(response.content))

        self.client.post('/backend/user/delete/2') # delete record

        response = self.client.get('/backend/')
        self.assertNotIn('buser1234@yahoo.com', str(response.content))



class CategoryAdminTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_a_list_of_categories_is_on_backend(self):

        # create superuser
        superUser = User(username='auser', email='auser1234@yahoo.com', is_superuser=True)
        superUser.set_password('passphrase')
        superUser.save()

        self.client.get('/login/')
        self.client.login(username='auser', password='passphrase')

        categoryOne = Category.objects.create(title='category one')
        categoryOne.save()

        categoryTwo = Category.objects.create(title='category two')
        categoryTwo.save()

        response = self.client.get('/backend/')

        self.assertIn('category one', str(response.content))
        self.assertIn('category two', str(response.content))

    def test_user_can_edit_a_category(self):

        # category one
        superUser = User(username='auser', email='auser1234@yahoo.com', is_superuser=True)
        superUser.set_password('passphrase')
        superUser.save()

        self.client.get('/login/')
        self.client.login(username='auser', password='passphrase')

        categoryOne = Category.objects.create(title='category one')
        categoryOne.save()

        self.client.post('/backend/category/edit/category-one/', data={'title':'category two'})

        # category two
        response = self.client.get('/backend/')
        self.assertIn('category two', str(response.content))




