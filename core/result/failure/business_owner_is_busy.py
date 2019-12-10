from core.messages.keys import Keys
from core.result import Result


class BusinessOwnerIsBusy(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.BUSINESS_OWNER_IS_BUSY, Keys.PARAMS: None}