from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from pins.forms import CategoryForm, PinForm
from pins.models import Category, Pin


class CategoryFormTest(TestCase):

    def test_CategoryForm_valid(self):
        form = CategoryForm(data={'title':'category one'})
        self.assertTrue(form.is_valid())

    def test_CreatePinForm_valid(self):
        category_object = Category.objects.create(title="Amsterdam")
        category_object.save()
        category = Category.objects.get(pk=1)
        path = '/home/matt/Documents/Explorer/media/ImageTest/4904752316.jpg'
        image = SimpleUploadedFile(name='4904752316.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        note = 'a short description about the image'
        form = PinForm(data={'image':image, 'note':note, 'category':category.id})
        self.assertTrue(form.is_valid(), form.errors)

    def test_EditPinForm_valid(self):
        Category.objects.create(title="Amsterdam")
        Category.objects.create(title="Rotterdam")
        category = Category.objects.get(pk=1)
        path = '/home/matt/Documents/Explorer/media/ImageTest/4904752316.jpg'
        image = SimpleUploadedFile(name='4904752316.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        note = 'a short description about the image'
        Pin.objects.create(image=image, note=note, category=category)
        # edit
        pin = Pin.objects.get(slug='4904752316')
        category = Category.objects.get(pk=2)
        # change data
        image = pin.image
        note = 'new description'
        category = category.id
        form = PinForm(data={'image':image, 'note':note, 'category': category})
        self.assertTrue(form.is_valid(), form.errors)