<<<<<<< HEAD
# This python module is for document generator module

import pydotplus
import cloudinary.uploader
import cloudinary.api

import cloudinary
import cloudinary.uploader
import cloudinary.api

import os
from django.conf import settings

from AutoDoApp.generator.GeneratorCommunicator import GeneratorCommunicator


class Generator(GeneratorCommunicator):

    def __init__(self):
        self.png_dir = ""
        self.git_project_name = ""
        self.url = ""
        self.api = {}

    def generate_document(self, data, name):
        self.__generate_graph(data, name)
        self.__generate_api(data)
        self.__generate_readme_md(name)

    def send_complete_notification(self):
        raise NotImplementedError("You must implement this methods!")

    def __generate_readme_md(self, name):
        readme_dir = self.png_dir + ".md"
        if os.path.isfile(readme_dir + ".md"):
            os.remove(readme_dir + ".md")
        '''
        readme_data = {"Introduction": "project",
                       "Requirements": "information need to execute",
                       "API Reference": {"class1":
                                         {
                                             "method1": "description",
                                             "method2": "description",
                                             "method3": "description"
                                         },
                                         "class2":
                                         {
                                             "method1": "description"
                                         }
                       },
                       "Dependency graph": "image of dependency graph",
                       "Contributor": "get recent participant of the projects",
                       "License": "get license of the project"}
        '''

        readme_order = ["Introduction", "Requirements", "API Reference", "Dependency graph", "Contributor", "License"]
        with open(readme_dir, "w") as readme:
            readme.write("# "+name+"\n")
            for title in readme_order:
                #content = readme_data[title]
                readme.write("### "+title+"\n")
                if title == "Introduction":

                    readme.write("TODO: Describe the about the project \n")
                elif title == "Requirements" :

                    readme.write("These are the requirements needs to be install "
                                 "in order to execute this project: \n\n")
                    readme.write("```"+"INPUT"+"```"+"\n")

                #elif title == "Installation" :
                #    readme.write("TODO: Describe the installation process\n")
                #    readme.write("``` code\n")
                #    readme.write("```"+"\n")

                elif title == "API Reference":
                    for class_name in sorted(self.api.keys()):
                        readme.write("##### " + class_name+"\n\n")
                        for method in sorted(self.api[class_name]):
                            readme.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + "**" + method + "**" + "\n\n")

                        readme.write("\n")
                elif title == "Dependency graph":
                    # graph file name
                    readme.write("<p align='center'>")
                    readme.write("<img src='" + self.url + "'/>")
                    readme.write("</p>\n")

                elif title == "Contributor":
                    readme.write("INPUT"+"\n")

                elif title == "License":
                    readme.write("INPUT"+"\n")
                readme.write("\n\n")

            readme.close()
        #raise NotImplementedError("You must implement this methods!")

    def generate_api(self, data):
        self.__generate_api(data)

    def __generate_api(self, data):
        self.api={}
        for i in range(len(data)):
            if not self.api[data[i][0]]:
                self.api[data[i][0]] = []
            self.api[data[i][0]].append(data[i][2])
        #print(self.api)
    #raise NotImplementedError("You must implement this methods!")

    '''
        data = [("class A","class B","method A to B"),
               ("class B","class C","method B to C"),
                ("class C","class A","method C to A"),
                ("class C", "class A", "method C' to A'"),
                ("class C", "class A", "method C'' to A''"),
                ("class A","class A","method A to A"),
                ("class B","class B","method B to B"),
                ("class C","class C","method C to C")]
    '''
    def generate_graph(self, data, name):
        self.__generate_graph(data, name)

    def __generate_graph(self, data, name):
        graph = pydotplus.Dot(graph_type="digraph")

        # let's add the relationship between the king and vassals
        for i in range(len(data)):
            edge = pydotplus.Edge(data[i][0], data[i][1], label=data[i][2], minlen='7')
            graph.add_edge(edge)

        # ok, we are set, let's save our graph into a file

        self.png_dir = os.path.join(settings.BASE_DIR, "parsing_result")
        self.png_dir = os.path.join(self.png_dir, name)
        if os.path.isfile(self.png_dir + ".png"):
            os.remove(self.png_dir + ".png")

        graph.write_png(self.png_dir + '.png')

        cloudinary.config(
            cloud_name="jin8",
            api_key="179139842767459",
            api_secret="BtqQQ54EvWJ8U4TKePyUvFk8kkU"
        )
        response = cloudinary.uploader.upload(self.png_dir + '.png', public_id=name)
        self.url = response['url']
        print(self.url)


if __name__ == "__main__":
    from AutoDoApp.parser.Parser import Parser

    p = Parser()
    re = p.parse_project(git_url="https://github.com/JunoJunho/AutoDoAppTest")
    g = Generator()
    g.generate_document(re[0], re[1])

=======
# This python module is for document generator module

import pydotplus
import cloudinary.uploader
import cloudinary.api

import cloudinary
import cloudinary.uploader
import cloudinary.api

import os
from django.conf import settings

from AutoDoApp.generator.GeneratorCommunicator import GeneratorCommunicator


class Generator(GeneratorCommunicator):

    def __init__(self):
        self.png_dir = ""
        self.git_project_name = ""
        self.url = ""

    def generate_document(self, name):
        readme_dir = self.png_dir + ".md"
        if os.path.isfile(readme_dir + ".md"):
            os.remove(readme_dir + ".md")
        readme_data = {"Introduction": "project",
                       "Requirements": "information need to execute",
                       "API Reference": {"class1":
                                         {
                                             "method1": "description",
                                             "method2": "description",
                                             "method3": "description"
                                         },
                                         "class2":
                                         {
                                             "method1": "description"
                                         }
                       },
                       "Dependency graph": "image of dependency graph",
                       "Contributor": "get recent participant of the projects",
                       "License": "get license of the project"}

        readme_order = ["Introduction", "Requirements", "API Reference", "Dependency graph", "Contributor", "License"]
        with open(readme_dir, "w") as readme:

            for title in readme_order:
                content = readme_data[title]
                readme.write("## " + title + "\n")
                if title == "Introduction":
                    readme.write("TODO: Describe the about the project \n")
                elif title == "Requirements" :
                    readme.write("These are the requirements needs to be install "
                                 "in order to execute this project: \n\n")
                    readme.write("```"+content+"```"+"\n")

                #elif title == "Installation" :
                #    readme.write("TODO: Describe the installation process\n")
                #    readme.write("``` code\n")
                #    readme.write("```"+"\n")

                elif title == "API Reference":
                    for class_name, method_dict in content.items():
                        readme.write("#### " + class_name+"\n\n")
                        for method, desc in method_dict.items():
                            readme.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + "**" + method + "**" + "\n\n")

                        readme.write("\n")
                elif title == "Dependency graph":
                    # graph file name
                    readme.write("<p align='center'>")

                    readme.write("<img src='" + self.url + "'/>")

                    readme.write("</p>\n")

                elif title == "Contributor":
                    readme.write(content+"\n")

                elif title == "License":
                    readme.write(content+"\n")
                readme.write("\n\n")

            readme.close()

    def send_complete_notification(self):
        raise NotImplementedError("You must implement this methods!")

    def generate_readme_md(self):
        raise NotImplementedError("You must implement this methods!")

    def generate_api(self):
        raise NotImplementedError("You must implement this methods!")

    '''
        data = [("class A","class B","method A to B"),
               ("class B","class C","method B to C"),
                ("class C","class A","method C to A"),
                ("class C", "class A", "method C' to A'"),
                ("class C", "class A", "method C'' to A''"),
                ("class A","class A","method A to A"),
                ("class B","class B","method B to B"),
                ("class C","class C","method C to C")]
    '''
    def generate_graph(self, data, name):
        self.__generate_graph(data, name)

    def __generate_graph(self, data, name):
        graph = pydotplus.Dot(graph_type="digraph")

        # let's add the relationship between the king and vassals
        for i in range(len(data)):
            edge = pydotplus.Edge(data[i][0], data[i][1], label=data[i][2], minlen='7')
            graph.add_edge(edge)

        # ok, we are set, let's save our graph into a file

        self.png_dir = os.path.join(settings.BASE_DIR, "parsing_result")
        self.png_dir = os.path.join(self.png_dir, name)
        if os.path.isfile(self.png_dir + ".png"):
            os.remove(self.png_dir + ".png")

        graph.write_png(self.png_dir + '.png')

        cloudinary.config(
            cloud_name="jin8",
            api_key="179139842767459",
            api_secret="BtqQQ54EvWJ8U4TKePyUvFk8kkU"
        )
        response = cloudinary.uploader.upload(self.png_dir + '.png', public_id=name)
        self.url = response['url']


if __name__ == "__main__":
    from AutoDoApp.parser.Parser import Parser

    p = Parser()
    re = p.parse_project(git_url="https://github.com/JunoJunho/AutoDoAppTest")
    g = Generator()
    g.generate_graph(re[0],re[1])
    g.generate_document(re[1])

>>>>>>> ef27b4ae32ca527cbb6037853ad328b7460209a1
