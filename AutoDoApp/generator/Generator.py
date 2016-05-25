# This python module is for document generator module

import pydotplus
import cloudinary.uploader
import cloudinary.api

import cloudinary
import cloudinary.uploader
import cloudinary.api

import os
import shutil
from django.conf import settings

from AutoDoApp.generator.GeneratorCommunicator import GeneratorCommunicator


class Generator(GeneratorCommunicator):

    def __init__(self):
        self.png_dir = ""
        self.git_project_name = ""

    def generate_document(self, name):
        readme_dir = self.png_dir + ".md"
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
                    readme.write("<img src='http://res.cloudinary.com/jin8/image/upload/"+name+".png'/>")
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
        if os.path.isdir(self.png_dir):  # If there is a directory
            shutil.rmtree(self.png_dir)  # remove it

        graph.write_png(self.png_dir + '.png')

        cloudinary.config(
            cloud_name="jin8",
            api_key="179139842767459",
            api_secret="BtqQQ54EvWJ8U4TKePyUvFk8kkU"
        )
        cloudinary.uploader.upload(self.png_dir + '.png', public_id=name + ".png")
