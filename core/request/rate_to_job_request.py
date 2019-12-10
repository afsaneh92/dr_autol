from core.interfaces.serialization import Serializable
from core.messages.keys import Keys
from core.request.base_request import RequestBaseClass
from core.result import Result
from core.validation.session_helper.session_manager import SessionManager


class RateJobRequest(RequestBaseClass):

    def __init__(self, json_obj):

        self.json_obj = json_obj
        self.phone_number = None
        self.rate = None
        self.job_id = None

    def validate_pattern(self):
        invalid_params = []
        result = self._rate_checker(self.rate)
        if not result[0]:
            invalid_params.append(result[0])
        if len(invalid_params) > 0:
            return False, {Keys.INVALID_PARAMS: invalid_params}
        return True, "regex is valid"

    @staticmethod
    def _rate_checker(rate):
        rate_not_int = []
        for item in rate:
            if not isinstance(item, int) and item is not None:
                rate_not_int.append(Result.language.RATE_IS_NOT_INT)
        if len(rate_not_int) > 0:
            return False, rate_not_int
        else:
            return True,

    @staticmethod
    def pre_deserialize(json_dict):
        """
        before deserializing, run this method. It help to check json and confirm it's schema.
        :param json_dict:
        :return:
        """
        missed_params = []
        if Keys.JOB_ID not in json_dict:
            missed_params.append(Result.language.MISSING_JOB_IN_JSON)
        if Keys.RATE not in json_dict:
            missed_params.append(Result.language.MISSING_RATE_IN_JSON)
        if len(missed_params) > 0:
            return False, missed_params

        return True,

    @staticmethod
    def is_session_valid():
        return SessionManager.is_key_exist(key=Keys.PHONE_NUMBER)

    def post_deserialize(self):
        return self.validate_pattern()

    def deserialize(self):
        if not type(self.json_obj) is dict:
            json_dict = Serializable.convert_input_to_dict(self.json_obj)
        else:
            json_dict = self.json_obj
        result = RateJobRequest.pre_deserialize(json_dict)

        res = self.is_session_valid()
        if not res:
            return False, Result.language.SESSION_KEY_IS_NOT_VALID
        if result:
            self.phone_number = SessionManager.retrieve_session_value_by_key(key=Keys.PHONE_NUMBER)
            self.rate = json_dict[Keys.RATE]
            self.job_id = json_dict[Keys.JOB_ID]
            result_pattern = self.post_deserialize()
            if not result_pattern[0]:
                return result_pattern
            return True, self
        return result
