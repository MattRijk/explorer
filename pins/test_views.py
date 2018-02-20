from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse, resolve
from pins.models import Category, Pin

IMAGE_TEST_PATH = '/home/matt/Documents/Explorer/ImageTest/images/'
CATEGORY_IMAGE_TEST_PATH = '/home/matt/Documents/Explorer/ImageTest/categories/'

class CategoryViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_category_list_on_home_page(self):
        path = '%scategory_one.jpg' % CATEGORY_IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='category_one.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        description='a short category description'
        Category.objects.create(title='category one', image=image, description=description)
        path = '%scategory_two.jpg' % CATEGORY_IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='category_two.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        Category.objects.create(title='category two', image=image, description=description)
        response = self.client.get(reverse('home_page'))
        self.assertContains(response, 'category one')
        self.assertContains(response, 'category two')

    def test_category_list_link_exists(self):
        response = self.client.get(reverse('home_page'))
        self.assertContains(response, '<a href="%s">Categories</a>' % reverse("category_list"), html=True)

    def test_category_detail_link_exists(self):
        path = '%scategory_one.jpg' % CATEGORY_IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='category_one.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        description='a short category description'
        Category.objects.create(title='category one', image=image, description=description)
        category = Category.objects.get(slug='category-one')
        response = self.client.get('/%s/' % (category.slug,))
        self.assertEqual(response.context['category'].slug, 'category-one')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'categories/category_detail.html')

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
        path = '%s4904741066.jpg' % IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='4904741066.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        note = 'a short description about the image'
        pin = Pin.objects.create(title=title, image=image, note=note, category=category)
        response = self.client.get(pin.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual([response.context['category'].slug,response.context['pin'].slug], ['category-one','1936-a-street-in-amsterdam',])

    def test_pin_detail_view_with_category_and_slug(self):
        Category.objects.create(title='category one')
        category = Category.objects.get(title='category one')
        title = '1936 A Street in Amsterdam'
        path = '%s4904741066.jpg' % IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='4904741066.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        note = 'a short description about the image'
        pin = Pin.objects.create(title=title, image=image, note=note, category=category)
        response = self.client.get('/%s/%s/' % (category.slug, pin.slug,))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pins/pin_detail.html')

    def test_pin_get_image_url(self):
        Category.objects.create(title='category one')
        category = Category.objects.get(title='category one')
        title = '1936 A Street in Amsterdam'
        path = '%s4904741066.jpg' % IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='4904741066.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        note = 'a short description about the image'
        pin = Pin.objects.create(title=title, image=image, note=note, category=category)
        response = self.client.get(pin.get_image_url())
        self.assertEqual(response.status_code, 200)

    # def test_pin_list_view(self):
    #     # pin 1
    #     Category.objects.create(title='category one')
    #     c1 = Category.objects.get(title='category one')
    #     title = '1936 A Street in Amsterdam'
    #     path = '/home/matt/Documents/Explorer/media/ImageTest/4904742524.jpg'
    #     image = SimpleUploadedFile(name='4904742524.jpg', content=open(path, 'rb').read(),
    #                                content_type='image/jpeg')
    #     note = 'a short description about a street in Amsterdam'
    #     Pin.objects.create(title=title, image=image, note=note, category=c1)
    #     # pin 2
    #     Category.objects.create(title='category two')
    #     c2 = Category.objects.get(title='category two')
    #     title = '1938 A Lake in Amsterdam'
    #     path = '/home/matt/Documents/Explorer/media/ImageTest/4904741066.jpg'
    #     image = SimpleUploadedFile(name='4904741066.jpg', content=open(path, 'rb').read(),
    #                                content_type='image/jpeg')
    #     note = 'a short description about a lake near Amsterdam'
    #     Pin.objects.create(title=title, image=image, note=note, category=c2)
    #     # pin 3
    #     Category.objects.create(title='category three')
    #     category = Category.objects.get(title='category three')
    #     title = '1942 after ww2 in Amsterdam'
    #     path = '/home/matt/Documents/Explorer/media/ImageTest/4904736510.jpg'
    #     image = SimpleUploadedFile(name='4904736510.jpg', content=open(path, 'rb').read(),
    #                                content_type='image/jpeg')
    #     note = 'a short description about ww2 in Amsterdam'
    #     Pin.objects.create(title=title, image=image, note=note, category=category)
    #     response = self.client.get(reverse('pins:all_images'))
    #     self.assertEqual(200, response.status_code)
    #     self.assertTemplateUsed(response, 'pins/all_images.html')
    #     self.assertContains(response, '1936 A Street in Amsterdam')
    #     self.assertContains(response, '1938 A Lake in Amsterdam')
    #     self.assertContains(response, '1942 after ww2 in Amsterdam')



