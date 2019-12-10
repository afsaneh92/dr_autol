from core.result import Result


class ValidatedBefore(Result):
    def dictionary_creator(self):
        return {"status": self.status, "message": self.message}
