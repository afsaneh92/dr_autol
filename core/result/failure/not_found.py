from core.messages.keys import Keys
from core.result import Result


class NotFound(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status}
