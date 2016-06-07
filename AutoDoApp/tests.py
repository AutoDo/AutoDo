from django.test import TestCase
from .models import Project


# Create your tests here.
class BasicTestCase(TestCase):
    def setUp(self):
        pass

    def test_should_pass(self):
        self.assertEqual(True, True)


# Test Cases for Django Database Model. Written by JS
class ProjectModelTestCase(TestCase):
    def setUp(self):
        Project.objects.create(repository_url="obj1", description='before statement')
        Project.objects.create(repository_url="obj2", branch_count=100, is_enrolled=False)
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
        pass

    def test_create_hook(self):
        pass

    def test_hook_callback(self):
        pass

    def test_create_file_commit(self):
        pass

    def test_create_a_branch(self):
        pass

    def test_generate_document(self):
        pass

    def test_oauth_callback(self):
        pass

    def test_integration_process(self):
        pass

    def test_github_info_parse(self):
        pass

    def test_post_json(self):
        pass