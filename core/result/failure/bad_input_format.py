from core.result import Result


class BadInputFormat(Result):
    def dictionary_creator(self):
        dct = {"status": self.status, "message": Result.language.BAD_SCHEMA, "params": self.params}
        return dct
