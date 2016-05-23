# This python module is Manager Thread to orchestrate parser, util, generator modules.
from AutoDoApp.generator.Generator import Generator
from AutoDoApp.parser.Parser import Parser
import threading
from queue import Queue


class ManagerThread(object):

    def __init__(self):
        self.parser = Parser()
        self.generator = Generator()
        self.task_q = Queue()
        self.result_q = Queue()
        for method in [self.get_request, self.parse_project, self.generate_document]:
            t = threading.Thread(method)
            t.daemon = True
            t.start()

    def get_request(self, req):
        self.task_q.put(req)

    def parse_project(self, github_id, project_id):
        # Need to process get project url using github id and project id
        while not self.task_q.empty():
            parse_result = self.parser.parse_project(github_id)
            self.result_q.put(parse_result)

    def generate_document(self, parsed_info):
        while not self.result_q.empty():
            self.generator.generate_graph(data=self.result_q.get())
