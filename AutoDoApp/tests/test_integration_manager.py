from AutoDoApp.parser.Parser import Parser
from AutoDoApp.generator.Generator import Generator
from AutoDoApp.Manager import ManagerThread
from django.test import TestCase
from django.conf import settings
import os
import stat


class IntegrationManagerTestCase(TestCase):
    def setUp(self):
        self.git_directory = os.path.join(settings.BASE_DIR, "git_project")
        if os.path.isdir(self.git_directory):  # If there is a directory
            for root, dirs, files in os.walk(top=self.git_directory, topdown=False):
                for name in files:
                    os.chmod(os.path.join(root, name), stat.S_IWRITE)
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.chmod(os.path.join(root, name), stat.S_IWRITE)
                    os.rmdir(os.path.join(root, name))
            os.rmdir(self.git_directory)

        os.mkdir(self.git_directory)  # Building a directory

        self.m = ManagerThread()
        self.test_git_url = "https://github.com/JunoJunho/AutoDoTestApp"
        self.project_name = "AutoDoTestApp"
        self.project_description = "Test description"
        self.m.put_request(req=self.test_git_url,
                           desc=self.project_description)
        self.result_directory = os.path.join(settings.BASE_DIR, "parsing_result")
        self.file_loc = os.path.join(self.result_directory, self.project_name)
        import time
        time.sleep(5)

    def test_manager_generate_graph_file(self):
        self.assertTrue(os.path.exists(self.file_loc + ".png"))

    def test_manager_generate_markdown_file(self):
        self.assertTrue(os.path.exists(self.file_loc + ".md"))
