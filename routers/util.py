from functools import wraps

from flask import make_response, jsonify

from core.messages import HttpStatus
from core.messages.keys import Keys
from core.validation.session_helper.session_manager import SessionManager


def login_required(controller):
    @wraps(controller)
    def login_required_wrapper(*args, **kwds):
        if not SessionManager.is_key_exist(Keys.USER_ID) or SessionManager.retrieve_session_value_by_key(
                Keys.USER_ID) is None:
            dct = {"type": "failure", "message": "you should login first", "status": HttpStatus.BAD_REQUEST}

            return make_response(jsonify(dct), dct["status"])
        return controller(*args, **kwds)

    return login_required_wrapper
