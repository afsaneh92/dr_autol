from core.messages.keys import Keys
from core.result import Result


class NotInSameGrade(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.NOT_IN_SAME_GRADE, Keys.PARAMS: None}
