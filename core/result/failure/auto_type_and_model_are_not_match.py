from core.result import Result


class AutoTypeAndModelNotMatched(Result):
    def dictionary_creator(self):
        return {"status": self.status, "message": Result.language.AUTO_TYPE_AND_MODEL_ARE_NOT_MATCH, "params": None}
