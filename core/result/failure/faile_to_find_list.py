from core.messages.keys import Keys
from core.result import Result


class FailToFindList(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.UNSUCCESS_LIST, Keys.PARAMS: self.params}
