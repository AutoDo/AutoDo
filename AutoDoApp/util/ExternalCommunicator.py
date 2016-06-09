# This Python interface file is for providing public methods on util component
# Author: Junho Kim
# AutoDo Project


class ExternalCommunicator(object):

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
