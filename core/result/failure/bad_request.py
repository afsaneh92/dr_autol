from core.result import Result


class BadRequest(Result):
    def dictionary_creator(self):
        return {"status": self.status}
