from flask import Blueprint, session
from flask import jsonify, request, make_response, redirect, url_for

from core.controller.admin_registration import AdminRegistrationController
from core.controller.code_validation.admin import CodeValidationAdminController
from core.interfaces.Convertible import JSONConverter
from core.messages import HttpStatus
from core.messages.keys import Keys
from core.request.admin_registration import AdminRegistrationRequest
from core.request.change_password import ChangePasswordRequest
from core.request.code_validation import CodeValidationRequest
from core.request.forget_password import ForgetPasswordRequest, States
from core.request.helpers import login_helper_request
from core.request.iws_register_request import IWSRegisterRequest
from core.request.login import LoginRequest
from core.request.supplier_registeration_request import SupplierRegistrationRequest
from core.request.user_registration import UserRegistrationRequest
from core.result.failure.bad_input_format import BadInputFormat
from core.validation.helpers import is_http_request_valid, bad_schema_response, is_request_json
from core.validation.helpers import unrecognized_request
from core.validation.session_helper.session_manager import SessionManager
from routers.endpoints import Endpoints
from routers.util import login_required

authentication = Blueprint('authentication', __name__)


@authentication.route('/register_user', methods=["POST"])
def register_user():
    from core.controller.user_registration import UserRegistrationController

    if not is_http_request_valid(request):
        return unrecognized_request()

    user = UserRegistrationRequest(request.json)
    result_deserialize = user.deserialize()
    if not result_deserialize[0]:
        bad_input = BadInputFormat(status=HttpStatus.BAD_REQUEST, message="bad schema", params=result_deserialize[1])
        dct = bad_input.dictionary_creator()
        return make_response(jsonify(dct), dct["status"])

    converter = JSONConverter()
    user_controller = UserRegistrationController(result_deserialize[1], converter)
    ret = user_controller.execute()
    return ret


@authentication.route('/validate_user', methods=["POST"])
def validate_user():
    from core.controller.code_validation import CodeValidationController

    if not is_http_request_valid(request):
        return unrecognized_request()
    code = CodeValidationRequest(request.json)
    result_deserialize = code.deserialize()
    if not result_deserialize[0]:
        bad_input = BadInputFormat(status=HttpStatus.BAD_REQUEST, message="bad schema", params=result_deserialize[1])
        dct = bad_input.dictionary_creator()
        return make_response(jsonify(dct), dct["status"])

    converter = JSONConverter()
    code_validation_controller = CodeValidationController(result_deserialize[1], converter)
    ret = code_validation_controller.execute()
    return ret


# @authentication.route('/login', methods=["POST"])
# def login():
#     from core.controller.login import LoginController
#
#     result = login_helper_request(request)
#     if not result[0]:
#         return result[1]
#
#     converter = JSONConverter()
#     login_controller = LoginController(result[1], converter)
#     ret = login_controller.execute()
#     return ret


@authentication.route('/user/logout', methods=["GET"])
@login_required
def logout():
    SessionManager.pop(Keys.USER_ID)
    dct = {"type": "success", "message": "Logout", "status": HttpStatus.OK}
    return make_response(jsonify(dct), dct["status"])


@authentication.route('/register_admin', methods=["POST"])
def register_admin():
    if not is_http_request_valid(request):
        return unrecognized_request()

    admin = AdminRegistrationRequest(request.json)
    result_deserialize = admin.deserialize()

    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])

    converter = JSONConverter()
    admin_register_controller = AdminRegistrationController(result_deserialize[1], converter)
    result = admin_register_controller.execute()
    return result


@authentication.route('/validate_admin', methods=["POST"])
def validate_admin():
    if not is_http_request_valid(request):
        return unrecognized_request()
    code = CodeValidationRequest.deserialize(request.json)
    if not code[0]:
        return bad_schema_response(code[1])

    converter = JSONConverter()
    code_validation_controller = CodeValidationAdminController(code[1], converter)
    ret = code_validation_controller.execute()
    return ret


@authentication.route(Endpoints.REGISTER_IWS, methods=["POST"])
def register_iws():
    from core.controller.iws_registration import IwsRegistrationController
    if not is_http_request_valid(request):
        return unrecognized_request()

    iws_registration = IWSRegisterRequest(request.json)
    result_deserialize = iws_registration.deserialize()
    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])

    converter = JSONConverter()
    register_controller = IwsRegistrationController(result_deserialize[1], converter)
    result = register_controller.execute()
    return result


@authentication.route(Endpoints.LOGIN_IWS, methods=["POST"])
def login_iws():
    from core.controller.login_iws import IwsLoginController

    # result = login_helper_request(request)
    # if not result[0]:
    #     return result[1]
    if not is_http_request_valid(request):
        return unrecognized_request()
    result = LoginRequest(request.json)
    result_deserialize = result.deserialize()
    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])

    converter = JSONConverter()
    login_controller = IwsLoginController(result_deserialize[1], converter)
    ret = login_controller.execute()
    return ret


@authentication.route('/validate_iws', methods=["POST"])
def validate_iws():
    from core.controller.iws_code_validation import CodeValidationController

    if not is_http_request_valid(request):
        return unrecognized_request()
    code = CodeValidationRequest.deserialize(request.json)
    if not code[0]:
        return bad_schema_response(code[1])

    converter = JSONConverter()
    code_validation_controller = CodeValidationController(code[1], converter)
    ret = code_validation_controller.execute()
    return ret


@authentication.route(Endpoints.FORGET_PASSWORD, methods=["POST"])
def forget_pass():
    from core.controller.forget_password.forget_password import ForgetPasswordController

    if not is_http_request_valid(request):
        return unrecognized_request()
    if Keys.FORGET_PASS not in session.keys():
        session[Keys.FORGET_PASS] = {}
    if Keys.STATE_ID not in session[Keys.FORGET_PASS].keys():

        session[Keys.FORGET_PASS][Keys.STATE_ID] = States.PHONE_NUMBER
        state_id = States.PHONE_NUMBER
    else:
        state_id = session[Keys.FORGET_PASS][Keys.STATE_ID]

    code = ForgetPasswordRequest(request.json, state_id)
    result = code.deserialize()
    if not result[0]:
        return bad_schema_response(result[1])

    converter = JSONConverter()
    forget_password_controller = ForgetPasswordController(result[1], converter)
    ret = forget_password_controller.execute()
    return ret


@authentication.route(Endpoints.CHANGE_PASSWORD, methods=["POST"])
@login_required
def change_pass():
    from core.controller.change_password.change_password import ChangePasswordController
    if not is_http_request_valid(request):
        return unrecognized_request()
    code = ChangePasswordRequest(request.json)
    result = code.deserialize()
    if not result[0]:
        print result[1]
        return bad_schema_response(result[1])
    phone_number = session[Keys.PHONE_NUMBER]
    # phone_number = request.json[Keys.PHONE_NUMBER]
    converter = JSONConverter()
    change_password_controller = ChangePasswordController(result[1], phone_number, converter)
    ret = change_password_controller.execute()
    return ret


@authentication.route(Endpoints.REGISTER_SUPPLIER, methods=["POST"])
def register_supplier_user():
    from core.controller.supplier_registration import SupplierRegistrationController

    if not is_http_request_valid(request):
        return unrecognized_request()

    supplier = SupplierRegistrationRequest(request.json)
    result_deserialize = supplier.deserialize()
    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])

    converter = JSONConverter()
    user_controller = SupplierRegistrationController(result_deserialize[1], converter)
    ret = user_controller.execute()
    return ret


@authentication.route(Endpoints.LOGIN, methods=["POST"])
def login():
    from core.controller.login import LoginController

    if not is_http_request_valid(request):
        return unrecognized_request()
    result = LoginRequest(request.json)
    result_deserialize = result.deserialize()
    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])

    converter = JSONConverter()
    login_controller = LoginController(result_deserialize[1], converter)
    ret = login_controller.execute()
    return ret
