from core.messages.keys import Keys
from core.request.base_request import RequestBaseClass
from core.interfaces.serialization import Serializable
from core.result import Result
from core.validation.helpers import is_int
from persistence.database.entity.job_.job import Job
from persistence.database.entity.payment_.full import FullPayment


class FullRequest(RequestBaseClass):
    def __init__(self, json_obj):
        self.job = None
        self.json_obj = json_obj

    def validate_pattern(self):
        invalid_params = []

        result = is_int(self.payment.amount)
        if not result:
            invalid_params.append(Result.language.PAYMENT_AMOUNT_IS_NOT_DECIMAL)
        result = is_int(self.job.id)
        if not result:
            invalid_params.append(Result.language.JOB_ID_IS_NOT_INT)
        result = is_int(self.payment.payment_type_id)
        if not result:
            invalid_params.append(Result.language.PAYMENT_TYPE_IS_NOT_VALID)

        if len(invalid_params) > 0:
            return False, {Keys.INVALID_PARAMS: invalid_params}

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

        if len(missed_params) > 0:
            return False, missed_params

        return True,

    def post_deserialize(self):
        # return True,
        return self.validate_pattern()

    def deserialize(self):
        if not type(self.json_obj) is dict:
            json_dict = Serializable.convert_input_to_dict(self.json_obj)
        else:
            json_dict = self.json_obj
        result = FullRequest.pre_deserialize(json_dict)
        if not result[0]:
            return result

        self.job = Job(id=json_dict[Keys.JOB_ID])
        self.payment = FullPayment(payment_type_id=json_dict[Keys.PAYMENT_TYPE], amount=json_dict[Keys.PAYMENT_AMOUNT],
                               currency='IRR', transaction_number=json_dict[Keys.TRANSACTION_NUMBER])
        result_pattern = self.post_deserialize()
        if not result_pattern[0]:
            return result_pattern
        return True, self
