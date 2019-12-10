from core.messages.keys import Keys
from core.result import Result


class JobPaidBefore(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.JOB_IS_PAID_BEFORE, Keys.PARAMS: None}
