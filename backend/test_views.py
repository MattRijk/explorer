from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
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
        self.assertRedirects(redirect, expected_url=reverse('backend:categories'), status_code=302, target_status_code=200)
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
        self.assertContains(response, '<a href="%s">Pins</a>' % reverse("backend:pins_list"), html=True)

    def test_create_form_exists(self):
        response = self.client.get(reverse('backend:index'))
        self.assertContains(response, '<a href="%s">Create Pin</a>' % reverse("backend:createPin"), html=True)

    def test_pin_list_template_exists(self):
        response = self.client.get(reverse('backend:pins_list'))
        self.assertEqual(200, response.status_code)

    def test_pin_list_has_a_list_of_pins(self):
        category = Category.objects.create(title='Amsterdam')
        title1 = '1934 a view of the kijkduinstraat in amsterdam-west'
        path = '/home/matt/Documents/Explorer/media/ImageTest/4904795089.jpg'
        note = 'a short description about the image'
        from django.core.files.uploadedfile import SimpleUploadedFile
        image1 = SimpleUploadedFile(name='4904795089.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        title2 = '1936 a view of the leidsestraat in amsterdam'
        path = '/home/matt/Documents/Explorer/media/ImageTest/4904777907.jpg'
        from django.core.files.uploadedfile import SimpleUploadedFile
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
        self.assertNotIn('4904795089', str(response.content))
        category = Category.objects.create(title='Amsterdam')
        title = '1930 a view of the zwanenburgwal in amsterdam'
        path = '/home/matt/Documents/Explorer/media/ImageTest/4904795016.jpg'
        image = SimpleUploadedFile(name='4904795016.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        note = 'a short description about the image'
        redirect = self.client.post('/backend/pins/create/',data = {'title':title,'image':image, 'note':note, 'category':category.id})
        self.assertRedirects(redirect, expected_url=reverse('backend:pins_list'), status_code=302, target_status_code=200)
        response = self.client.get(reverse('backend:pins_list'))
        self.assertIn('1930 a view of the zwanenburgwal in amsterdam', str(response.content))
        self.assertTemplateUsed(response, 'pins/pins_list.html')


    def test_pin_edit_view(self):
        # create two categories
        Category.objects.create(title='Amsterdam')
        Category.objects.create(title='Rotterdam')
        # pin 1
        title = '1936 A Street in Amsterdam'
        path = '/home/matt/Documents/Explorer/media/ImageTest/4904742124.jpg'
        image = SimpleUploadedFile(name='4904742124.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        note = 'a short description about the image'
        category = Category.objects.get(pk=1)
        # create pin
        p = Pin.objects.create(title=title, image=image, note=note, category=category)
        p.save()

        pin = Pin.objects.get(slug='1936-a-street-in-amsterdam') # don't edit image
        category = Category.objects.get(pk=2)
        title = '1934 a view of the kijkduinstraat in amsterdam-west'
        redirect = self.client.post('/backend/pins/edit/1936-a-street-in-amsterdam/',
            data = {'title':title,'image':pin.image, 'note':'A new entry', 'category':category.id})
        self.assertRedirects(redirect, expected_url=reverse('backend:pins_list'), status_code=302,
                             target_status_code=200)
        # pin 2
        title = '1935 a view of the zaandammerplein'
        path = '/home/matt/Documents/Explorer/media/ImageTest/4904777907.jpg'
        image = SimpleUploadedFile(name='.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        note = '1935 a view of the zaandammerplein is a square in the spaarndammerbuurt neighborhood of amsterdam-west'
        category = Category.objects.get(pk=1)
        pin = Pin.objects.create(title=title, image=image, note=note, category=category)

        # edit pin
        category = Category.objects.get(pk=2)
        redirect = self.client.post('/backend/pins/edit/1934-a-view-of-the-kijkduinstraat-in-amsterdam-west/',
            data = {'title':title,'image':pin.image,'note':note,'category':category.id})
        self.assertRedirects(redirect, expected_url=reverse('backend:pins_list'), status_code=302,
                             target_status_code=200)
        response = self.client.get(reverse('backend:pins_list'))
        self.assertIn('1935-a-view-of-the-zaandammerplein', str(response.content))
        self.assertTemplateUsed(response, 'pins/pins_list.html')





