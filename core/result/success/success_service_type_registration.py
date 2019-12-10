from core.messages.keys import Keys
from core.result import Result


class SuccessServiceTypeRegistration(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: 200, Keys.MESSAGE: self.message, Keys.PARAMS: None}
