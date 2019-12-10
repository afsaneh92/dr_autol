from core.messages.keys import Keys
from core.result import Result


class EmptySheet(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.JOB_RATED_BEFORE, Keys.PARAMS: self.params}
