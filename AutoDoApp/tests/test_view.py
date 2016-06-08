from django.test import TestCase
from django.test.client import Client
from django.conf import settings


class ViewTestCase(TestCase):
    # To be implemented
    def setUp(self):
        self.client = Client()

    def test_login_page_switch(self):
        response = self.client.get("/")
        #   Status Code Check
        self.assertEqual(response.status_code, 200)
        #   Template Check
        self.assertTemplateUsed(response, 'AutoDoApp/login.html')
        #   Context value Check
        self.assertEqual(response.context['client_id'], settings.GIT_HUB_URL)

    def test_main_page_switch(self):
        session = self.client.session
        session['oauth'] = 'test_oauth'
        session.save()
        response = self.client.get("/main/")
        #   Template Check
        self.assertTemplateUsed(response, 'AutoDoApp/main.html')

    def test_main_status_code(self):
        session = self.client.session
        session['oauth'] = 'test_oauth'
        session.save()
        response = self.client.get("/main/")
        #   Status Code Check
        self.assertEqual(response.status_code, 200)

    def test_main_context_content(self):
        session = self.client.session
        session['oauth'] = 'test_oauth'
        session.save()
        response = self.client.get("/main/")
        #   Context value Check
        self.assertEqual(response.context['client_id'], settings.GIT_HUB_URL)