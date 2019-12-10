from abc import ABCMeta, abstractmethod

from core.messages.translator.persian import Persian


class Result:
    __metaclass__ = ABCMeta

    language = Persian

    def __init__(self, status, message=None, params=None):
        self.status = status
        self.message = message
        self.params = params

    @abstractmethod
    def dictionary_creator(self):
        pass

