from django.test import TestCase
from pins.forms import CategoryForm, PinForm
from pins.models import Category


class CategoryFormTest(TestCase):

    def test_CategoryForm_valid(self):
        form = CategoryForm(data={'title':'category one'})
        self.assertTrue(form.is_valid())

    def test_PinForm_valid(self):
        object = Category.objects.create(title="Amsterdam")
        object.save()
        category = Category.objects.get(pk=1)
        path = '/home/matt/Documents/Explorer/media/ImageTest/4904752316.jpg'
        from django.core.files.uploadedfile import SimpleUploadedFile
        image = SimpleUploadedFile(name='4904752316.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        note = 'a short description about the image'
        form = PinForm(data={'image':image, 'note':note, 'category':category.id})
        self.assertTrue(form.is_valid(), form.errors)