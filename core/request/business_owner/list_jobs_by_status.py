import numbers

from core.interfaces.serialization import Serializable
from core.messages.keys import Keys
from core.request.base_request import RequestBaseClass
from core.result import Result
from core.validation.session_helper.session_manager import SessionManager
from persistence.database.entity.user.business_owner import BusinessOwner


class ListJobsByStatusRequest(RequestBaseClass):
    def __init__(self, json_obj):
        self.business_owner = None
        self.status = None
        self.json_obj = json_obj

    def validate_pattern(self):
        if not isinstance(self.status, list):
            return False, 'status is wrong'
        if not isinstance(self.business_owner.id, numbers.Number):
            return False, 'id is not a number'
        return True, self

    @staticmethod
    def pre_deserialize(json_dict):
        """
        before deserializing, run this method. It help to check json and confirm it's schema.
        :param json_dict:
        :return:
        """
        missed_params = []
        if not SessionManager.is_key_exist(Keys.USER_ID):
            missed_params.append(Result.language.MISSING_BUSINESS_OWNER_ID_IN_JSON)
        if Keys.STATUS not in json_dict:
            missed_params.append(Result.language.MISSING_STATUS_IN_JSON)

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
        result = ListJobsByStatusRequest.pre_deserialize(json_dict)
        if not result[0]:
            return result
        self.business_owner = BusinessOwner(id=SessionManager.retrieve_session_value_by_key(Keys.USER_ID))
        self.status = json_dict[Keys.STATUS]
        result_pattern = self.post_deserialize()
        if not result_pattern[0]:
            return result_pattern
        return True, self
