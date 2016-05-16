# This module file is for parsing the github project.
from AutoDoApp.parser.ParserCommunicator import ParserCommunicator
import os
import codecs
import git
import shutil


class Parser(ParserCommunicator):

    def __init__(self):
        self.tmp_dir = "temp"
        self.dir_dict = {}
        self.class_dict = {}  # key: full path file_name, value: a list containing class names

    def task_request(self, project_id, user_id):
        raise NotImplementedError("Implement this method!")

    def task_complete(self, project_id, user_id):
        raise NotImplementedError("Implement this method!")

    def parse_api(self):
        raise NotImplementedError("Implement this method!")

    def parse_readme(self):
        raise NotImplementedError("Implement this method!")

    def parse_graph(self):
        raise NotImplementedError("Implement this method!")

    def parse_project(self, git_url):
        self.__clone_repository(git_url=git_url)
        self.__parse_directory_structure()
        self.__traverse_directories()

    def __clone_repository(self, git_url):
        git_url = git_url
        if os.path.isdir(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)

        os.mkdir(self.tmp_dir)

        repo = git.Repo.init(self.tmp_dir)
        origin = repo.create_remote('origin', git_url)
        origin.fetch()
        origin.pull(origin.refs[0].remote_head)

    def __parse_directory_structure(self):
        # Root directory setup
        root_dir = self.tmp_dir + "/hot_opinion/"
        # Traverse each directory to parse sub-directories and their files
        for dir_name, subdir_list, file_list in os.walk(root_dir):
            r_index = dir_name.rfind("/")
            if dir_name.startswith(".", r_index+1) or dir_name.startswith("_", r_index+1):
                continue
            tmp_list = []
            for f_name in file_list:  # Check suffix of python project
                if f_name[-3:] == ".py":
                    tmp_list.append(f_name)
            if len(tmp_list) > 0:  # We will not add empty directory into the dictionary
                dir_name = dir_name.replace("\\", "/")
                self.dir_dict[dir_name] = tmp_list

    def __traverse_directories(self):
        # To traverse each source file, searching directories
        for key in self.dir_dict:
            print("Directory found: " + key)
            for item in self.dir_dict[key]:
                if key.endswith("/"):
                    path = key + item
                else:
                    path = key + "/" + item
                self.__traverse_source_file(path=path)

    def __traverse_source_file(self, path):
        # traverse each python file
        print("Full path: " + path)
        f = codecs.open(path, mode='r', encoding='utf-8')
        class_list = []
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if not line.startswith("class"):
                continue
            else:
                tokens = line.split("class")
                cls_name = tokens[1].strip()
                cls_name = cls_name.replace(":", "")
                print("\tFound class: " + cls_name)
                class_list.append(cls_name)
        if len(class_list) > 0:
            self.class_dict[path] = class_list



    def prev_parse_project(self):
        raise NotImplementedError("Implement this method!")

    def calculate_diff_between(self, curr, prev):
        raise NotImplementedError("Implement this method!")

    def test(self):
        self.__parse_directory_structure()
        self.__traverse_directories()


if __name__ == "__main__":
    p = Parser()
    p.test()
