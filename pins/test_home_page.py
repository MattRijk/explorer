from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from pins.models import Category, Pin

class HomePageViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_success(self):
        response = self.client.get(reverse('homepage'))
        self.assertIn('home page', str(response.content))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'home.html')

    def test_category_list_exist_on_home_page(self):
        Category.objects.create(title='category one')
        Category.objects.create(title='category two')
        response = self.client.get(reverse('homepage'))
        self.assertEqual(200, response.status_code)
        self.assertIn('category one', str(response.content))
        self.assertIn('category two', str(response.content))
        self.assertIn('category one', [category.title for category in
                                       response.context['categories']])



    # get pin image to display
    def test_can_get_image(self):
         Category.objects.create(title='category one')
         category = Category.objects.get(title='category one')
         title = '1936 A Street in Amsterdam'
         path = '/home/matt/Documents/Explorer/media/ImageTest/4904736510.jpg'
         image = SimpleUploadedFile(name='4904736510.jpg', content=open(path, 'rb').read(),
                                    content_type='image/jpeg')
         note = 'a short description about the image'
         Pin.objects.create(title=title, image=image, note=note, category=category)
         response = self.client.get(reverse('homepage'))
         self.assertEqual(200, response.status_code)
         queryset = [pin.image.url for category in
                     response.context['categories']
                     for pin in category.pin_set.all()
         ]
         self.assertEqual('4904736510', queryset[0].strip('/images/uploads/')[:10])









