from core.messages.keys import Keys
from core.result import Result


class OrderList(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: 200, Keys.MESSAGE: Result.language.ORDER_LIST, Keys.PARAMS: self.params}