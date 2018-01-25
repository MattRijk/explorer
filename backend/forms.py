from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.forms import ModelForm
from pins.models import Category


class EditUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_password(self):
        return ""


class EditCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('title',)