from core.messages.keys import Keys
from core.result import Result


class EmptyList(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: 404, Keys.MESSAGE: Result.language.FAIL_LIST, Keys.PARAMS: None}
