from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class EditUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_superuser')
    def clean_password(self):
        return ""

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_superuser')
    def clean_password(self):
        return ""