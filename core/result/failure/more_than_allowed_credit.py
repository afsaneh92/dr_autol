from core.messages.keys import Keys
from core.result import Result


class MoreThanAllowed(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.MORE_THAN_ALLOWED_CREDIT,
                Keys.PARAMS: self.params}
