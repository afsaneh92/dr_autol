from core.messages.keys import Keys
from core.result import Result


class SuccessCancelJob(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.SUCCESS_CANCEL_JOB, Keys.PARAMS: None}
