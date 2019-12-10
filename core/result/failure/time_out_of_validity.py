from core.messages.keys import Keys
from core.result import Result


class TimeOutOfValidity(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: self.message, Keys.PARAMS: self.params}
