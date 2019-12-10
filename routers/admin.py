from flask import request, Blueprint, send_file
from os.path import dirname, realpath

from core.controller.auto_type.list_auto_types import ListAutoTypesController
from core.controller.forget_password.forget_password import ForgetPasswordController
from core.controller.system_admin.show_rest_of_allowed_credit import BusinessOwnerRestCreditController
from core.controller.trace_unfinished_task.list_unfinished_job import ListUnfinishedJob
from core.controller.version_checker import VersionCheckerController
from core.interfaces.Convertible import JSONConverter
from core.messages.keys import Keys
from core.request.forget_password import ForgetPasswordRequest
from core.request.show_rest_of_allowed_credit_request import BusinessOwnerRestCreditRequest
from core.validation.helpers import is_http_request_valid, bad_schema_response
from core.validation.helpers import unrecognized_request
from routers.endpoints import Endpoints
from routers.util import login_required
import io

admin = Blueprint('admin', __name__)


@admin.route(Endpoints.LIST_AUTO_TYPE, methods=[Keys.METHOD_GET])
@login_required
def get_auto_types():
    if not is_http_request_valid(request):
        return unrecognized_request()
    converter = JSONConverter()
    list_controller = ListAutoTypesController(converter)
    result = list_controller.execute()
    return result


@admin.route(Endpoints.FORGET_PASSWORD, methods=[Keys.METHOD_POST])
def forget_password():
    # if not is_http_request_valid(request):
    #     return unrecognized_request()
    code = ForgetPasswordRequest.deserialize(request.json)
    if not code[0]:
        return bad_schema_response(code[1])

    converter = JSONConverter()
    forget_password_controller = ForgetPasswordController(code[1], converter)
    ret = forget_password_controller.execute()
    return ret


@admin.route(Endpoints.LIST_UNFINISHED_JOB, methods=[Keys.METHOD_GET])
@login_required
def get_iws_status():
    if not is_http_request_valid(request):
        return unrecognized_request()

    converter = JSONConverter()
    unfinished_job_list = ListUnfinishedJob(converter)
    result = unfinished_job_list.execute()
    return result


@admin.route(Endpoints.FORCE_UPDATE + '/<app_name>/<version>', methods=[Keys.METHOD_GET])
def force_update(app_name, version):
    converter = JSONConverter()
    need_update = VersionCheckerController(app_name, version, converter)
    result = need_update.execute()
    return result


@admin.route('/<uuid>/<type>', methods=[Keys.METHOD_GET])
def load_image(uuid, type):
    imageDictionary = {
        '4a58fc5e-a9e9-11e8-9eb4-34f39aa7f24b': 'core/img/4a58fc5e/4a58fc5e-a9e9-11e8-9eb4-34f39aa7f24b.JPG',
        '7753e0e1-a9e9-11e8-8add-34f39aa7f24b': 'core/img/7753e0e/7753e0e1-a9e9-11e8-8add-34f39aa7f24b.JPG',
        '75106e9e-a9eb-11e8-a66e-34f39aa7f24b': 'core/img/75106e9e/75106e9e-a9eb-11e8-a66e-34f39aa7f24b.JPG',
    }

    filename = dirname(realpath(__file__)) + '/../' + imageDictionary[uuid]
    with open(filename, 'rb') as bites:
        return send_file(
            io.BytesIO(bites.read()),
            attachment_filename='profile-pic.jpeg',
            mimetype='image/jpg'
        )


@admin.route(Endpoints.GET_BUSINESS_OWNER_REST_OF_ALLOWED_CREDIT,
             methods=[Keys.METHOD_GET])
def get_business_owner_rest_of_credit():
    if not is_http_request_valid(request):
        return unrecognized_request()
    list_of_product = BusinessOwnerRestCreditRequest()
    result_deserialize = list_of_product.deserialize()
    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])

    converter = JSONConverter()
    list_of_product_controller = BusinessOwnerRestCreditController(result_deserialize[1], converter)
    result = list_of_product_controller.execute()
    return result
