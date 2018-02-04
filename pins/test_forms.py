from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from pins.forms import CategoryForm, PinForm
from pins.models import Category, Pin


class CategoryFormTest(TestCase):

    def test_CategoryForm_valid(self):
        form = CategoryForm(data={'title':'category one'})
        self.assertTrue(form.is_valid())

class PinFormTest(TestCase):
    def test_CreatePinForm_valid(self):
        category_object = Category.objects.create(title="Amsterdam")
        category_object.save()
        category = Category.objects.get(pk=1)
        title = '1938 a view of the lekstraat in the rivierenbuurt of amsterdam'
        path = '/home/matt/Documents/Explorer/media/ImageTest/4904752316.jpg'
        image = SimpleUploadedFile(name='4904752316.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        note = 'a short description about the image'
        form = PinForm(data={'title':title, 'image':image, 'note':note, 'category':category.id})
        self.assertTrue(form.is_valid(), form.errors)

    def test_EditPinForm_valid(self):
        Category.objects.create(title="Amsterdam")
        Category.objects.create(title="Rotterdam")
        category = Category.objects.get(pk=1)
        title = '1934 a view of the kijkduinstraat in amsterdam-west'
        path = '/home/matt/Documents/Explorer/media/ImageTest/4904752316.jpg'
        image = SimpleUploadedFile(name='4904752316.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        note = 'a short description about the image'
        Pin.objects.create(title=title,image=image, note=note, category=category)
        # edit
        pin = Pin.objects.get(slug='1934-a-view-of-the-kijkduinstraat-in-amsterdam-west')
        category = Category.objects.get(pk=2)
        # change data
        title = '1935 a view of the leidseplein in amsterdam'
        image = pin.image
        note = 'new description'
        category = category.id
        form = PinForm(data={'title':title,'image':image, 'note':note, 'category': category})
        self.assertTrue(form.is_valid(), form.errors)