from core.messages.keys import Keys
from core.result import Result


class SupplierIdPhoneNumberNotMatch(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.ID_AND_PHONE_NUMBER_NOT_MATCH,
                Keys.PARAMS: None}
