from core.messages.keys import Keys
from core.result import Result


class SuccessStartJob(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.SUCCESS_START_JOB, Keys.PARAMS: self.params}
