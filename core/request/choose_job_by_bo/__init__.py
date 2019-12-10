import logging

from core.interfaces.serialization import Serializable
from core.messages.keys import Keys
from core.messages.translator.situations import ReflectionRequests
from core.result import Result
from core.result.failure.invalid_class import InvalidClass
from core.validation.helpers import create_class_dynamically

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class BaseJobProcessStatusesRequest(object):
    dct = {
        Keys.ACCEPT_JOB_REQUEST: ReflectionRequests.ACCEPT_JOB_REQUEST,
        Keys.DENY_JOB_REQUEST: ReflectionRequests.DENY_JOB_REQUEST,
        Keys.START_JOB_REQUEST: ReflectionRequests.START_JOB_REQUEST,
        Keys.FINISH_JOB_REQUEST: ReflectionRequests.FINISH_JOB_REQUEST,
        Keys.CANCEL_JOB_BY_BUSINESS_OWNER_REQUEST: ReflectionRequests.CANCEL_JOB_BY_BO_REQUEST,
    }

    @staticmethod
    def pre_deserialize(json_dict):
        missed_params = []
        if Keys.USER_TYPE not in json_dict:
            missed_params.append(Result.language.MISSING_REQUEST_TYPE_JSON)
        if len(missed_params) > 0:
            return False, missed_params

        return True,

    @staticmethod
    def deserialize(json_obj):
        if not type(json_obj) is dict:
            json_dict = Serializable.convert_input_to_dict(json_obj)
        else:
            json_dict = json_obj
        result = BaseJobProcessStatusesRequest.pre_deserialize(json_dict)
        if not result[0]:
            return result
        result = BaseJobProcessStatusesRequest.generate_appropriate_request(json_dict[Keys.USER_TYPE])
        if not result[0]:
            res = False, result[1].params
            return res

        return BaseJobProcessStatusesRequest.child_class_deserialize(result[1], json_dict)

    @staticmethod
    def generate_appropriate_request(class_type):
        if class_type not in BaseJobProcessStatusesRequest.dct.keys():
            return False, InvalidClass(status=400, message=Result.language.NO_CLASS_PATH,
                                       params={Keys.USER_TYPE: class_type})
        type_ = BaseJobProcessStatusesRequest.dct[class_type]
        return create_class_dynamically(logger, type_['module'], type_['class'], class_type)

    @staticmethod
    def child_class_deserialize(klass, json_dict):
        model = klass(json_dict)
        result = model.deserialize()
        if result[0]:
            return result[0], result[1], json_dict[Keys.USER_TYPE]
        return result
