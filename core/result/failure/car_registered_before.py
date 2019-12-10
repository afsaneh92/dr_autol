from core.result import Result


class CarRegisteredBefore(Result):
    def dictionary_creator(self):

        return {"status": self.status, "message": Result.language.CAR_REGISTERED_BEFORE, "params": self.params}
