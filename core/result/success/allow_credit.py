from core.messages.keys import Keys
from core.result import Result


class AllowCredit(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: 200, Keys.MESSAGE: Result.language.ALLOW_CREDIT, Keys.PARAMS: self.params}