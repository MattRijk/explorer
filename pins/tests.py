from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User


class PinsModelTestCase(TestCase): pass


class PinViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home_page_template(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'home.html')



















