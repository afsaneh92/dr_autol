from core.result import Result


class SuccessCarOwnerOrder(Result):
    def dictionary_creator(self):
        params = []
        for param in self.params:
            dct = {"status": param.status, "business_owner": param.workspace_name, "plate_number": param.plate_number,
                   "start_time": param.start_schedule, "job_id": param.id}
            params.append(dct)
        return {"status": self.status, "message": Result.language.SUCCESS_ADD_NEW_USER, "param": params}
