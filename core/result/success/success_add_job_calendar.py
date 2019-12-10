from core.result import Result


class SuccessAddNewJob(Result):
    def dictionary_creator(self):
        return {"status": 200, "message": Result.language.SUCCESS_ADD_NEW_JOB}
