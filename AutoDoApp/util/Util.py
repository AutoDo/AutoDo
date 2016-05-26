# This Util module file is for github interaction and database interaction
# Author: Junho Kim
# AutoDo Project
from .ExternalCommunicator import ExternalCommunicator


class Util(ExternalCommunicator):
    def get_db_cursor(self):
        raise NotImplementedError("Implement this method!")

    def exec_query(self, query):
        raise NotImplementedError("Implement this method!")

    def clone_repository(self, git_url):
        raise NotImplementedError("Implement this method!")

    def create_pull_request(self, project):
        raise NotImplementedError("Implement this method!")

    def register_git_hook(self, repository):
        raise NotImplementedError("Implement this method!")

    def get_git_instance(self):
        raise NotImplementedError("Implement this method!")
