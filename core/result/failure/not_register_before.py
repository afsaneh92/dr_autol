from core.result import Result


class NotRegisteredBefore(Result):
    def dictionary_creator(self):
        return {"status": self.status, "message": Result.language.NOT_REGISTERED_BEFORE}