from core.result import Result


class SuccessCreate(Result):
    def dictionary_creator(self):
        return {"status": 200}
