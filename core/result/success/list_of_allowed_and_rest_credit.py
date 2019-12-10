from core.messages.keys import Keys
from core.result import Result


class ListOfAllowedAndUsedCredit(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: 200, Keys.MESSAGE: Result.language.SUCCESS_TO_BUY, Keys.PARAMS: self.params}
