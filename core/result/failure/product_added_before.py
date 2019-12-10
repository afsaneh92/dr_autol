from core.messages.keys import Keys
from core.result import Result


class ProductAddedBefore(Result):
    def dictionary_creator(self):

        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.ID_IS_NOT_IN_DB, Keys.PARAMS: None}