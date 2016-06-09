from django.test import TestCase
from AutoDoApp.models import Project
from AutoDoApp.models import User


class ProjectModelTestCase(TestCase):

    def setUp(self):
        u = User(email="test@test.com", account_ID="test_account")
        u.access_token = "token"
        Project.objects.create(repository_url="obj1", description='before statement', user=u)
        Project.objects.create(repository_url="obj2", branch_count=100, is_enrolled=False, user=u)
        self.wrong_type_int_to_bool = False
        self.wrong_type_int_to_str = "5"
        self.wrong_type_bool_to_str = "False"
        self.wrong_type_bool_to_int = 3
        self.wrong_type_str_to_int = 4
        self.wrong_type_str_to_bool = True
        self.correct_str = "test statement"

    def test_wrong_data_type_int_to_str_should_raise_type_error(self):
        obj = Project.objects.get(repository_url="obj1")
        obj.branch_count = self.wrong_type_int_to_str
        self.assertRaises(TypeError, obj.update)

    def test_wrong_data_type_int_to_bool_should_raise_type_error(self):
        obj = Project.objects.get(repository_url="obj1")
        obj.branch_count = self.wrong_type_int_to_bool
        self.assertRaises(TypeError, obj.update)

    def test_wrong_data_type_bool_to_int_should_raise_type_error(self):
        obj = Project.objects.get(repository_url="obj1")
        obj.is_enrolled = self.wrong_type_bool_to_int
        self.assertRaises(TypeError, obj.enroll)

    def test_wrong_data_type_bool_to_str_should_raise_type_error(self):
        obj = Project.objects.get(repository_url="obj1")
        obj.is_enrolled = self.wrong_type_bool_to_str
        self.assertRaises(TypeError, obj.enroll)

    def test_wrong_data_type_str_to_int_should_raise_type_error(self):
        obj = Project.objects.get(repository_url="obj1")
        obj.description = self.wrong_type_str_to_int
        self.assertRaises(TypeError, obj.desc_update, self.correct_str)

    def test_wrong_data_type_str_to_bool_should_raise_type_error(self):
        obj = Project.objects.get(repository_url="obj1")
        obj.description = self.wrong_type_str_to_bool
        self.assertRaises(TypeError, obj.desc_update, self.correct_str)

    def test_wrong_param_data_type_str_to_int_should_raise_type_error(self):
        obj = Project.objects.get(repository_url="obj1")
        obj.description = self.correct_str
        self.assertRaises(TypeError, obj.desc_update, self.wrong_type_str_to_int)

    def test_wrong_param_data_type_str_to_bool_should_raise_type_error(self):
        obj = Project.objects.get(repository_url="obj1")
        obj.description = self.correct_str
        self.assertRaises(TypeError, obj.desc_update, self.wrong_type_str_to_bool)

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