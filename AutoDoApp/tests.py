from django.test import TestCase
from django.test.client import Client
from django.conf import settings
from .models import Project
from .models import User


# Create your tests here.
class BasicTestCase(TestCase):
    def setUp(self):
        pass

    def test_should_pass(self):
        self.assertEqual(True, True)


# Test Cases for Django Database Model. Written by JS
class ProjectModelTestCase(TestCase):
    def setUp(self):
        u = User.objects.create(email="test")
        Project.objects.create(repository_url="obj1", description='before statement', user=u)
        Project.objects.create(repository_url="obj2", branch_count=100, is_enrolled=False, user=u)
        pass

    def test_desc_update(self):
        obj1 = Project.objects.get(repository_url="obj1")
        obj1.desc_update("test statement")
        self.assertEqual(obj1.description, "test statement")

    def test_branch_count_update(self):
        obj = Project.objects.get(repository_url="obj2")
        obj.update()
        self.assertEqual(obj.branch_count, 101)

    def test_enroll(self):
        obj = Project.objects.get(repository_url="obj2")
        obj.enroll()
        self.assertEqual(obj.is_enrolled, True)


class ViewTestCase(TestCase):
    # To be implemented
    def setUp(self):
        self.client = Client()

    def test_hook_callback(self):
        response = self.client.get("hook/")
        #   Status Code Check
        self.assertEqual(response.status_code, 200)

    def test_oauth_callback(self):
        response = self.client.get("callback/")
        #   Status Code Check
        self.assertEqual(response.status_code, 200)
        #   Template Check
        self.assertTemplateUsed(response, 'main.html')

    def test_login_page_switch(self):
        response = self.client.get("/")
        #   Status Code Check
        self.assertEqual(response.status_code, 200)
        #   Template Check
        self.assertTemplateUsed(response, 'login.html')
        #   Context value Check
        self.assertEqual(response.context['client_id'],settings.GIT_HUB_URL)

    def test_main_rendering(self):
        response = self.client.get("/main/")
        #   Status Code Check
        #self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'login.html')
        #   Template Check
        self.assertTemplateUsed(response, 'main.html')
        #   Context value Check
        self.assertEqual(response.context['client_id'],settings.GIT_HUB_URL)