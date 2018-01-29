from django.test import LiveServerTestCase
from selenium import webdriver
import requests


class DashboardUserFunctionalTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.PhantomJS('/usr/local/bin/phantomjs')
        self.browser.set_window_size(1120, 550)
        self.response = requests.get(self.live_server_url + '/backend/')

    def test_a_user_goes_to_the_signup_page(self):
        signup = requests.get(self.live_server_url + '/signup/')
        self.assertIn('signup', str(signup.content))

    def test_a_user_goes_to_the_login_page(self):
        login = requests.get(self.live_server_url + '/login/')
        self.assertIn('login', str(login.content))

    def test_a_user_can_signup_to_site(self):
        self.browser.get(self.live_server_url + '/signup/')
        username = self.browser.find_element_by_xpath('//*[@id="id_username"]')
        email = self.browser.find_element_by_xpath('//*[@id="id_email"]')
        password = self.browser.find_element_by_xpath('//*[@id="id_password1"]')
        repassword = self.browser.find_element_by_xpath('//*[@id="id_password2"]')
        username.send_keys('kuser')
        email.send_keys('RickDHoyt@teleworm.us')
        password.send_keys('logcatj4')
        repassword.send_keys('logcatj4')
        self.browser.find_element_by_xpath('//*[@id="signup_form"]/button').click()
        self.assertEqual(self.live_server_url + '/backend/', self.browser.current_url)
        self.assertIn('dashboard', self.browser.page_source)
        self.assertTemplateUsed('backend.html')
        self.assertIn('kuser', self.browser.page_source)
        self.assertIn('Sign Out', self.browser.page_source)


    def TearDown(self):
        self.browser.close()



