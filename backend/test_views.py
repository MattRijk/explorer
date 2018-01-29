from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from pins.models import Category, Pin


class AdminCategoryViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.superuserLoggedIn(username='auser', email='auser1234@yahoo.com')

    def test_can_get_category_list_template(self):
        response = self.client.get(reverse('backend:categories'))
        self.assertTemplateUsed(response, 'categories/category_list.html')

    def test_category_list_link(self):
        response = self.client.get(reverse('backend:index'))
        self.assertContains(response, '<a href="%s">Categories</a>' % reverse("backend:categories"), html=True)

    def test_category_create_link_exists(self):
        response = self.client.get(reverse('backend:index'))
        self.assertContains(response, '<a href="%s">Create Category</a>' % reverse("backend:createCategory"), html=True)

    def test_category_list_view(self):
        Category.objects.create(title='category one')
        Category.objects.create(title='category two')
        response = self.client.get(reverse('backend:categories'))
        self.assertIn('category one', str(response.content))
        self.assertIn('category two', str(response.content))

    def test_category_create_view(self):
        response = self.client.get(reverse('backend:categories'))
        self.assertNotIn('category one', str(response.content))
        redirect = self.client.post('/backend/categories/create/', data={'title': 'category one'})
        self.assertRedirects(redirect, expected_url=reverse('backend:index'), status_code=302, target_status_code=200)
        response = self.client.get(reverse('backend:categories'))
        self.assertIn('category one', str(response.content))
        self.assertTemplateUsed(response, 'categories/category_list.html')

    def test_category_edit_view(self):
        Category.objects.create(title='category one')
        redirect = self.client.post('/backend/categories/edit/category-one/', data={'title':'category two'})
        self.assertRedirects(redirect, expected_url=reverse('backend:categories'), status_code=302, target_status_code=200)
        response = self.client.get(reverse('backend:categories'))
        self.assertIn('category two', str(response.content))
        self.assertTemplateUsed(response, 'categories/category_list.html')

    def test_category_delete_view(self):
        Category.objects.create(title='category one')
        response = self.client.get(reverse('backend:categories'))
        self.assertIn('category one', str(response.content))
        redirect = self.client.post('/backend/categories/delete/category-one/')
        self.assertRedirects(redirect, expected_url=reverse('backend:categories'),status_code=302, target_status_code=200)
        response = self.client.get(reverse('backend:categories'))
        self.assertNotIn('category one', str(response.content))
        self.assertTemplateUsed(response, 'categories/category_list.html')

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


class DashboardPinViewTest(TestCase):

    def test_pins_link_on_dashboard(self):
        response = self.client.get(reverse('backend:index'))
        self.assertContains(response, '<a href="%s">Pins</a>' % reverse("backend:pins"), html=True)

    def test_create_form_exists(self):
        response = self.client.get(reverse('backend:index'))
        self.assertContains(response, '<a href="%s">Create Pin</a>' % reverse("backend:createPin"), html=True)

    def test_pin_list_view(self):