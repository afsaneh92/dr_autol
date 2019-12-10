from core.messages.keys import Keys
from core.result import Result


class CompanyNotFound(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.NOT_FOUND_COMPANY, Keys.PARAMS: None}