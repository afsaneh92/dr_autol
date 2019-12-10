from core.messages.keys import Keys
from core.result import Result


class BadRangRate(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: 404, Keys.MESSAGE: Result.language.BAD_RANGE_RATE, Keys.PARAMS: self.params}
