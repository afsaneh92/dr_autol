from core.result import Result


class BadIdType(Result):
    def dictionary_creator(self):

        return {"status": self.status, "message": Result.language.ID_IS_NOT_INTEGER, "params": None}