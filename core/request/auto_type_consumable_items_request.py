from core.validation.helpers import is_int
from core.interfaces.serialization import Serializable
from core.messages.keys import Keys
from core.request.base_request import RequestBaseClass
from core.result import Result


class ListAutoTypeConsumableItemsRequest(RequestBaseClass):

    def __init__(self, json_ob):
        self.json_obj = json_ob
        self.auto_type_id = None
        self.service_type_id = None

    def validate_pattern(self):
        res = self._auto_id_checker(self.auto_type_id)
        result = self._auto_id_checker(self.service_type_id)
        if not res[0] or not result[0]:
            return res

        return True,

    def _auto_id_checker(self, id):
        result = is_int(id)
        if not result:
            return False,
        return True,

    @staticmethod
    def pre_deserialize(json_dict):
        """
        before deserializing, run this method. It help to check json and confirm it's schema.
        :param json_dict:
        :return:
        """
        missed_params = []
        if Keys.AUTO_TYPE_ID not in json_dict:
            missed_params.append(Result.language.MISSING_AUTO_TYPE_ID_IN_JSON)
        if Keys.SERVICE_TYPE_ID not in json_dict:
            missed_params.append(Result.language.MISSING_SERVICE_TYPE_ID)
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
        result = ListAutoTypeConsumableItemsRequest.pre_deserialize(json_dict)
        if result[0]:
            self.auto_type_id = json_dict[Keys.AUTO_TYPE_ID]
            self.service_type_id = json_dict[Keys.SERVICE_TYPE_ID]

            result_pattern = self.post_deserialize()
            if not result_pattern[0]:
                return result_pattern
            return True, self
        return result
