from django.test import TestCase
from django.test.client import Client
from django.conf import settings
from django.template import loader
from .models import Project
from .models import User


# Test Cases for Django Database Model. Written by JS
class ProjectModelTestCase(TestCase):
    def setUp(self):
        self.correct_email = "test@test.com"
        self.wrong_email = "abcd.com"
        self.correct_account_ID = "test_account"
        self.wrong_account_ID = " "
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


class UserModelTestCase(TestCase):
    def setUp(self):
        self.correct_email = "test@test.com"
        self.wrong_email = "abcd.com"
        self.correct_account_ID = "test_account"
        self.wrong_account_ID = " "

    def test_wrong_email_should_raise_value_error(self):
        kwargs = {"email": self.wrong_email,
                  "account_ID": self.correct_account_ID}
        self.assertRaises(ValueError, User.objects.create, self.wrong_email, self.correct_account_ID)


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
        #   Status Code Check
        self.assertEqual(response.status_code, 200)
        #   Template Check
        self.assertTemplateUsed(response, 'AutoDoApp/main.html')
        #   Context value Check
        self.assertEqual(response.context['client_id'], settings.GIT_HUB_URL)
