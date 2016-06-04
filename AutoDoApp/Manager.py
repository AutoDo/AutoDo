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
        self.threads = []
        self.proj_desc = ""
        self.proj_license = ""
        for method in [self.parse_project, self.generate_document]:
            t = threading.Thread(target=method)
            t.daemon = True
            print("Method " + str(method) + " started")
            self.threads.append(t)
            t.start()

    def put_request(self, req, desc, licen):
        self.proj_desc = desc
        self.proj_license = licen
        self.task_q.put(req)

    def parse_project(self):
        # Need to process get project url using github id and project id
        while True:
            if not self.task_q.empty():
                tu = self.parser.parse_project(self.task_q.get())
                self.result_q.put(tu)
                break

    def generate_document(self):
        while True:
            if not self.result_q.empty():
                re = self.result_q.get()
                self.generator.generate_document(data=re[0],
                                                 name=re[1],
                                                 raw_api=re[2],
                                                 desc=self.proj_desc,
                                                 licen=self.proj_license)
                break
        for t in self.threads:
            t.join()
