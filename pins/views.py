from django.shortcuts import render
from django.contrib.auth.models import User


def home(requests):
    return render(requests, template_name='home.html', context={})


