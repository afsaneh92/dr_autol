from core.result import Result


class SuccessListServiceGrades(Result):
    def dictionary_creator(self):
        params = []
        for param in self.params:
            dct = {"service_grade_name": param.name, "id": param.id}
            params.append(dct)
        return {"status": 200, "message": Result.language.SUCCESS_LIST, "params": params}
