from core.result import Result


class SuccessDeleteNewCar(Result):
    def dictionary_creator(self):
        return {"status": 200, "message": Result.language.SUCCESS_DELETE_CAR, "params": self.params}
