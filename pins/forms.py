from django.forms import ModelForm
from pins.models import Category


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('title',)