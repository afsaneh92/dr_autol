from core.result import Result


class SuccessRateBusinessOwner(Result):
    def dictionary_creator(self):
        return {"status": 200, "message": Result.language.BUSINESS_OWNER_IS_RATED, "params": self.params}
