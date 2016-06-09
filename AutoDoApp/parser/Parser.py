# This module file is for parsing the github project.
from AutoDoApp.parser.ParserCommunicator import ParserCommunicator
import os
import codecs
import git
import stat
from django.conf import settings


class Parser(ParserCommunicator):

    def __init__(self):
        self.git_dir = ""
        self.dir_dict = {}
        self.class_dict = {}  # key: full path file_name, value: a list containing class names
        self.method_dict = {}  # key: class name, value: a list containing method names defined in the class
        self.instance_dict = {}  # key: class name, value: a list containing instance names inside the class
        self.variable_dict = {}  # key: instance name, value : a list containing invoked methods
        self.file_list = []
        self.req_list = []
        self.license = ""

    def task_request(self, project_id, user_id):
        raise NotImplementedError("Implement this method!")

    def task_complete(self, project_id, user_id):
        raise NotImplementedError("Implement this method!")

    def parse_api(self):
        return self.method_dict

    def parse_readme(self):
        raise NotImplementedError("Implement this method!")

    def parse_graph(self):
        raise NotImplementedError("Implement this method!")

    def parse_project(self, git_url):
        self.__init__()
        self.__clone_repository(git_url=git_url)
        self.__parse_directory_structure()
        self.__traverse_directories()

        # Output formatting
        graph = []
        for callee_class_name in self.variable_dict:
            for caller_class_name, instance_name in self.variable_dict[callee_class_name]:
                for invoked_method in self.instance_dict[instance_name]:
                    graph.append((caller_class_name, callee_class_name, invoked_method))
        name = "".join(git_url.split('/')[-1:])
        tu = [graph, name, self.parse_api(), self.req_list, self.license]
        return tuple(tu)

    def __clone_repository(self, git_url):

        if "github.com" not in git_url:
            raise ValueError("Wrong Github Address!")

        git_dir = os.path.join(settings.BASE_DIR, "git_project")
        git_dir = os.path.join(git_dir, "".join(git_url.split('/')[-1:]))
        self.git_dir = git_dir

        if os.path.isdir(git_dir):  # If there is a directory
            for root, dirs, files in os.walk(top=git_dir, topdown=False):
                for name in files:
                    os.chmod(os.path.join(root, name), stat.S_IWRITE)
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.chmod(os.path.join(root, name), stat.S_IWRITE)
                    os.rmdir(os.path.join(root, name))
            os.rmdir(git_dir)

        os.mkdir(git_dir)  # Building a directory

        repo = git.Repo.init(git_dir)
        origin = repo.create_remote('origin', git_url)
        origin.fetch()
        try:
            for each in origin.refs:
                if 'master' in each:
                    origin.pull(each.remote_head)
        except TypeError:
            origin.pull(origin.refs[0].remote_head)

    def __parse_directory_structure(self):
        # Root directory setup
        root_dir = self.git_dir
        # Traverse each directory to parse sub-directories and their files
        for dir_name, subdir_list, file_list in os.walk(root_dir):
            r_index = dir_name.rfind("/")
            if dir_name.startswith(".", r_index+1) or dir_name.startswith("_", r_index+1):
                continue
            tmp_list = []
            for f_name in file_list:  # Check suffix of python project
                if f_name[-3:] == ".py":
                    tmp_list.append(f_name)
                elif "requirement" in f_name and ".txt" in f_name:
                    self.req_list = self.__parse_requirements(f_name)
                elif "LICENSE" in f_name:
                    self.license = self.__parse_license(f_name)
            if len(tmp_list) > 0:  # We will not add empty directory into the dictionary
                dir_name = dir_name.replace("\\", "/")
                self.dir_dict[dir_name] = tmp_list

    def __traverse_directories(self):
        # To traverse each source file, searching directories
        for key in self.dir_dict:
            for item in self.dir_dict[key]:
                if key.endswith("/"):
                    path = key + item
                else:
                    path = key + "/" + item
                self.file_list.append(path)
        for path in self.file_list:
            self.__traverse_source_file_path1(path=path)
        for path in self.file_list:
            self.__traverse_source_file_path2(path=path)

    def __traverse_source_file_path1(self, path):
        # traverse each python file
        f = codecs.open(path, mode='r', encoding='utf-8')
        class_list = []
        lines = f.readlines()
        # Path1: traverse class name
        for line in lines:
            line = line.strip()
            if not line.startswith("class"):
                continue
            else:
                tokens = line.split("class")
                cls_name = tokens[1].strip()
                cls_name = cls_name.replace(":", "")
                class_list.append(cls_name)
        if len(class_list) > 0:
            self.class_dict[path] = class_list

        # Path2: traverse method name
        method_list = []
        cur_context = ""
        for line in lines:
            line = line.strip()
            if line.startswith("class"):
                if len(method_list) > 0:
                    self.method_dict[cur_context] = method_list
                    method_list.clear()
                tokens = line.split("class")
                cur_context = tokens[1].strip()
                cur_context = cur_context.replace(":", "")
            if not line.startswith("def"):
                continue
            else:
                tokens = line.split("def")
                method_name = tokens[1].strip()
                method_name = method_name.replace(":", "")
                method_list.append(method_name)
        if len(method_list) > 0:
            self.method_dict[cur_context] = method_list

    def __traverse_source_file_path2(self, path):
        f = codecs.open(path, mode='r', encoding='utf-8')
        lines = f.readlines()
        # Path3: traverse source file to parse instance variables and its call relationships
        # traverse information is stored at self.instance_dict.
        # Structure: first dict : {class name : second_dict}
        #            second dict : {instance_variable : invoked method list}
        invoked_method_dict = {}
        cur_context = {}
        cls_name = ""
        for line in lines:
            line = line.strip()
            if "." in line and "(" in line:  # Just method call
                tokens = line.split(".")
                instance_name = tokens[0]
                if len(tokens) > 1 and "." in tokens[1]:
                    method_name = tokens[1].split(".")[0].strip()
                    method_name = method_name.split("(")[0]
                elif len(tokens) > 1:
                    method_name = tokens[1].split("(")[0]
                if 'method_name' in locals():  # At least method call
                    if instance_name not in self.instance_dict:
                        self.instance_dict[instance_name] = [method_name+tokens[1]]
                    else:
                        self.instance_dict[instance_name].append(method_name+tokens[1])
            elif "(" in line and "=" in line:  # Possible to instance creation
                tokens = line.split("=")
                instance_name = tokens[0].strip()
                if len(tokens) > 1:
                    tokens = tokens[1].split("(")
                    if len(tokens) > 1:
                        instance_type = tokens[0].strip()
                        for files in self.class_dict:
                            for class_name in self.class_dict[files]:
                                if class_name.split("(")[0] == instance_type:
                                    if instance_type not in self.variable_dict:
                                        self.variable_dict[instance_type] = [(cls_name, instance_name)]  # Callee class
                                    else:
                                        self.variable_dict[instance_type].append((cls_name, instance_name))
            elif "class" in line:
                tokens = line.split("class")
                cls_name = tokens[1].strip()
                cls_name = cls_name.replace(":", "")

    def __parse_requirements(self, f_name):
        req_loc = os.path.join(self.git_dir, f_name)
        f = open(req_loc, 'r')
        req = f.readlines()
        return req

    def __parse_license(self, f_name):
        li_loc = os.path.join(self.git_dir, f_name)
        f = open(li_loc, 'r')
        return f.readline()

    def prev_parse_project(self):
        raise NotImplementedError("Implement this method!")

    def calculate_diff_between(self, curr, prev):
        raise NotImplementedError("Implement this method!")

    def test(self):
        self.parse_project("https")


if __name__ == "__main__":
    p = Parser()
    p.test()
