from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from pins.models import Category, Pin


class CategoryViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_category_list_on_home_page(self):
        Category.objects.create(title='category one')
        Category.objects.create(title='category two')
        response = self.client.get(reverse('home_page'))
        self.assertContains(response, 'category one')
        self.assertContains(response, 'category two')

class PinViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home_page_template(self):
        response = self.client.get(reverse('home_page'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'home.html')

    def test_pin_detail_get_absolute_url(self):
        Category.objects.create(title='category one')
        category = Category.objects.get(title='category one')
        title = '1936 A Street in Amsterdam'
        path = '/home/matt/Documents/Explorer/media/ImageTest/4904741066.jpg'
        image = SimpleUploadedFile(name='4904741066.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        note = 'a short description about the image'
        pin = Pin.objects.create(title=title, image=image, note=note, category=category)
        response = self.client.get(pin.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['pin'].slug, '1936-a-street-in-amsterdam')

    def test_pin_detail_view_with_slug(self):
        Category.objects.create(title='category one')
        category = Category.objects.get(title='category one')
        title = '1936 A Street in Amsterdam'
        path = '/home/matt/Documents/Explorer/media/ImageTest/4904741066.jpg'
        image = SimpleUploadedFile(name='4904741066.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        note = 'a short description about the image'
        pin = Pin.objects.create(title=title, image=image, note=note, category=category)
        response = self.client.get('/%s/%s/' % (category.slug, pin.slug,))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pins/pin_detail.html')

