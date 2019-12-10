from core.messages.keys import Keys
from core.result import Result


class NotFinishedJob(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.JOB_IS_NOT_FINISHED, Keys.PARAMS: self.params}