from abc import ABCMeta, abstractmethod
from core.validation.helpers import *
from core.messages.request_json_types import UserJSONTypes


class ValidationCodeBase:
    __metaclass__ = ABCMeta

    @abstractmethod
    def send_message(self, json_details):
        pass


class ValidationCodeSMS(ValidationCodeBase):

    def send_message(self, json_details):
        # json_details.json. It should return tuple(True/False, message)
        pass


def is_request_qualified_keys(user_request):
    result = None
    if hasattr(user_request, 'json'):
        if 'request_type' not in user_request.json:
            return False, "request_type is not defined"
        if user_request.json['request_type'] == UserJSONTypes.register_car_owner_user:
            result = is_contains_car_owner_register_json(user_request)

        elif user_request.json['request_type'] == UserJSONTypes.validation_type:
            result = is_contains_validation_code_json(user_request)

        else:
            return False, "request_type is not valid"

    else:
        return False, "request type is not json"

    if result is None:
        return False, "Bad request"
    return result


# def check_emptiness_keys_in_json(user_request):
#     for key, val in user_request.json.items():
#         if len(val) == 0:
#             return False, key + " is empty"
#
#     return True,


def extract_user_info(user_request):
    user = dict()
    user['request_type'] = user_request.json['request_type']
    user['phone_number'] = user_request.json['phone_number']
    user['name'] = user_request.json['name']
    user['password'] = user_request.json['password']
    user['user_type'] = user_request.json['user_type']

    return user
