from core.messages.keys import Keys
from core.result import Result


class WrongPassOrPhoneNumber(Result):
    def dictionary_creator(self):
        user_info = {Keys.PHONE_NUMBER: self.params[Keys.PHONE_NUMBER]}
        return {Keys.STATUS: self.status, Keys.MESSAGE: self.message, Keys.PARAMS: user_info}
