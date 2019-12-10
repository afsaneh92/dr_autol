from core.messages.keys import Keys
from core.request.base_request import RequestBaseClass
from core.result import Result
from core.validation.session_helper.session_manager import SessionManager


class BusinessOwnerRestCreditRequest(RequestBaseClass):
    def __init__(self):
        self.phone_number = None
        self.business_owner_id = None

    def validate_pattern(self):
        return True,

    @staticmethod
    def pre_deserialize(json_dict):
        """
        before deserializing, run this method. It help to check json and confirm it's schema.
        :param json_dict:
        :return:
        """
        return True,

    @staticmethod
    def is_session_valid():
        return SessionManager.is_key_exist(key=Keys.PHONE_NUMBER)

    def deserialize(self):
        res = self.is_session_valid()
        if not res:
            return False, Result.language.SESSION_KEY_IS_NOT_VALID

        self.phone_number = SessionManager.retrieve_session_value_by_key(key=Keys.PHONE_NUMBER)
        self.business_owner_id = SessionManager.retrieve_session_value_by_key(key=Keys.USER_ID)

        return True, self
