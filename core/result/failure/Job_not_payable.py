from core.messages.keys import Keys
from core.result import Result


class JobNotPayable(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.JOB_IS_NOT_PAYABLE, Keys.PARAMS: None}
