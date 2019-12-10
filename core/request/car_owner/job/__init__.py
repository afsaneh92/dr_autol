import logging

from core.interfaces.serialization import Serializable
from core.messages.keys import Keys
from core.messages.translator.situations import ReflectionRequests
from core.result import Result
from core.result.failure.invalid_class import InvalidClass
from core.validation.helpers import create_class_dynamically

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class JobBaseRequest(object):
    dct = {
        Keys.AUTO_SERVICE_JOB_REQUEST: ReflectionRequests.AUTO_SERVICE_JOB_REQUEST,
        Keys.INSURANCE_JOB_REQUEST: ReflectionRequests.INSURANCE_JOB_REQUEST,
    }

    def __init__(self, json_obj):
        self.json_obj = json_obj

    @staticmethod
    def pre_deserialize(json_dict):
        missed_params = []
        if Keys.USER_TYPE not in json_dict:
            missed_params.append(Result.language.MISSING_REQUEST_TYPE_JSON)
        if len(missed_params) > 0:
            return False, missed_params

        return True,

    # @staticmethod
    # def pre_deserialize(json_dict):
    #
    #     missed_params = []
    #     if Keys.REQUEST_TYPE not in json_dict:
    #         missed_params.append("is full or installment?")
    #     if Keys.PAYMENT_TYPE not in json_dict:
    #         missed_params.append(Result.language.MISSING_PAYMENT_TYPE)
    #     if Keys.PAYMENT_AMOUNT not in json_dict:
    #         missed_params.append(Result.language.MISSING_PAYMENT_AMOUNT)
    #     if Keys.TRANSACTION_NUMBER not in json_dict:
    #         missed_params.append(Result.language.MISSING_TRANSACTION_NUMBER)
    #     if Keys.JOB_ID not in json_dict:
    #         missed_params.append(Result.language.MISSING_JOB_ID)
    #
    #     if len(missed_params) > 0:
    #         return False, missed_params
    #
    #     return True,

    def deserialize(self):
        if not type(self.json_obj) is dict:
            json_dict = Serializable.convert_input_to_dict(self.json_obj)
        else:
            json_dict = self.json_obj
        result = JobBaseRequest.pre_deserialize(json_dict)
        if not result[0]:
            return result
        result = JobBaseRequest.generate_appropriate_request(json_dict[Keys.USER_TYPE], JobBaseRequest.dct)
        if not result[0]:
            res = False, result[1].params
            return res

        return JobBaseRequest.child_class_deserialize(result[1], json_dict)

    @staticmethod
    def generate_appropriate_request(class_type, dct):
        if class_type not in dct.keys():
            return False, InvalidClass(status=400, message=Result.language.NO_CLASS_PATH,
                                       params={Keys.USER_TYPE: class_type})
        type_ = dct[class_type]
        return create_class_dynamically(logger, type_['module'], type_['class'], class_type)

    @staticmethod
    def child_class_deserialize(klass, json_dict):
        model = klass(json_dict)
        result = model.deserialize()
        if result[0]:
            return result[0], result[1], json_dict[Keys.USER_TYPE]
        return result
