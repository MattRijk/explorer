from django.test import LiveServerTestCase
from selenium import webdriver
import requests


class IndexPageFunctionalTests(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.PhantomJS('/usr/local/bin/phantomjs')
        self.browser.set_window_size(1120, 550)
        self.response = requests.get(self.live_server_url + '/')
        self.page = str(self.response.content)

    def test_title_on_index_page(self):
        self.assertIn('home page',self.page)

    def TearDown(self):
        self.browser.close()



