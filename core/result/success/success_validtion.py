from core.result import Result


class SuccessValidation(Result):
    def dictionary_creator(self):
        return {"status": self.status, "message": self.message, "params": self.params}
