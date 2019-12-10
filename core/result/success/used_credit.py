from core.messages.keys import Keys
from core.result import Result


class UsedCredit(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: 200, Keys.MESSAGE: Result.language.USED_CREDIT, Keys.PARAMS: self.params}
