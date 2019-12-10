from core.result import Result


class SuccessListCars(Result):
    def dictionary_creator(self):
        params = []
        for param in self.params:
            dct = {"vin_number": param[1], "plate_number": param[2], "id": param[3], "auto_type": param[4],
                   "auto_type_id": param[5]}
            params.append(dct)
        return {"status": 200, "message": Result.language.SUCCESS_LIST, "params": params}
