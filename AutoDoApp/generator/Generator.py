# This python module is for document generator module
from .GeneratorCommunicator import GeneratorCommunicator


class Generator(GeneratorCommunicator):

    def generate_document(self):
        raise NotImplementedError("You must implement this methods!")

    def send_complete_notification(self):
        raise NotImplementedError("You must implement this methods!")

    def generate_readme_md(self):
        raise NotImplementedError("You must implement this methods!")

    def generate_api(self):
        raise NotImplementedError("You must implement this methods!")

    def generate_graph(self):
        raise NotImplementedError("You must implement this methods!")
