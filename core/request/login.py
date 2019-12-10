from core.interfaces.serialization import Serializable
from core.messages.keys import Keys
from core.request.base_request import RequestBaseClass
from core.result import Result
from core.validation.helpers import phone_number_regex_checker, password_regex_checker


class LoginRequest(RequestBaseClass):

    def __init__(self, json_obj):
        self.phone_number = None
        self.password = None
        self.reg_id = None
        self.os = None
        self.json_obj = json_obj
        self.type = None

    def validate_pattern(self):
        invalid_params = []

        result = self._password_checker(self.password)
        if not result[0]:
            invalid_params.append(result[1])
        result = self._phone_number_checker(self.phone_number)
        if not result[0]:
            invalid_params.append(result[1])

        if len(invalid_params) > 0:
            return False, {Keys.INVALID_PARAMS: invalid_params}
        return True, Keys.REGEX_IS_VALID

    def _phone_number_checker(self, phone_number):
        return phone_number_regex_checker(phone_number)

    def _password_checker(self, password):
        return password_regex_checker(password)

    @staticmethod
    def pre_deserialize(json_dict):
        """
        before deserializing, run this method. It help to check json and confirm it's schema.
        :param json_dict:
        :return:
        """
        missed_params = []
        if Keys.PHONE_NUMBER not in json_dict:
            missed_params.append(Result.language.MISSING_PHONE_NUMBER_IN_JSON)
        if Keys.PASSWORD not in json_dict:
            missed_params.append(Result.language.MISSING_PASSWORD_IN_JSON)
        if Keys.REG_ID not in json_dict:
            missed_params.append(Result.language.MISSING_REG_ID_IN_JSON)
        if Keys.OS not in json_dict:
            missed_params.append(Result.language.MISSING_OS_IN_JSON)
        if len(missed_params) > 0:
            return False, missed_params

        return True,

    @staticmethod
    def pre_deserialize_supplier(json_dict):
        """
        before deserializing, run this method. It help to check json and confirm it's schema.
        :param json_dict:
        :return:
        """
        missed_params = []
        if Keys.PHONE_NUMBER not in json_dict:
            missed_params.append(Result.language.MISSING_PHONE_NUMBER_IN_JSON)
        if Keys.PASSWORD not in json_dict:
            missed_params.append(Result.language.MISSING_PASSWORD_IN_JSON)
        if len(missed_params) > 0:
            return False, missed_params

        return True,

    def post_deserialize(self):
        return self.validate_pattern()

    def deserialize(self):
        if Keys.USER_TYPE not in self.json_obj:
            return False, Result.language.MISSING_PHONE_NUMBER_IN_JSON

        if not type(self.json_obj) is dict:
            json_dict = Serializable.convert_input_to_dict(self.json_obj)
        else:
            json_dict = self.json_obj
            self.type = json_dict[Keys.USER_TYPE]
        if not self.type == Keys.SUPPLIER:
            result = self.deserialize_none_supplier_users(json_dict)
        else:
            result = self.deserialize_supplier_users(json_dict)
        return result

    def deserialize_none_supplier_users(self, json_dict):
        result = LoginRequest.pre_deserialize(json_dict)
        if result[0]:
            self.phone_number = json_dict[Keys.PHONE_NUMBER]
            self.password = json_dict[Keys.PASSWORD]
            self.reg_id = json_dict[Keys.REG_ID]
            self.os = json_dict[Keys.OS]
            result_pattern = self.post_deserialize()
            if not result_pattern[0]:
                return result_pattern
            return True, self
        return result

    def deserialize_supplier_users(self, json_dict):
        result = LoginRequest.pre_deserialize_supplier(json_dict)
        if result[0]:
            self.phone_number = json_dict[Keys.PHONE_NUMBER]
            self.password = json_dict[Keys.PASSWORD]
            result_pattern = self.post_deserialize()
            if not result_pattern[0]:
                return result_pattern
            return True, self
        return result
