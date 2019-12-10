from flask import Blueprint
from flask import request

from core.controller.business_owner.business_owner_update_location import BusinessOwnerUpdateLocationController
from core.controller.business_owner.change_business_owner_activation import ActivationStateController
from core.controller.business_owner.job_process_statuses import BaseJobProcessStatusesController
from core.controller.business_owner.list_business_owner_jobs_queue import JobsQueueListController
from core.controller.business_owner.list_jobs_by_status import ListJobsByStatusController
from core.controller.calendar.delete_job_from_calendar import CalenderDeletionController
from core.controller.calendar.insert_job_in_calendar import CalenderInsertionController
from core.interfaces.Convertible import JSONConverter
from core.messages.keys import Keys
from core.request.business_owner.business_owner_update_location import BusinessOwnerUpdateLocationRequest
from core.request.business_owner.list_jobs_by_status import ListJobsByStatusRequest
from core.request.calendar_deletion_request import CalendarDeletionRequest
from core.request.calendar_insertin_request import CalendarInsertionRequest
from core.request.change_business_owner_activation import ActivationStateRequest
from core.request.choose_job_by_bo import BaseJobProcessStatusesRequest
from core.request.list_business_owner_jobs_queue import JobsQueueListRequest
from core.validation.helpers import is_http_request_valid, bad_schema_response
from core.validation.helpers import unrecognized_request
from routers.endpoints import Endpoints
from routers.util import login_required

business_owner = Blueprint('business_owner', __name__)


@business_owner.route(Endpoints.BUSINESS_OWNER_JOB_REQUEST, methods=["PUT"])
@login_required
def accept_deny():
    if not is_http_request_valid(request):
        return unrecognized_request()

    accept_deny_request = BaseJobProcessStatusesRequest.deserialize(request.json)

    if not accept_deny_request[0]:
        return bad_schema_response(accept_deny_request[1])

    converter = JSONConverter()
    accept_deny_controller = BaseJobProcessStatusesController(accept_deny_request[1], accept_deny_request[2], converter)
    result = accept_deny_controller.execute()
    return result


@business_owner.route(Endpoints.BUSINESS_OWNER_JOBS + Endpoints.VARIABLE_BUSINESS_OWNER, methods=[Keys.METHOD_GET])
@login_required
def get_jobs(business_owner_id):
    if not is_http_request_valid(request):
        return unrecognized_request()
    business_owner = JobsQueueListRequest(business_owner_id)
    result_deserialize = business_owner.deserialize()
    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])

    converter = JSONConverter()
    list_controller = JobsQueueListController(result_deserialize[1], converter)
    result = list_controller.execute()
    return result


@business_owner.route(Endpoints.BUSINESS_OWNER_JOB, methods=[Keys.METHOD_PUT])
@login_required
def change_status_job():
    if not is_http_request_valid(request):
        return unrecognized_request()

    accept_deny_request = BaseJobProcessStatusesRequest.deserialize(request.json)
    if not accept_deny_request[0]:
        return bad_schema_response(accept_deny_request[1])

    converter = JSONConverter()
    list_controller = BaseJobProcessStatusesController(accept_deny_request[1], accept_deny_request[2], converter)
    result = list_controller.execute()
    return result


@business_owner.route(Endpoints.ACTIVATE_BUSINESS_OWNER, methods=[Keys.METHOD_PUT])
@login_required
def change_status_activation():
    if not is_http_request_valid(request):
        return unrecognized_request()

    activation_status_request = ActivationStateRequest(request.json)
    result_deserialize = activation_status_request.deserialize()
    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])

    converter = JSONConverter()
    activation_status_controller = ActivationStateController(result_deserialize[1], converter)
    result = activation_status_controller.execute()
    return result


@business_owner.route(Endpoints.INSERT_IN_CALENDAR, methods=[Keys.METHOD_POST])
@login_required
def insert_job_calender():
    if not is_http_request_valid(request):
        return unrecognized_request()
    job_calendar_insertion_request = CalendarInsertionRequest(request.json)
    result_deserialize = job_calendar_insertion_request.deserialize()

    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])

    converter = JSONConverter()
    insert_calender_controller = CalenderInsertionController(result_deserialize[1], converter)
    result = insert_calender_controller.execute()
    return result


@business_owner.route(Endpoints.DELETE_FROM_CALENDAR, methods=[Keys.METHOD_PUT])
@login_required
def delete_job_calender():
    if not is_http_request_valid(request):
        return unrecognized_request()
    job_calendar_deletion = CalendarDeletionRequest(request.json)
    result_deserialize = job_calendar_deletion.deserialize()

    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])

    converter = JSONConverter()
    delete_calender_controller = CalenderDeletionController(result_deserialize[1], converter)
    result = delete_calender_controller.execute()
    return result


@business_owner.route(Endpoints.BUSINESS_OWNER_UPDATE_LOCATION, methods=[Keys.METHOD_PUT])
@login_required
def update_business_owner_location():
    if not is_http_request_valid(request):
        return unrecognized_request()

    update_location_request = BusinessOwnerUpdateLocationRequest(request.json)
    result_deserialize = update_location_request.deserialize()
    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])

    converter = JSONConverter()
    update_location_controller = BusinessOwnerUpdateLocationController(result_deserialize[1].business_owner, converter)
    result = update_location_controller.execute()
    return result


@business_owner.route(Endpoints.LIST_JOBS_FOR_BUSINESS_OWNER, methods=[Keys.METHOD_POST])
@login_required
def list_business_owner_jobs_by_status():
    if not is_http_request_valid(request):
        return unrecognized_request()

    job_list_request = ListJobsByStatusRequest(request.json)
    result_deserialize = job_list_request.deserialize()
    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])

    converter = JSONConverter()
    job_list_controller = ListJobsByStatusController(result_deserialize[1].business_owner,
                                                     result_deserialize[1].status, converter)
    result = job_list_controller.execute()
    return result
