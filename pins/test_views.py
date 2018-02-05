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
        response = self.client.get(reverse('homepage'))
        self.assertIn('category one', str(response.content))
        self.assertIn('category two', str(response.content))

class PinViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home_page_template(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'home.html')

    def test_list_of_category_pins_on_home_page(self):
        Category.objects.create(title='category one')
        category = Category.objects.get(title='category one')
        title = '1936 A Street in Amsterdam'
        path = '/home/matt/Documents/Explorer/media/ImageTest/4904741066.jpg'
        image = SimpleUploadedFile(name='4904741066.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        note = 'a short description about the image'
        Pin.objects.create(title=title, image=image, note=note, category=category)
        response = self.client.get(reverse('homepage'))
        self.assertEqual(200, response.status_code)
        queryset = [pin.slug for category in
                 response.context['categories']
                 for pin in category.pin_set.all()
        ]
        self.assertIn('1936-a-street-in-amsterdam', queryset)

    def test_pin_detail_get_absolute_url(self):
        # create pin
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
        response = self.client.get('/pins/%s/' % (pin.slug,))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pins/pin_detail.html')

