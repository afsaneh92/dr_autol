from flask import Blueprint
from flask import request

from core.controller.cancellation.cancel_by_car_owner import CancellationByCarOwnerController
from core.controller.car.delete_car import DeleteCarController
from core.controller.car.list_car_problems import CarProblemListController
from core.controller.car.list_cars import ListCarsController
from core.controller.car.list_search_iws import ListSearchIWSController
from core.controller.car.new_car import NewCarController
from core.controller.car.update_car import UpdateCarController
from core.controller.car_owner.job import JobBaseController
from core.controller.car_owner.job.list_payable_job import ListPayableJob
from core.controller.car_owner.payment import BasePaymentOperationController
from core.controller.last_event_rating.send_question_text_to_client import ListFinishedJob
from core.controller.rating.rate_to_jobs import RateJobsController
from core.interfaces.Convertible import JSONConverter
from core.messages.keys import Keys
from core.request.car_owner.job.not_payed_job import NotPayedJobRequest
from core.request.rate_to_job_request import RateJobRequest
from core.request.car_owner.job import JobBaseRequest
from core.request.car_owner.payment import PaymentOperationBaseRequest
# from core.request.car_owner.payment_operation import PaymentOperationRequest
from core.request.cancel_by_car_owner import CancellationByCarOwnerRequest
from core.request.car_owner.job import JobBaseRequest
from core.request.car_owner.payment import PaymentOperationBaseRequest
from core.request.delete_car_request import DeleteCarRequest
from core.request.list_search_iws_request import ListSearchIWSRequest
from core.request.new_car import NewCarRequest
from core.request.rate_to_job_request import RateJobRequest
from core.request.update_car_request import UpdateCarRequest
from core.validation.helpers import is_http_request_valid, bad_schema_response
from core.validation.helpers import unrecognized_request
from routers.endpoints import Endpoints
from routers.util import login_required

car_owner = Blueprint('car_owner', __name__)


@car_owner.route(Endpoints.ADD_NEW_CAR, methods=[Keys.METHOD_POST])
@login_required
def add_new_car():
    if not is_http_request_valid(request):
        return unrecognized_request()

    new_car = NewCarRequest(request.json)
    result_deserialize = new_car.deserialize()

    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])

    converter = JSONConverter()
    new_car_controller = NewCarController(result_deserialize[1], converter)
    result = new_car_controller.execute()
    return result


@car_owner.route('/car_owner/delete_car/<car_id>', methods=["PUT"])
@login_required
def delete_car(car_id):
    if not is_http_request_valid(request):
        return unrecognized_request()

    delete_car = DeleteCarRequest(request.json)
    result_deserialize = delete_car.deserialize()

    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])

    converter = JSONConverter()
    delete_car_controller = DeleteCarController(result_deserialize[1], converter)
    result = delete_car_controller.execute()
    return result


@car_owner.route('/car_owner/cars/<car_id>', methods=["PUT"])
@login_required
def update_car(car_id):
    if not is_http_request_valid(request):
        return unrecognized_request()

    update_car = UpdateCarRequest(request.json)
    result_deserialize = update_car.deserialize()

    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])

    converter = JSONConverter()
    car = result_deserialize[1].car
    update_car_controller = UpdateCarController(car, converter)
    result = update_car_controller.execute()
    return result


@car_owner.route('/car_owner/cars/<user_id>', methods=["GET"])
@login_required
def get_cars(user_id):
    if not is_http_request_valid(request):
        return unrecognized_request()

    converter = JSONConverter()
    list_controller = ListCarsController(user_id, converter)
    result = list_controller.execute()
    return result


@car_owner.route(Endpoints.LIST_IWS_BY_SEARCH, methods=["POST"])
@login_required
def search_iws():
    if not is_http_request_valid(request):
        return unrecognized_request()

    list_iws_request = ListSearchIWSRequest(request.json)
    result_deserialize = list_iws_request.deserialize()

    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])

    converter = JSONConverter()
    list_controller = ListSearchIWSController(result_deserialize[1], converter)
    result = list_controller.execute()
    return result


@car_owner.route(Endpoints.CAR_OWNER_SET_APPOINTMENT, methods=["POST"])
@login_required
def set_appointment():
    if not is_http_request_valid(request):
        return unrecognized_request()

    job_request = JobBaseRequest(request.json)
    result_deserialize = job_request.deserialize()

    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])

    converter = JSONConverter()
    job_controller = JobBaseController(result_deserialize[1], result_deserialize[2], converter)
    result = job_controller.execute()
    return result


@car_owner.route('/car_owner/jobs/<car_owner_id>', methods=["GET"])
@login_required
def list_jobs(car_owner_id):
    if not is_http_request_valid(request):
        return unrecognized_request()

    converter = JSONConverter()
    list_controller = CarProblemListController(car_owner_id, converter)
    result = list_controller.execute()
    return result


@car_owner.route(Endpoints.CANCEL_JOB_BY_CAR_OWNER, methods=["PUT"])
@login_required
def cancel_job():
    if not is_http_request_valid(request):
        return unrecognized_request()

    cancellation_request = CancellationByCarOwnerRequest(request.json)
    result_deserialize = cancellation_request.deserialize()

    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])

    converter = JSONConverter()
    cancel_controller = CancellationByCarOwnerController(result_deserialize[1].job, result_deserialize[1].car_owner,converter)
    result = cancel_controller.execute()
    return result


@car_owner.route(Endpoints.CAR_OWNER_PAYMENTS, methods=[Keys.METHOD_POST])
@login_required
def payment_operation():
    if not is_http_request_valid(request):
        return unrecognized_request()

    payment_operation_request = PaymentOperationBaseRequest(request.json)
    result_deserialize = payment_operation_request.deserialize()
    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])

    converter = JSONConverter()
    payment_operation_controller = BasePaymentOperationController(result_deserialize[1], result_deserialize[2],
                                                                  converter)
    result = payment_operation_controller.execute()
    return result


@car_owner.route(Endpoints.RATE_BUSINESS_OWNER_BY_CAR_OWNER, methods=[Keys.METHOD_PUT])
@login_required
def rate_to_jobs():
    if not is_http_request_valid(request):
        return unrecognized_request()

    rate_to_jobs_request = RateJobRequest(request.json)
    result_deserialize = rate_to_jobs_request.deserialize()
    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])
    converter = JSONConverter()
    rate_to_jobs_controller = RateJobsController(
        result_deserialize[1],
        converter)
    result = rate_to_jobs_controller.execute()
    return result


@car_owner.route(Endpoints.LAST_EVENT, methods=[Keys.METHOD_GET])
@login_required
def last_event():
    if not is_http_request_valid(request):
        return unrecognized_request()

    converter = JSONConverter()
    last_event_controller = ListFinishedJob(converter)
    result = last_event_controller.execute()
    return result


@car_owner.route(Endpoints.PAYABLE_LIST, methods=[Keys.METHOD_GET])
# @login_required
def payable_list():
    if not is_http_request_valid(request):
        return unrecognized_request()

    not_payed_job_request = NotPayedJobRequest(request.json)
    result_deserialize = not_payed_job_request.deserialize()
    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])

    converter = JSONConverter()
    last_event_controller = ListPayableJob(result_deserialize[1].car_owner_id, converter)
    result = last_event_controller.execute()
    return result
