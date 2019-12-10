from flask import Blueprint
from flask import request, redirect, url_for

from core.controller.car.auto_type_consumable_items import ListAutoTypeConsumableItemsController
from core.controller.services.add_service_grade import AddServiceGradesController
from core.controller.services.list_service_grades import ListServiceGradesController
from core.controller.services.list_service_types import ListServiceTypesController
from core.controller.services.register_service_type import ServiceTypeRegistrationController
from core.interfaces.Convertible import JSONConverter
from core.messages.keys import Keys
from core.request.add_service_grade import NewServiceGradeRequest
from core.request.add_service_type import NewServiceTypeRequest
from core.request.auto_type_consumable_items_request import ListAutoTypeConsumableItemsRequest
from core.request.list_service_types import ListServiceTypesRequest
from core.validation.helpers import is_http_request_valid, is_logged_in, bad_schema_response
from core.validation.helpers import unrecognized_request
from routers.endpoints import Endpoints
from routers.util import login_required

choose_service_grade = Blueprint('choose_service_grade', __name__)


@choose_service_grade.route(Endpoints.SERVICES_SERVICE_GRADES, methods=["GET"])
def list_service_grades():
    if not is_logged_in():
        return redirect(url_for('login'))

    if not is_http_request_valid(request):
        return unrecognized_request()

    converter = JSONConverter()
    list_service_grades_controller = ListServiceGradesController(converter)
    result = list_service_grades_controller.execute()
    return result


@choose_service_grade.route(Endpoints.SERVICES_SERVICE_GRADES, methods=["POST"])
def add_new_service_grades():
    if not is_logged_in():
        return redirect(url_for('login'))

    if not is_http_request_valid(request):
        return unrecognized_request()

    new_service_grade = NewServiceGradeRequest(request.json)
    deserialize_result = new_service_grade.deserialize()

    if not deserialize_result[0]:
        return bad_schema_response(deserialize_result[1])

    converter = JSONConverter()
    new_service_grade_controller = AddServiceGradesController(deserialize_result[1], converter)
    result = new_service_grade_controller.execute()
    return result


@choose_service_grade.route(Endpoints.SERVICES_SERVICE_TYPES, methods=["POST"])
def add_new_service_type():
    if not is_logged_in():
        return redirect(url_for('login'))

    if not is_http_request_valid(request):
        return unrecognized_request()

    new_service_type = NewServiceTypeRequest(request.json)
    deserialize_result = new_service_type.deserialize()

    if not deserialize_result[0]:
        return bad_schema_response(deserialize_result[1])

    converter = JSONConverter()
    new_car_controller = ServiceTypeRegistrationController(deserialize_result[1], converter)
    result = new_car_controller.execute()
    return result


@choose_service_grade.route('/services/service_types/<service_grade_id>', methods=["GET"])
def get_service_types(service_grade_id):
    if not is_logged_in():
        return redirect(url_for('login'))

    if not is_http_request_valid(request):
        return unrecognized_request()

    service_type_request = ListServiceTypesRequest(service_grade_id)
    deserialize_request = service_type_request.deserialize()
    if not deserialize_request[0]:
        return bad_schema_response(deserialize_request[1])

    converter = JSONConverter()
    list_controller = ListServiceTypesController(deserialize_request[1].service_grade_id, converter)
    result = list_controller.execute()
    return result


@choose_service_grade.route(Endpoints.AUTO_TYPE_CONSUMABLE_ITEMS, methods=[Keys.METHOD_GET])
@login_required
def auto_type_consumable_items():
    if not is_http_request_valid(request):
        return unrecognized_request()

    car_consumable_items_request = ListAutoTypeConsumableItemsRequest(request.json)
    result_request_deserialize = car_consumable_items_request.deserialize()
    if not result_request_deserialize[0]:
        return bad_schema_response(result_request_deserialize[1])

    converter = JSONConverter()
    list_auto_type_consumable_items = ListAutoTypeConsumableItemsController(result_request_deserialize[1], converter)
    result = list_auto_type_consumable_items.execute()
    return result
