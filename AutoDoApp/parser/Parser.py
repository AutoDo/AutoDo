# This module file is for parsing the github project.
from AutoDoApp.parser.ParserCommunicator import ParserCommunicator
import os
import git
import shutil


class Parser(ParserCommunicator):

    def __init__(self):
        self.tmp_dir = "temp"

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
        dir_dict = {}
        # Traverse each directory to parse sub-directories and their files
        for dir_name, subdir_list, file_list in os.walk(root_dir):
            r_index = dir_name.rfind("/")
            if dir_name.startswith(".", r_index+1) or dir_name.startswith("_", r_index+1):
                continue
            tmp_list = []
            print("Directory found: " + dir_name)
            for f_name in file_list:
                tmp_list.append(f_name)
            dir_dict[dir_name] = tmp_list

    def prev_parse_project(self):
        raise NotImplementedError("Implement this method!")

    def calculate_diff_between(self, curr, prev):
        raise NotImplementedError("Implement this method!")

    def test(self):
        self.__parse_directory_structure()


if __name__ == "__main__":
    p = Parser()
    p.test()
