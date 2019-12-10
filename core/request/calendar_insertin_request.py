from core.interfaces.serialization import Serializable
from core.messages.keys import Keys
from core.request.base_request import RequestBaseClass
from core.result import Result
from core.validation.helpers import time_regex_checker


class CalendarInsertionRequest(RequestBaseClass):

    def __init__(self, json_obj):
        self.start_time = None
        self.finish_time = None
        self.business_owners_id = None
        self.json_obj = json_obj

    def validate_pattern(self):
        invalid_params = []
        if not isinstance(self.business_owners_id, int):
            return False, Result.language.POST_VALIDATION_BUSINESS_OWNER_ID
        result = self._time_regex_checker(self.start_time)
        if not result[0]:
            invalid_params.append(result[1])
        result = self._time_regex_checker(self.finish_time)
        if not result[0]:
            invalid_params.append(result[1])
        if len(invalid_params) > 0:
            return False, {"invalid_params": invalid_params}
        return True, "regex is valid"

    def _time_regex_checker(self, date):
        return time_regex_checker(date)

    def post_deserialize(self):
        return self.validate_pattern()

    @staticmethod
    def pre_deserialize(json_dict):
        """
             before deserializing, run this method. It help to check json and confirm it's schema.
             :param json_dict:
             :return:
             """
        missed_params = []

        if Keys.BUSINESS_OWNER_ID not in json_dict:
            missed_params.append(Result.language.MISSING_BUSINESS_OWNER_ID_IN_JSON)
        if Keys.START_TIME not in json_dict:
            missed_params.append(Result.language.MISSING_START_TIME_IN_JSON)
        if Keys.FINISH_TIME not in json_dict:
            missed_params.append(Result.language.MISSING_FINISH_TIME_IN_JSON)

        if len(missed_params) > 0:
            return False, missed_params

        return True,

    def deserialize(self):
        if not type(self.json_obj) is dict:
            json_dict = Serializable.convert_input_to_dict(self.json_obj)
        else:
            json_dict = self.json_obj
        result = CalendarInsertionRequest.pre_deserialize(json_dict)
        if result[0]:
            self.start_time = json_dict[Keys.START_TIME]
            self.finish_time = json_dict[Keys.FINISH_TIME]
            self.business_owners_id = json_dict[Keys.BUSINESS_OWNER_ID]
            result_pattern = self.post_deserialize()
            if not result_pattern[0]:
                return result_pattern
            return True, self
        return result
