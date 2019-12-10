from flask import make_response, jsonify

from core.messages import HttpStatus
from core.request.login import LoginRequest
from core.result.failure.bad_input_format import BadInputFormat
from core.validation.helpers import is_http_request_valid, unrecognized_request


def login_helper_request(request):
    if not is_http_request_valid(request):
        return False, unrecognized_request()
    login = LoginRequest(request.json)
    result_deserialize = login.deserialize()
    if not result_deserialize[0]:
        bad_input = BadInputFormat(status=HttpStatus.BAD_REQUEST, message="bad schema", params=result_deserialize[1])
        dct = bad_input.dictionary_creator()
        return False, make_response(jsonify(dct), dct["status"])
    return True, result_deserialize[1]
