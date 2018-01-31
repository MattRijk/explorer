from django.forms import ModelForm, ModelChoiceField, Select
from pins.models import Category, Pin


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('title',)


class PinForm(ModelForm):
    class Meta:
        model = Pin
        category = ModelChoiceField(queryset=Category.objects.all().distinct(),widget=Select())
        fields = ('image', 'note', 'category')

    def __init__(self, *args, **kwargs):
        super(PinForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
