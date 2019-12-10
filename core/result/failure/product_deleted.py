from core.messages.keys import Keys
from core.result import Result


class SuccessDeleteProduct(Result):
    def dictionary_creator(self):

        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.SUCCESS_DELETE_PRODUCT, Keys.PARAMS: None}