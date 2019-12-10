from core.result import Result


class SuccessListServiceTypes(Result):
    def dictionary_creator(self):
        params = {}
        service_type_list = []
        if len(self.params) == 1:
            params = {"service_grade_id": self.params[0].id, "service_grade_name": self.params[0].name}
            service_types = self.params[0].service_types
            for service_type in service_types:
                a = {"id": service_type.id, "name": service_type.name, "price": service_type.price}
                service_type_list.append(a)
            params["service_types"] = service_type_list
        return {"status": 200, "message": Result.language.SUCCESS_LIST, "params": params}
