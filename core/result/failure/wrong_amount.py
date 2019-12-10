from core.messages.keys import Keys
from core.result import Result

class WrongAmountFactor(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.JOB_PRICE_IS_WRONG, Keys.PARAMS: None}
