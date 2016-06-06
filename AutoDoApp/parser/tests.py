from django.test import TestCase
from AutoDoApp.parser.Parser import Parser
import os
from django.conf import settings

class ParserTestCase(TestCase):

    def setUp(self):
        self.correct_git_address = "https://github.com/JunoJunho/AutoDoTestApp"
        self.wrong_git_address = "https://jithub.com/JunoJunho/AutoDoTestApp"
        self.project_name = "AutoDoTestApp"
        self.p = Parser()
        git_dir = os.path.join(settings.BASE_DIR, "git_project")
        if not os.path.exists(git_dir):
            os.mkdir(git_dir)

    def test_wrong_git_address_should_raise_value_error(self):
        self.assertRaises(ValueError, self.p.parse_project, self.wrong_git_address)

    def test_should_return_tuple(self):
        result = self.p.parse_project(git_url=self.correct_git_address)
        self.assertIsInstance(result, tuple)

    def test_should_return_tuple_with_existing_directory(self):
        result = self.p.parse_project(git_url=self.correct_git_address)
        self.assertIsInstance(result, tuple)

    def test_tuple_length_should_be_5(self):
        result = self.p.parse_project(git_url=self.correct_git_address)
        self.assertEqual(len(result), 5)

    def test_project_name_is_correct(self):
        result = self.p.parse_project(git_url=self.correct_git_address)
        self.assertEqual(self.project_name, result[1])

    def test_requirement_list_is_list_type(self):
        result = self.p.parse_project(git_url=self.correct_git_address)
        self.assertIsInstance(result[3], list)

    def test_api_is_dict_type(self):
        result = self.p.parse_project(git_url=self.correct_git_address)
        self.assertIsInstance(result[2], dict)

    def test_license_should_be_MIT(self):
        result = self.p.parse_project(git_url=self.correct_git_address)
        self.assertTrue("MIT" in result[4])

    def test_graph_is_list_type(self):
        result = self.p.parse_project(git_url=self.correct_git_address)
        self.assertIsInstance(result[0], list)
