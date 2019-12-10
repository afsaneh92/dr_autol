from core.messages.keys import Keys
from core.request.base_request import RequestBaseClass
from core.result import Result
from core.validation.helpers import phone_number_regex_checker, password_regex_checker
from core.validation.session_helper.session_manager import SessionManager


class SupplierDailyPurchaseListRequest(RequestBaseClass):

    def __init__(self):
        self.phone_number = None
        self.user_id = None

    def validate_pattern(self):
        invalid_params = []
        if not isinstance(self.user_id, int):
            return False, Result.language.ID_IS_NOT_INTEGER

        result = self._phone_number_checker(self.phone_number)
        if not result[0]:
            invalid_params.append(result[1])

        if len(invalid_params) > 0:
            return False, {Keys.INVALID_PARAMS: invalid_params}
        return True, Keys.REGEX_IS_VALID

    def _phone_number_checker(self, phone_number):
        return phone_number_regex_checker(phone_number)

    @staticmethod
    def is_session_valid():
        return SessionManager.is_key_exist(key=Keys.PHONE_NUMBER)

    @staticmethod
    def pre_deserialize():
        """
        before deserializing, run this method. It help to check json and confirm it's schema.
        :param json_dict:
        :return:
        """
        res = SupplierDailyPurchaseListRequest.is_session_valid()
        if not res:
            return False, Result.language.SESSION_KEY_IS_NOT_VALID

        return True,

    def post_deserialize(self):
        return self.validate_pattern()

    def deserialize(self):

        result = SupplierDailyPurchaseListRequest.pre_deserialize()
        if result[0]:
            self.phone_number = SessionManager.retrieve_session_value_by_key(key=Keys.PHONE_NUMBER)
            self.user_id = SessionManager.retrieve_session_value_by_key(key=Keys.USER_ID)
            result_pattern = self.post_deserialize()
            if not result_pattern[0]:
                return result_pattern
            return True, self
        return result
