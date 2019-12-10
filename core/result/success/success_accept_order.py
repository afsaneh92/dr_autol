from core.messages.keys import Keys
from core.result import Result


class SuccessAcceptOrder(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.SUCCESS_ACCEPT_ORDER, Keys.PARAMS: None}

