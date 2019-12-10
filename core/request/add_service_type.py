from core.interfaces.serialization import Serializable
from core.request.base_request import RequestBaseClass
from persistence.database.entity.service_type import ServiceType


class NewServiceTypeRequest(RequestBaseClass):

    def __init__(self, json_obj):
        self.service_grades = None
        self.service_type = None
        self.json_obj = json_obj

    def validate_pattern(self):
        invalid_params = []
        for grade in self.service_grades:
            if not isinstance(grade, int):
                invalid_params.append("grade should be int")
        if len(self.service_type.name.strip()) == 0:
            invalid_params.append("name is invalid")
        if isinstance(self.service_type.price, int):
            if self.service_type.price <= 0:
                invalid_params.append("price should be greater than 0")
        else:
            invalid_params.append("price should be int")

        if len(invalid_params) > 0:
            return False, {"invalid_params": invalid_params}
        return True, "regex is valid"

    @staticmethod
    def pre_deserialize(json_dict):
        """
        before deserializing, run this method. It help to check json and confirm it's schema.
        :param json_dict:
        :return:
        """
        missed_params = []
        if 'service_type' not in json_dict:
            missed_params.append("missing_service_grade_name_in_json")
        else:
            if 'name' not in json_dict['service_type']:
                missed_params.append("missing_service_type_name_in_json")
            if 'price' not in json_dict['service_type']:
                missed_params.append("missing_price_in_json")
        if 'service_grades' not in json_dict:
            missed_params.append("missing_service_grades_in_json")

        if len(missed_params) > 0:
            return False, missed_params

        return True,

    def post_deserialize(self):
        return self.validate_pattern()

    def deserialize(self):
        if not type(self.json_obj) is dict:
            json_dict = Serializable.convert_input_to_dict(self.json_obj)
        else:
            json_dict = self.json_obj
        result = NewServiceTypeRequest.pre_deserialize(json_dict)
        if not result[0]:
            return result
        service_grades = json_dict['service_grades']
        service_type = ServiceType(name=json_dict['service_type']['name'],
                                   price=json_dict['service_type']['price'])
        self.service_type = service_type
        self.service_grades = service_grades
        result_pattern = self.post_deserialize()
        if not result_pattern[0]:
            return result_pattern
        return True, self
