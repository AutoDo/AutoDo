# This python module is for document generator module

import pydotplus
import cloudinary.uploader
import cloudinary.api

import cloudinary
import cloudinary.uploader
import cloudinary.api

import os
from django.conf import settings
#from django.contrib.sites import requests
import requests
from AutoDoApp.generator.GeneratorCommunicator import GeneratorCommunicator


class Generator(GeneratorCommunicator):

    def __init__(self):
        self.png_dir = ""
        self.git_project_name = ""
        self.url = ""
        self.api = {}

    def generate_document(self, data, name, raw_api, desc, licen, req):

        self.__generate_graph(data, name)
        self.__generate_api(raw_api)
        self.__generate_readme_md(name, desc, licen, req)



    def send_complete_notification(self):
        raise NotImplementedError("You must implement this methods!")

    def generate_readme_md(self, name, desc, licen,req):
        self.__generate_readme_md(name,desc,licen,req)

    def __generate_readme_md(self, name, desc, licen, req):
        if type(name) is not str:
            raise TypeError("Wrong name type: it needs to be str type")
        if type(desc) is not str:
            raise TypeError("Wrong desc type: it needs to be str type")
        if type(licen) is not str:
            raise TypeError("Wrong licen type: it needs to be str type")
        if type(req) is not list:
            raise TypeError("Wrong req type: it needs to be list type")



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

        readme_order = ["Introduction", "Requirements", "API Reference", "Dependency graph", "License"]
        with open(readme_dir, "w") as readme:
            readme.write("# "+name+"\n")
            for title in readme_order:
                # content = readme_data[title]
                readme.write("### "+title+"\n")
                if title == "Introduction":

                    readme.write(desc + " \n")
                    readme.write("***")
                elif title == "Requirements":

                    readme.write("These are the requirements needs to be install "
                                 "in order to execute this project: \n\n")
                    if len(req) < 1:
                        #print("No req")
                        readme.write("```\n"+"No requirements"+"\n```"+"\n")
                    else:
                        for each in req:
                            readme.write("```\n"+each+"\n```"+"\n")
                    readme.write("***")
                # elif title == "Installation" :
                #    readme.write("TODO: Describe the installation process\n")
                #    readme.write("``` code\n")
                #    readme.write("```"+"\n")

                elif title == "API Reference":
                    for class_name in sorted(self.api.keys()):
                        readme.write("##### " + class_name+"\n\n")
                        for method in sorted(set(self.api[class_name])):
                            if "__" in method:
                                method = method.replace("__", "\__", 1)
                            readme.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + "**" + method + "**" + "\n\n")
                        readme.write("\n")
                    readme.write("***")
                elif title == "Dependency graph":
                    request = requests.get(self.url)
                    if(request.status_code == 200):
                        # graph file name
                        readme.write("<p align='center'>")
                        readme.write("<img src='" + self.url + "'/>")
                        readme.write("</p>\n")
                        readme.write("***")
                    else:
                        raise ValueError("URL does not exist in cloudinary")
                elif title == "License":
                    readme.write(licen+"\n")
                    readme.write("***")
                    print("license is added")
                readme.write("\n\n")

            readme.close()
        # raise NotImplementedError("You must implement this methods!")

    def generate_api(self, data):
        if type(data) is dict:
            self.__generate_api(data)
        else:
            raise TypeError("Wrong data type: it needs to be dict")

    def __generate_api(self, data):  # data -> dictionary
        self.api = {}
        for each_key in data:
            self.api[each_key] = []
            for item in data[each_key]:
                print(each_key + " + " + item)
                self.api[each_key].append(item)
        # for i in range(len(data)):
        #     if not(data[i][0] in self.api):
        #         self.api[data[i][0]] = []
        #     self.api[data[i][0]].append(data[i][2])

    def generate_graph(self, data, name):
        self.__generate_graph(data, name)
        return self.url
    def __generate_graph(self, data, name):
        graph = pydotplus.Dot(graph_type="digraph")

        # validate data
        for i in range(len(data)):
            if len(data[i]) < 3: # each data has to contain (node, node, edge)
                raise ValueError("Wrong input for graph")



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
        #print(self.url)


if __name__ == "__main__":
    from AutoDoApp.parser.Parser import Parser

    p = Parser()
    re = p.parse_project(git_url="https://github.com/JunoJunho/AutoDoAppTest")
    g = Generator()
    g.generate_document(re[0], re[1])

