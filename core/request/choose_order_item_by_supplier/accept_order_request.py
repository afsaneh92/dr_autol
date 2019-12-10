from core.interfaces.serialization import Serializable
from core.messages.keys import Keys
from core.request.base_request import RequestBaseClass
from core.result import Result
from persistence.database.entity.order_items import OrderItem


class AcceptOrderRequest(RequestBaseClass):
    def __init__(self, json_obj):
        self.order = None
        self.json_obj = json_obj

    def validate_pattern(self):
        if not isinstance(self.order.id, int):
            return False, Result.language.Keys.ORDER_ID_IS_NOT_INT
        return True,

    @staticmethod
    def pre_deserialize(json_dict):
        """
        before deserializing, run this method. It help to check json and confirm it's schema.
        :param json_dict:
        :return:
        """
        missed_params = []
        if Keys.ORDER_ID not in json_dict:
            missed_params.append(Result.language.MISSING_JOB_IN_JSON)

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
        result = AcceptOrderRequest.pre_deserialize(json_dict)
        if not result[0]:
            return result
        self.order = OrderItem(id=json_dict[Keys.ORDER_ID])
        result_pattern = self.post_deserialize()
        if not result_pattern[0]:
            return result_pattern
        return True, self
