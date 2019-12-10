from core.interfaces.serialization import Serializable
from core.request.base_request import RequestBaseClass
from persistence.database.entity.service_grade import ServiceGrade


class NewServiceGradeRequest(RequestBaseClass):

    def __init__(self, json_obj):
        self.service_grade = None
        self.json_obj = json_obj

    def validate_pattern(self):
        if len(self.service_grade.name.strip()) == 0:
            return False, "Service grade name is not valid"
        return True,

    @staticmethod
    def pre_deserialize(json_dict):
        """
        before deserializing, run this method. It help to check json and confirm it's schema.
        :param json_dict:
        :return:
        """
        missed_params = []
        if 'service_grade_name' not in json_dict:
            missed_params.append("missing_service_grade_name_in_json")

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
        result = NewServiceGradeRequest.pre_deserialize(json_dict)
        if not result[0]:
            return result

        service_grade = ServiceGrade(name=json_dict['service_grade_name'])
        self.service_grade = service_grade
        result_pattern = self.post_deserialize()
        if not result_pattern[0]:
            return result_pattern
        return True, self
