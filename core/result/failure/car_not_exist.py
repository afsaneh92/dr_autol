from core.result import Result


class CarNotExist(Result):
    def dictionary_creator(self):

        return {"status": self.status, "message": Result.language.CAR_NOT_EXIST, "params": self.params}
