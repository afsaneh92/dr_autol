from core.messages.keys import Keys
from core.result import Result


class RegisteredBefore(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.REGISTERED_BEFORE}

