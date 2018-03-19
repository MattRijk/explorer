from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from pins.forms import CategoryForm, PinForm
from pins.models import Category, Pin

IMAGE_TEST_PATH = '/home/matt/Documents/Explorer/ImageTest/images/'
CATEGORY_IMAGE_TEST_PATH = '/home/matt/Documents/Explorer/ImageTest/categories/'

class CategoryFormTest(TestCase):
    def test_CategoryForm_valid(self):
        path = '%scategory_one.jpg' % CATEGORY_IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='category_one.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        description='a short category description'
        form = CategoryForm(data={'title':'category one', 'image':image, 'description':description})
        self.assertTrue(form.is_valid())


#'title','image','note','source', 'category','tags'
class PinFormTest(TestCase):
    def test_PinForm_valid(self):
        path = '%scategory_one.jpg' % CATEGORY_IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='category_one.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        description='a short category description'
        category_object=Category.objects.create(title='category one',image=image,
                                                description=description)
        category_object.save()
        category = Category.objects.get(pk=1)
        title = '1938 a view of the lekstraat in the rivierenbuurt of amsterdam'
        path = '%s4904752316.jpg' % IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='4904752316.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        note = 'a short description about the image'
        source = 'http://www.google.com'
        tags = 'one, two, three'

        form = PinForm(data={'title':title, 'image':image, 'note':note,
                             'source':source, 'category':category.pk, 'tags':tags})
        self.assertTrue(form.is_valid(), form.errors)

    def test_PinForm_valid(self):
        path = '%scategory_one.jpg' % CATEGORY_IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='category_one.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        description='a short category description'
        category_object=Category.objects.create(title='category one',image=image,
                                                description=description)
        category_object.save()
        category = Category.objects.get(pk=1)
        title = '1938 a view of the lekstraat in the rivierenbuurt of amsterdam'
        path = '%s4904752316.jpg' % IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='4904752316.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        note = 'a short description about the image'
        source = 'http://www.google.com'
        tags = 'one, two, three'

        form = PinForm(data={'title':title, 'image':image, 'note':note,
                             'source':source, 'category':category.pk, 'tags':tags})
        self.assertTrue(form.is_valid(), form.errors)

    def test_PinForm_valid(self):
        path = '%scategory_one.jpg' % CATEGORY_IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='category_one.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        description='a short category description'
        category_object=Category.objects.create(title='category one',image=image,
                                                description=description)
        category_object.save()
        category = Category.objects.get(pk=1)
        title = '1938 a view of the lekstraat in the rivierenbuurt of amsterdam'
        path = '%s4904752316.jpg' % IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='4904752316.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        note = 'a short description about the image'
        source = 'http://www.google.com'
        tags = 'one, two, three'

        form = PinForm(data={'title':title, 'image':image, 'note':note,
                             'source':source, 'category':category.pk, 'tags':tags})
        self.assertTrue(form.is_valid(), form.errors)

    def test_PinForm_invalid(self):
        path = '%scategory_one.jpg' % CATEGORY_IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='category_one.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        description='a short category description'
        category_object=Category.objects.create(title='category one',image=image,
                                                description=description)
        category_object.save()
        category = Category.objects.get(pk=1)
        title = '1938 a view of the lekstraat in the rivierenbuurt of amsterdam'
        path = '%s4904752316.jpg' % IMAGE_TEST_PATH
        image = SimpleUploadedFile(name='4904752316.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        note = 'a short description about the image'
        source = 'http://www.google.com'
        tags = 'one, two, three'

        form = PinForm(data={'title':'', 'image':image, 'note':note,
                             'source':'', 'category':'', 'tags':tags})
        self.assertFalse(form.is_valid(), form.errors)


