from core.result import Result


class SuccessUpdate(Result):
    def dictionary_creator(self):
        return {"status": 200, "message": self.message, "params": self.params}
