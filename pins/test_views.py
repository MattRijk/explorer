from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse, resolve
from pins.models import Category, Pin
from explorer.settings import BASE_DIR


IMAGE_TEST_PATH = ''.join([BASE_DIR, '/ImageTest/images/'])
CATEGORY_IMAGE_TEST_PATH = ''.join([BASE_DIR,'/ImageTest/categories/'])

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
        self.assertIn('<a href="%s">Categories</a>' % reverse("category_list"), str(response.content))
        self.assertTemplateUsed('home.html')

    # get_rendered keeps printing when running tests
    def test_category_detail_get_absolute_url(self):
        path = '%scategory_one.jpg' % CATEGORY_IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='category_one.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        description='a short category description'
        category = Category.objects.create(title='category one', image=image, description=description)
        response = self.client.get(category.get_absolute_url())
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
        path = '%scategory_one.jpg' % CATEGORY_IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='category_one.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        description='a short category description'
        Category.objects.create(title='category one', image=image, description=description)
        category = Category.objects.get(title='category one')

        title = '1936 A Street in Amsterdam'
        path = '%s4904741066.jpg' % IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='4904741066.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        note = 'a short description about the image'
        pin = Pin.objects.create(title=title, image=image, note=note, category=category)
        pin.tags.add('amsterdam', 'rotterdam')
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
        pin.tags.add('amsterdam', 'rotterdam')
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
        pin.tags.add('amsterdam', 'rotterdam')
        response = self.client.get(pin.get_image_url())
        self.assertEqual(response.status_code, 200)

    def test_pin_list_view(self):
        Category.objects.create(title='category one')
        c1 = Category.objects.get(title='category one')
        title = '1936 A Street in Amsterdam'
        path = '%s4904742524.jpg' % IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='4904742524.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        note = 'a short description about a street in Amsterdam'
        pin_1 = Pin.objects.create(title=title, image=image, note=note, category=c1)
        pin_1.tags.add('amsterdam', 'rotterdam')
        Category.objects.create(title='category two')
        c2 = Category.objects.get(title='category two')
        title = '1938 A Lake in Amsterdam'
        path = '%s4904741066.jpg' % IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='4904741066.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        note = 'a short description about a lake near Amsterdam'
        pin_2 = Pin.objects.create(title=title, image=image, note=note, category=c2)
        pin_2.tags.add('amsterdam', 'rotterdam')
        # pin 3
        Category.objects.create(title='category three')
        category = Category.objects.get(title='category three')
        title = '1942 after ww2 in Amsterdam'
        path = '%s4904736510.jpg' % IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='4904736510.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        note = 'a short description about ww2 in Amsterdam'
        source = 'http://www.vintag.es/2015/11/amsterdam-flee-market-ca-1950s.html'
        pin_3 = Pin.objects.create(title=title, image=image, note=note, source=source, category=category)
        pin_3.tags.add('amsterdam', 'rotterdam')
        response = self.client.get(reverse('pins:all_images'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'pins/all_images.html')
        self.assertContains(response, '/image/1936-a-street-in-amsterdam/')
        self.assertContains(response, '/image/1938-a-lake-in-amsterdam')
        self.assertContains(response, '/image/1942-after-ww2-in-amsterdam')



