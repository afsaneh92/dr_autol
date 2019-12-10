
from core.interfaces.serialization import Serializable
from core.messages.keys import Keys
from core.request.base_request import RequestBaseClass
from core.result import Result
from core.validation.helpers import password_regex_checker
from core.validation.session_helper.session_manager import SessionManager


class ChangePasswordRequest(RequestBaseClass):
    def __init__(self, json_obj):
        self.json_obj = json_obj

    def validate_pattern(self):
        invalid_params = []
        result = self._password_checker(self.old_password)
        if not result[0]:
            invalid_params.append(result[1])
        result = self._password_checker(self.new_password)
        if not result[0]:
            invalid_params.append(result[1])
        if len(invalid_params) > 0:
            return False, {Keys.INVALID_PARAMS: invalid_params}
        return True, Result.language.REGEX_IS_VALID

    # def is_not_empty_password(self):
    #     if len(self) == 0:
    #         return False
    #     else:
    #         return True

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
        if Keys.OLD_PASSWORD not in json_dict:
            missed_params.append(Result.language.MISSING_PASSWORD_IN_JSON)
        if Keys.NEW_PASSWORD not in json_dict:
            missed_params.append(Result.language.MISSING_PASSWORD_IN_JSON)
        if Keys.TYPE_USER not in json_dict:
            missed_params.append(Result.language.MISSING_TYPE_USER_IN_JSON)
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
        result = ChangePasswordRequest.pre_deserialize(json_dict)
        if result[0]:
            self.phone_number = SessionManager.retrieve_session_value_by_key(Keys.PHONE_NUMBER)
            self.old_password = json_dict[Keys.OLD_PASSWORD]
            self.new_password = json_dict[Keys.NEW_PASSWORD]
            self.type_user = json_dict[Keys.TYPE_USER]
            result_pattern = self.post_deserialize()
            if not result_pattern[0]:
                return result_pattern
            return True, self
        return result
