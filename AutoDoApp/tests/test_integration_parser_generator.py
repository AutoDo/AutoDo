from AutoDoApp.parser.Parser import Parser
from AutoDoApp.generator.Generator import Generator
from AutoDoApp.Manager import ManagerThread
from django.test import TestCase
from django.conf import settings
import os
import stat


class IntegrationTestCase(TestCase):

    def setUp(self):
        self.p = Parser()
        self.g = Generator()
        self.test_git_url = "https://github.com/JunoJunho/AutoDoTestApp"
        self.result = self.p.parse_project(self.test_git_url)
        self.project_description = "Test description"
        self.g.generate_document(data=self.result[0],
                                 name=self.result[1],
                                 raw_api=self.result[2],
                                 desc=self.project_description,
                                 licen=self.result[4],
                                 req=self.result[3])
        self.result_directory = os.path.join(settings.BASE_DIR, "parsing_result")
        self.project_name = "AutoDoTestApp"
        self.git_directory = os.path.join(settings.BASE_DIR, "git_project")
        self.file_loc = os.path.join(self.result_directory, self.project_name)

    def test_graph_file_is_generated(self):
        self.assertTrue(os.path.exists(self.file_loc + ".png"))

    def test_read_me_is_generated(self):
        self.assertTrue(os.path.exists(self.file_loc + ".md"))
