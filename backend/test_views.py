from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from pins.models import Category, Pin
from Explorer.settings import BASE_DIR

IMAGE_TEST_PATH = ''.join([BASE_DIR, '/ImageTest/images/'])
CATEGORY_IMAGE_TEST_PATH = ''.join([BASE_DIR,'/ImageTest/categories/'])

class AdminCategoryViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.superuserLoggedIn(username='auser', email='auser1234@yahoo.com')

    def test_can_get_category_list_template(self):
        response = self.client.get(reverse('backend:admin_category_list'))
        self.assertTemplateUsed(response, 'categories/admin_category_list.html')

    def test_category_list_link(self):
        response = self.client.get(reverse('backend:index'))
        self.assertIn('<a href="%s">Categories</a>' % reverse("backend:admin_category_list"), str(response.content))

    def test_category_create_link_exists(self):
        response = self.client.get(reverse('backend:index'))
        self.assertIn('<a href="%s" class="add-item">Add Category</a>' % reverse("backend:createCategory"), str(response.content))

    def test_category_list_view(self):
        Category.objects.create(title='category one')
        Category.objects.create(title='category two')
        response = self.client.get(reverse('backend:admin_category_list'))
        self.assertIn('category one', str(response.content))
        self.assertIn('category two', str(response.content))

    def test_category_create_view(self):
        response = self.client.get(reverse('backend:admin_category_list'))
        self.assertNotIn('category three', str(response.content))
        path = '%scategory_three.jpg' % CATEGORY_IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='category_three.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        description = 'a short category description.'
        redirect = self.client.post('/backend/categories/create/',
          data={'title':'category three', 'image':image, 'description':description})
        self.assertRedirects(redirect, expected_url=reverse('backend:admin_category_list'),status_code=302,target_status_code=200)
        response = self.client.get(reverse('backend:admin_category_list'))
        self.assertContains(response, 'category three')
        self.assertTemplateUsed(response, 'categories/admin_category_list.html')

    def test_category_edit_view(self):
        path = '%scategory_one.jpg' % CATEGORY_IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='category_one.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        description = 'a short category description.'
        Category.objects.create(title='category one', image=image, description=description)
        title = 'category two'
        path = '%scategory_two.jpg' % CATEGORY_IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='category_two.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        redirect = self.client.post('/backend/categories/edit/category-one/',
          data={'title':title,'image':image,'description':'another description'})
        self.assertRedirects(redirect, expected_url=reverse('backend:admin_category_list'),status_code=302,target_status_code=200)
        response = self.client.get(reverse('backend:admin_category_list'))
        self.assertIn('category two', str(response.content))
        self.assertTemplateUsed(response, 'categories/admin_category_list.html')

    def test_category_delete_view(self):
        Category.objects.create(title='category one')
        response = self.client.get(reverse('backend:admin_category_list'))
        self.assertIn('category one', str(response.content))
        redirect = self.client.post('/backend/categories/delete/category-one/')
        self.assertRedirects(redirect, expected_url=reverse('backend:admin_category_list'),status_code=302, target_status_code=200)
        response = self.client.get(reverse('backend:admin_category_list'))
        self.assertNotIn('category one', str(response.content))
        self.assertTemplateUsed(response, 'categories/admin_category_list.html')

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


class AdminPinViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.superuserLoggedIn(username='auser', email='auser1234@yahoo.com')

    def test_pins_link_on_dashboard(self):
        response = self.client.get(reverse('backend:index'))
        self.assertIn('<a href="%s">Pins</a>' % reverse("backend:pins_list"), str(response.content))

    def test_create_form_exists(self):
        response = self.client.get(reverse('backend:index'))
        self.assertIn('<a href="%s" class="add-item">Add Pin</a>' % reverse("backend:createPin"), str(response.content))
        self.assertTemplateUsed('backend/index.html')

    def test_pin_list_template_exists(self):
        response = self.client.get(reverse('backend:pins_list'))
        self.assertEqual(200, response.status_code)

    def test_pin_list_has_a_list_of_pins(self):
        category = Category.objects.create(title='Amsterdam')
        title1 = '1934 a view of the kijkduinstraat in amsterdam-west'
        path = '%s4904795089.jpg' % IMAGE_TEST_PATH
        note = 'a short description about the image'
        image1 = SimpleUploadedFile(name='4904795089.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        title2 = '1936 a view of the leidsestraat in amsterdam'
        path = '%s4904777907.jpg' % IMAGE_TEST_PATH
        image2 = SimpleUploadedFile(name='4904777907.jpg', content=open(path, 'rb').read(),
                                    content_type='image/jpeg')
        Pin.objects.create(title=title1,image=image1, note=note, category=category)
        Pin.objects.create(title=title2, image=image2, note=note, category=category)
        response = self.client.get(reverse('backend:pins_list'))
        self.assertIn('1934 a view of the kijkduinstraat in amsterdam-west', str(response.content))
        self.assertIn('1936 a view of the leidsestraat in amsterdam', str(response.content))

    def test_pins_form_template_exists(self):
        response = self.client.get(reverse('backend:createPin'))
        self.assertTemplateUsed(response, 'pins/pins_form.html')

    def test_pin_create_view(self):
        response = self.client.get(reverse('backend:pins_list'))
        self.assertNotIn('4904752316', str(response.content))
        path = '%scategory_one.jpg' % CATEGORY_IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='category_one.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        description = 'a short category description.'
        Category.objects.create(title='category one', image=image, description=description)
        category = Category.objects.get(slug='category-one')
        title = '1930 a view of the zwanenburgwal in amsterdam'
        path = '%s4904752316.jpg' % IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='4904752316.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        note = 'a short description about the image'
        source = 'http://www.google.com'
        tags = 'one, two, three'
        data = {'title': title, 'image': image, 'note': note,
                'source': source, 'category': category.id, 'tags': tags}
        redirect = self.client.post('/backend/pins/create/', data=data)
        self.assertRedirects(redirect, expected_url=reverse('backend:pins_list'),status_code=302,target_status_code=200)
        response = self.client.get(reverse('backend:pins_list'))
        self.assertIn('1930 a view of the zwanenburgwal in amsterdam', str(response.content))
        self.assertTemplateUsed(response, 'pins/pins_list.html')

    # def test_pin_edit_view(self):
    #     path = '%scategory_one.jpg' % CATEGORY_IMAGE_TEST_PATH
    #     image = SimpleUploadedFile(name='category_one.jpg', content=open(path, 'rb').read(),
    #                                content_type='image/jpeg')
    #     description = 'a short category description.'
    #     Category.objects.create(title='category one', image=image, description=description)
    #
    #     # create pin
    #     title = '1936 A Street in Amsterdam'
    #     path = '%s4904742524.jpg' % IMAGE_TEST_PATH
    #     image = SimpleUploadedFile(name='4904742524.jpg', content=open(path, 'rb').read(),
    #                                content_type='image/jpeg')
    #     note = 'a short description about the image'
    #     source = 'http://www.google.com'
    #     tags = 'one, two, three'
    #
    #     category = Category.objects.get(slug='category-one')
    #     Pin.objects.create(title=title, image=image, note=note, source=source, category=category, tags=tags)
    #
    #     # get pin
    #     #pin = Pin.objects.get(slug='1936-a-street-in-amsterdam') # don't edit image
    #
    #     new_image = SimpleUploadedFile(name='4904720037.jpg', content=open(path, 'rb').read(),
    #                                    content_type='image/jpeg')
    #     redirect = self.client.post('/backend/pins/edit/1936-a-street-in-amsterdam/',
    #       data = {'title':'new title','image':new_image, 'note':'A new entry', 'source':'http://www.aol.com',
    #               'category':'', tags:'one'})
    #     self.assertRedirects(redirect, expected_url=reverse('backend:pins_list'), status_code=302,
    #                          target_status_code=200)
    #     response = self.client.get(reverse('backend:pins_list'))
    #     self.assertIn('new-title', str(response.content))
    #     self.assertTemplateUsed(response, 'pins/pins_list.html')

    def test_pin_delete_view(self):
        Category.objects.create(title='Amsterdam')
        title = '1936 A Street in Amsterdam'
        path = '%s4904742524.jpg' % IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='4904742524.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        note = 'a short description about the image'
        category = Category.objects.get(pk=1)
        p = Pin.objects.create(title=title, image=image, note=note, category=category)
        p.save()
        response = self.client.get(reverse('backend:pins_list'))
        self.assertIn('1936-a-street-in-amsterdam', str(response.content))
        redirect = self.client.post('/backend/pins/delete/1936-a-street-in-amsterdam/')
        self.assertRedirects(redirect, expected_url=reverse('backend:pins_list'),status_code=302, target_status_code=200)
        response = self.client.get(reverse('backend:pins_list'))
        self.assertNotIn('1936-a-street-in-amsterdam', str(response.content))
        self.assertTemplateUsed(response, 'pins/pins_list.html')

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






