from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm


class EditUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_password(self):
        return ""

