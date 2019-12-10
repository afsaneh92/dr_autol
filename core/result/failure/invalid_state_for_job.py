from core.messages.keys import Keys
from core.result import Result


class InvalidState(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.INVALID_STATE}
