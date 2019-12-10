from flask import session
from core.interfaces.serialization import Serializable
from core.messages.keys import Keys
from core.request.base_request import RequestBaseClass
from core.result import Result
from core.validation.helpers import phone_number_regex_checker, is_request_json, password_regex_checker, \
    code_validation_regex_checker


class States(object):
    PHONE_NUMBER = Keys.PHONE_NUMBER
    CODE = Keys.CODE
    PASSWORD = Keys.PASSWORD
    RESEND_CODE = Keys.RESEND_CODE


class ForgetPasswordRequest(RequestBaseClass):
    def __init__(self, json_obj, state_id):
        self.phone_number = None
        self.state_id = state_id
        self.json_obj = json_obj

    def validate_pattern_state_phone_number(self):
        invalid_params = []
        result = self._phone_number_checker(self.phone_number)
        if not result[0]:
            invalid_params.append(result[1])
        if len(invalid_params) > 0:
            return False, {Keys.INVALID_PARAMS: invalid_params}
        return True, Result.language.REGEX_IS_VALID

    def validate_pattern_state_code(self):
        invalid_params = []
        result = self._code_checker(self.code)
        if not result[0]:
            invalid_params.append(result[1])
        if len(invalid_params) > 0:
            return False, {Keys.INVALID_PARAMS: invalid_params}
        return True, Result.language.REGEX_IS_VALID

    def validate_pattern_state_password(self):
        invalid_params = []
        result = self._password_checker(self.password)
        if not result[0]:
            invalid_params.append(result[1])
        if len(invalid_params) > 0:
            return False, {Keys.INVALID_PARAMS: invalid_params}
        return True, Result.language.REGEX_IS_VALID

    def _phone_number_checker(self, phone_number):
        return phone_number_regex_checker(phone_number)

    def _password_checker(self, password):
        return password_regex_checker(password)

    def _code_checker(self, code):
        return code_validation_regex_checker(code)

    @staticmethod
    def _pre_deserialize_template(json_dict, key, message):
        """
                before deserializing, run this method. It help to check json and confirm it's schema.
                :param json_dict:
                :return:
                """
        missed_params = []
        if key not in json_dict:
            missed_params.append(message)

        if len(missed_params) > 0:
            return False, missed_params

        return True,

    @staticmethod
    def pre_deserialize_state_phone_number(json_dict):
        """
                        before deserializing, run this method. It help to check json and confirm it's schema.
                        :param json_dict:
                        :return:
                        """
        missed_params = []
        if Keys.PHONE_NUMBER not in json_dict:
            missed_params.append(Result.language.MISSING_PHONE_NUMBER_IN_JSON)
        if Keys.TYPE_USER not in json_dict:
            missed_params.append(Result.language.MISSING_TYPE_USER_IN_JSON)

        if len(missed_params) > 0:
            return False, missed_params

        return True,

    @staticmethod
    def pre_deserialize_state_code(json_dict):
        return ForgetPasswordRequest._pre_deserialize_template(json_dict, Keys.CODE, Result.language.MISSING_CODE_IN_JSON)

    @staticmethod
    def pre_deserialize_state_password(json_dict):
        return ForgetPasswordRequest._pre_deserialize_template(json_dict, Keys.PASSWORD, Result.language.MISSING_PASSWORD_IN_JSON )

    def post_deserialize_state_phone_number(self):
        return self.validate_pattern_state_phone_number()

    def post_deserialize_state_state_code(self):
        return self.validate_pattern_state_code()

    def post_deserialize_state_password(self):
        return self.validate_pattern_state_password()

    def validate_pattern(self):
        return True

    def deserialize(self):

        if self.state_id == Keys.PHONE_NUMBER:
            if not type(self.json_obj) is dict:
                json_dict = Serializable.convert_input_to_dict(self.json_obj)
            else:
                json_dict = self.json_obj
            result = ForgetPasswordRequest.pre_deserialize_state_phone_number(json_dict)
            if result[0]:
                self.phone_number = self.json_obj[Keys.PHONE_NUMBER]
                self.type_user = self.json_obj[Keys.TYPE_USER]
                session[Keys.FORGET_PASS][Keys.TYPE_USER] = self.json_obj[Keys.TYPE_USER]
                result_pattern = self.post_deserialize_state_phone_number()
                if not result_pattern[0]:
                    return result_pattern

                return True, self
            else:
                return result

        elif self.state_id == Keys.CODE:
            if not type(self.json_obj) is dict:
                json_dict = Serializable.convert_input_to_dict(self.json_obj)
            else:
                json_dict = self.json_obj
            result = ForgetPasswordRequest.pre_deserialize_state_code(json_dict)
            if result[0]:
                self.phone_number = self.json_obj[Keys.PHONE_NUMBER]
                self.code = json_dict[Keys.CODE]
                result_pattern = self.post_deserialize_state_state_code()
                if not result_pattern[0]:
                    session[Keys.FORGET_PASS][Keys.STATE_ID] = Keys.PHONE_NUMBER
                    return result_pattern
                return True, self
            else:
                session[Keys.FORGET_PASS][Keys.STATE_ID] = Keys.PHONE_NUMBER
                return result

        elif self.state_id == Keys.PASSWORD:
            self.phone_number = session[Keys.FORGET_PASS][Keys.USER_ID]
            if not type(self.json_obj) is dict:
                json_dict = Serializable.convert_input_to_dict(self.json_obj)
            else:
                json_dict = self.json_obj
            result = ForgetPasswordRequest.pre_deserialize_state_password(json_dict)
            if result[0]:
                self.password = json_dict[Keys.PASSWORD]
                result_pattern = self.post_deserialize_state_password()
                if not result_pattern[0]:
                    return result_pattern
                return True, self
            else:
                return result
        elif self.state_id == Keys.RESEND_CODE:
                return True, self
        else:
            return False, Result.language.WRONG_STATE

