from core.result import Result


class SuccessAddServiceGrade(Result):
    def dictionary_creator(self):
        return {"status": 200, "message": Result.language.SUCCESS_ADD_SERVICE_GRADE, "params": self.params}
