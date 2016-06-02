# This python abstract class is for providing public methods to utilize the generator in AutoDo
# Project AutoDo


class GeneratorCommunicator(object):

    def generate_document(self, data, name):
        raise NotImplementedError("You must implement this methods!")

    def send_complete_notification(self):
        raise NotImplementedError("You must implement this methods!")
