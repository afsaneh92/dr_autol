from core.messages.keys import Keys
from core.result import Result


class NotCancellable(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.IS_NOT_CANCELLABLE, Keys.PARAMS: None}
