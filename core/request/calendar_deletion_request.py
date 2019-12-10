from core.interfaces.serialization import Serializable
from core.messages.keys import Keys
from core.request.base_request import RequestBaseClass
from core.result import Result


class CalendarDeletionRequest(RequestBaseClass):

    def __init__(self, json_obj):

        self.json_obj = json_obj
        self.id = None

    def validate_pattern(self):

        if not isinstance(self.id, int):
            return False, Result.language.POST_VALIDATION_CALENDAR_ID
        return True, Keys.REGEX_IS_VALID

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

        if Keys.CALENDAR_ID not in json_dict:
            missed_params.append(Result.language.MISSING_CALENDAR_ID_IN_JSON)

        if len(missed_params) > 0:
            return False, missed_params

        return True,

    def deserialize(self):
        if not type(self.json_obj) is dict:
            json_dict = Serializable.convert_input_to_dict(self.json_obj)
        else:
            json_dict = self.json_obj
        result = CalendarDeletionRequest.pre_deserialize(json_dict)
        if result[0]:
            self.id = json_dict[Keys.CALENDAR_ID]
            result_pattern = self.post_deserialize()
            if not result_pattern[0]:
                return result_pattern
            return True, self
        return result
