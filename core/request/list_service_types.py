from core.request.base_request import RequestBaseClass
from core.validation.helpers import is_string_int


class ListServiceTypesRequest(RequestBaseClass):

    def __init__(self, service_grade_id):
        self.service_grade_id = service_grade_id

    def validate_pattern(self):
        res = self._id_checker(self.service_grade_id)
        if not res[0]:
            return res

        return True,

    def _id_checker(self, id):
        if not is_string_int(id):
            return False, "service grade should be int"
        return True,

    @staticmethod
    def pre_deserialize(json_dict):
        """
        before deserializing, run this method. It help to check json and confirm it's schema.
        :param json_dict:
        :return:
        """
        return True,

    def post_deserialize(self):
        return self.validate_pattern()

    def deserialize(self):
        result = ListServiceTypesRequest.pre_deserialize(self.service_grade_id)
        if result[0]:
            result_pattern = self.post_deserialize()
            if not result_pattern[0]:
                return result_pattern
            return True, self
        return result


