from core.messages.keys import Keys
from core.result import Result


class SuccessRegisterProblem(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.SUCCESS_REGISTER_PROBLEM, Keys.PARAMS: None}
