from django.contrib.sites import requests
import requests
from django.test import TestCase
from AutoDoApp.parser.Parser import Parser
from AutoDoApp.generator.Generator import Generator
import os
from django.conf import settings

class GeneratorTestCase(TestCase):

    def setUp(self):

        self.git_address = "https://github.com/JunoJunho/AutoDoTestApp"
        self.project_name = "AutoDoTestApp"
        self.p = Parser()
        self.test_graph = Generator()
        self.test_readme = Generator()
        self.test_api = Generator()
        self.test_document = Generator()
        #self.client = Client()
        self.parsing_dir = os.path.join(settings.BASE_DIR, "parsing_result")
        if not os.path.exists(self.parsing_dir):
            os.mkdir(self.parsing_dir)

        git_dir = os.path.join(settings.BASE_DIR, "git_project")
        if not os.path.exists(git_dir):
            os.mkdir(git_dir)


    #invalid wrong valid
    def test_invalid_input_graph(self):
        #result = self.p.parse_project(git_url=self.correct_git_address)

        test_data = [("class A", "class A", "method1"),("class B", "class 1", "method2"),("class C",)]
        self.assertRaises(ValueError, self.test_graph.generate_graph, test_data,"TestInvalidInputGraph")

    def test_valid_input_graph(self):
        file_name = "TestValidGraph"
        test_data = [("class A", "class A", "method1"), ("class B", "class 1", "method2"), ("class C","class A","method3")]
        url = self.test_graph.generate_graph(test_data, "TestValidGraph")
        request = requests.get(url)
        self.assertTrue(request.status_code == 200)

    def test_invalid_name_readme(self):
        self.assertRaises(TypeError, self.test_readme.generate_readme_md, [], "test","test",[])

    def test_invalid_desc_readme(self):
        self.assertRaises(TypeError, self.test_readme.generate_readme_md, "TestInvalidReadme", [], "test", [])

    def test_invalid_licen_readme(self):
        self.assertRaises(TypeError, self.test_readme.generate_readme_md, "TestInvalidReadme", "test", [], [])

    def test_invalid_req_readme(self):
        self.assertRaises(TypeError, self.test_readme.generate_readme_md, "TestInvalidReadme", "test", "test", "test")

    def test_invalid_url_readme(self):
        self.assertRaises(ValueError, self.test_readme.generate_readme_md, "TestInvalidReadme", "test", "test", [])

    def test_valid_readme(self):
        file_name = "TestValidGraph"
        test_data = [("class A", "class A", "method1"), ("class B", "class A", "method2"),
                     ("class C", "class A", "method3")]
        self.test_readme.generate_graph(test_data, "TestValidGraph")
        self.test_readme.generate_readme_md("TestValidGraph", "test", "test", [])
        self.assertTrue(os.path.isfile(os.path.join(self.parsing_dir,file_name)+".md"))

    def test_invalid_api(self):
        self.assertRaises(TypeError, self.test_api.generate_api, [])

    def test_valid_api(self):
        self.test_api.generate_api({})
        self.assertTrue(True)

    def test_valid_document(self):
        re = self.p.parse_project(self.git_address)
        #generate_document(self, data, name, raw_api, desc, licen, req):
        #tu = [graph, name, self.parse_api(), self.req_list, self.license]
        self.test_document.generate_document(re[0],re[1],re[2],"desc", re[4],re[3])
        self.assertTrue(os.path.isfile(os.path.join(self.parsing_dir,self.project_name)+".md"))


