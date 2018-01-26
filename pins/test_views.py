from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from pins.models import Category


class CategoryViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.superuserLoggedIn(username='auser', email='auser1234@yahoo.com')

    def test_a_list_of_categories_is_on_backend(self):
        Category.objects.create(title='categories one')
        Category.objects.create(title='categories two')
        response = self.client.get(reverse('backend:index'))
        self.assertIn('categories one', str(response.content))
        self.assertIn('categories two', str(response.content))

    def test_create_form_exists(self):
        response = self.client.get(reverse('backend:index'))
        self.assertIn('Create Category', str(response.content))

    def test_user_can_create_category(self):
        response = self.client.get(reverse('backend:index'))
        self.assertNotIn('category one', str(response.content))
        self.client.post('/backend/categories/create/', data={'title': 'category one'})
        response = self.client.get(reverse('backend:index'))
        self.assertIn('category one', str(response.content))

    def test_user_can_edit_category(self):
        Category.objects.create(title='category one')
        self.client.post('/backend/categories/edit/category-one/', data={'title':'category two'})
        response = self.client.get(reverse('backend:index'))
        self.assertIn('category two', str(response.content))

    def test_user_can_delete_category(self):
        Category.objects.create(title='category one')
        response = self.client.get(reverse('backend:index'))
        self.assertIn('category one', str(response.content))
        self.client.post('/backend/categories/delete/category-one/')
        response = self.client.get(reverse('backend:index'))
        self.assertNotIn('category one', str(response.content))

    def create_superuser(self, username, email):
        user = User(username=username, email='', is_superuser=True)
        user.set_password('passphrase')  # can't set above because of hashing
        user.save()  # needed to save to temporary test db

    def superuserLoggedIn(self, username, email):
        self.create_superuser(username=username, email=email)
        login, response = self.loggedIn(username=username, email=email)
        return login, response

    def loggedIn(self, username, email):
        response = self.client.get('/login/')
        login = self.client.login(username=username, email=email, password='passphrase')
        return login, response


class PinViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home_page_template(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'home.html')

