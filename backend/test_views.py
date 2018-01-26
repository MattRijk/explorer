from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


def create_superuser(request):
    form = None