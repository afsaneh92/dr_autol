from core.result import Result


class SuccessRangeRate(Result):
    def dictionary_creator(self):
        return {"status": 200, "message": Result.language.SUCCESS_RANG_RATE, "params": self.params}
