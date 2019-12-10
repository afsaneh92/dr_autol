from core.messages.keys import Keys
from core.result import Result


class NotInSameCategory(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.NOT_IN_SAME_CATEGORY, Keys.PARAMS: None}
