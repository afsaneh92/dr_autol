from core.interfaces.serialization import Serializable
from core.messages.keys import Keys
from core.request.base_request import RequestBaseClass
from core.result import Result
from core.validation.helpers import is_latitude, is_longitude, is_int
from persistence.database.entity.user.business_owner import BusinessOwner


class BusinessOwnerUpdateLocationRequest(RequestBaseClass):
    def __init__(self, json_obj):
        self.business_owner = None
        self.json_obj = json_obj

    def validate_pattern(self):
        if not is_latitude(self.business_owner.lat):
            return False, 'lat is wrong'
        if not is_longitude(self.business_owner.lng):
            return False, 'lng is wrong'

        if not is_int(self.business_owner.id):
            return False, "Service grade name is not valid"
        return True, self

    @staticmethod
    def pre_deserialize(json_dict):
        """
        before deserializing, run this method. It help to check json and confirm it's schema.
        :param json_dict:
        :return:
        """
        missed_params = []
        if Keys.LATITUDE not in json_dict:
            missed_params.append(Result.language.MISSING_LATITUDE_IN_JSON)
        if Keys.LONGITUDE not in json_dict:
            missed_params.append(Result.language.MISSING_LONGITUDE_IN_JSON)
        if Keys.BUSINESS_OWNER_ID not in json_dict:
            missed_params.append(Result.language.MISSING_BUSINESS_OWNER_ID_IN_JSON)

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
        result = BusinessOwnerUpdateLocationRequest.pre_deserialize(json_dict)
        if not result[0]:
            return result
        self.business_owner = BusinessOwner(id=json_dict[Keys.BUSINESS_OWNER_ID], lat=json_dict[Keys.LATITUDE],
                                             lng=json_dict[Keys.LONGITUDE])
        result_pattern = self.post_deserialize()
        if not result_pattern[0]:
            return result_pattern
        return True, self
