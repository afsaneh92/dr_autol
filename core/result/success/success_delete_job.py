from core.messages.keys import Keys
from core.result import Result


class SuccessDeleteJob(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.SUCCESS_DELETE_JOB, Keys.PARAMS: self.params}
