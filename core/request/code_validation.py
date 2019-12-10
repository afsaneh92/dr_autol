import re

from core.messages import fail_keys
from core.request.base_request import RequestBaseClass
from core.interfaces.serialization import Serializable


class CodeValidationRequest(RequestBaseClass):

    def __init__(self, json_obj):
        self.phone_number = None
        self.code = None
        self.json_obj = json_obj

    def validate_pattern(self):
        res = self._code_checker(self.code)
        if not res[0]:
            return res
        return True,

    def _code_checker(self, code):
        if re.match(r'^[0-9]{4}$', code):
            return True,
        else:
            return False, fail_keys.FailKeysForJSON.code_pattern_is_not_valid

    @staticmethod
    def pre_deserialize(json_dict):
        """
        before deserializing, run this method. It help to check json and confirm it's schema.
        :param json_dict:
        :return:
        """
        result = True,
        if 'phone_number' not in json_dict:
            result = False, "missing_phone_number_in_json"
        elif 'code' not in json_dict:
            result = False, "missing_code_in_json"

        return result

    def post_deserialize(self):
        return self.validate_pattern()

    def deserialize(self):
        if not type(self.json_obj) is dict:
            json_dict = Serializable.convert_input_to_dict(self.json_obj)
        else:
            json_dict = self.json_obj
        result = CodeValidationRequest.pre_deserialize(json_dict)
        if result[0]:
            self.code = json_dict['code']
            self.phone_number = json_dict['phone_number']
            result_pattern = self.post_deserialize()
            if not result_pattern[0]:
                return result_pattern
            return True, self
        return result
