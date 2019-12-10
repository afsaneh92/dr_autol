from core.result import Result


class AutoIdDoseNotExist(Result):
    def dictionary_creator(self):

        return {"status": self.status, "message": Result.language.AUTO_ID_DOES_NOT_EXIST, "params": None}