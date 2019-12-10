from core.interfaces.serialization import Serializable
from core.messages.keys import Keys
from core.request.base_request import RequestBaseClass
from core.result import Result
from core.validation.helpers import is_int


class ActivationStateRequest(RequestBaseClass):
    def __init__(self, json_obj):
        self.business_owner_id = None
        self.json_obj = json_obj

    def validate_pattern(self):
        invalid_params = []
        result = is_int(self.business_owner_id)
        if not result:
            invalid_params.append(Result.language.ID_IS_NOT_INTEGER)
        if len(invalid_params) > 0:
            return False, {'invalid_params': invalid_params}
        return True,

    @staticmethod
    def pre_deserialize(json_dict):
        """
        before deserializing, run this method. It help to check json and confirm it's schema.
        :param json_dict:
        :return:
        """
        missed_params = []
        if Keys.BUSINESS_OWNER_ID not in json_dict:
            missed_params.append(Result.language.MISSING_ID_IN_JSON)

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
        result = ActivationStateRequest.pre_deserialize(json_dict)
        if result[0]:
            self.business_owner_id = json_dict[Keys.BUSINESS_OWNER_ID]
            result_pattern = self.post_deserialize()
            if not result_pattern[0]:
                return result_pattern
            return True, self
        return result
