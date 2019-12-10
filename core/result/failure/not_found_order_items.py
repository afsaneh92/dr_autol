from core.messages.keys import Keys
from core.result import Result


class NotFoundOrderItem(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.NOT_FOUND_ORDER_ITEM, Keys.PARAMS: self.params}
