from core.result import Result


class SuccessNewPass(Result):
    def dictionary_creator(self):
        return {"status": 200, "message": Result.language.SUCCESS_CHANGE_PASSWORD, "params": self.params}
