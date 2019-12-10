from core.messages.keys import Keys
from core.result import Result


class JobNotFound(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.NOT_FOUND_JOB, Keys.PARAMS: None}
