from core.interfaces.serialization import Serializable
from core.messages.keys import Keys
from core.request.base_request import RequestBaseClass
from core.result import Result
from core.validation.session_helper.session_manager import SessionManager
from persistence.database.entity.job_.job import Job
from persistence.database.entity.user.car_owner import CarOwner


class CancellationByCarOwnerRequest(RequestBaseClass):

    def __init__(self, json_obj):
        self.job = None
        self.car_owner = None
        self.json_obj = json_obj

    def validate_pattern(self):
        res = self._id_checker(self.job.id)
        if not res[0]:
            return res

        return True, res

    def _id_checker(self, id):
        if id is int:
            return False,
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
        if not SessionManager.is_key_exist(Keys.USER_ID):
            missed_params.append(Result.language.SESSION_KEY_IS_ABSENT)

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
        result = CancellationByCarOwnerRequest.pre_deserialize(json_dict)
        if result[0]:
            self.job = Job(json_dict[Keys.JOB_ID])
            self.car_owner = CarOwner(id=SessionManager.retrieve_session_value_by_key(Keys.USER_ID))
            result_pattern = self.post_deserialize()
            if not result_pattern[0]:
                return result_pattern
            return True, self.job
        return result
