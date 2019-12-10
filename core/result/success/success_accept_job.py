from core.messages.keys import Keys
from core.result import Result


class SuccessAcceptJob(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.SUCCESS_ACCEPT_JOB, Keys.PARAMS: None}


class SuccessDenyJob(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.SUCCESS_DENY_JOB, Keys.PARAMS: None}
