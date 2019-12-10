from core.result import Result


class InvalidServiceGrade(Result):
    def dictionary_creator(self):

        return {"status": self.status, "message": Result.language.INVALID_SERVICE_GRADE}
