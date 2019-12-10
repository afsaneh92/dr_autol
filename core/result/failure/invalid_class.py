from core.messages.keys import Keys
from core.result import Result


class InvalidClass(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.NO_CLASS_PATH, Keys.PARAMS: self.params}
