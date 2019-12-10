from core.interfaces.serialization import Serializable
from core.request.base_request import RequestBaseClass


class ListServiceGradesRequest(RequestBaseClass):

    def __init__(self, json_obj):
        self.car_id = None
        self.json_obj = json_obj

    def validate_pattern(self):
        res = self._id_checker(self.car_id)
        if not res[0]:
            return res

        return True,

    def _id_checker(self, id):
        if id is int:
            return False,
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
        if not type(self.json_obj) is dict:
            json_dict = Serializable.convert_input_to_dict(self.json_obj)
        else:
            json_dict = self.json_obj
        result = ListServiceGradesRequest.pre_deserialize(json_dict)
        if result[0]:
            self.car_id = json_dict['car_id']
            result_pattern = self.post_deserialize()
            if not result_pattern[0]:
                return result_pattern
            return True, self
        return result
