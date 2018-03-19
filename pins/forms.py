import io
import csv
from django import forms
from django.forms import ModelForm, ModelChoiceField, Select, Form, FileField
from pins.models import Category, Pin


class SearchForm(forms.Form):
    query = forms.CharField()

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('title','image','description')

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False

class PinForm(ModelForm):
    class Meta:
        model = Pin
        category = ModelChoiceField(queryset=Category.objects.all().distinct(),widget=Select())
        fields = ('title','image','note','source', 'category','tags')

    def __init__(self, *args, **kwargs):
        super(PinForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False


class DataForm(Form):
    data_file = FileField()

    def process_data(self):
        csv_ = io.TextIOWrapper(self.cleaned_data['data_file'].file)
        reader = csv.DictReader(csv_)

        for cursor in reader:
            category_id = Category.objects.get(pk=cursor['category'])
            image_path= cursor['image']
            pin = Pin.objects.create(title=cursor['title'], slug=cursor['slug'], published=cursor['published'], note=cursor['note'], source=cursor['source'], image=image_path, category=category_id)                      
            if len(cursor['tag1']) > 0:
                pin.tags.add(cursor['tag1'].strip())
            if len(cursor['tag2']) > 0:
                pin.tags.add(cursor['tag2'].strip())
            if len(cursor['tag3']) > 0:
                pin.tags.add(cursor['tag3'].strip())
            if len(cursor['tag4']) > 0:
                pin.tags.add(cursor['tag4'].strip())

        csv_.close()


