from flask import Blueprint
from flask import request

from core.controller.supplier.daily_purchase_list import SupplierDailyPurchaseListController
# from core.controller.supplier.supplier_add_product import SupplierNewProductController
from core.controller.supplier.order_process_statuses import BaseOrderProcessStatusesController
from core.controller.supplier.search_on_product import SearchOnProductController
from core.controller.supplier.supplier_delete_product_info import SupplierDeleteProductInfoController
from core.controller.supplier.supplier_manage_product_info import SupplierManageProductInfoController
from core.controller.supplier.list_of_supplier_products import ListOfProductsController
from core.interfaces.Convertible import JSONConverter
from core.messages.keys import Keys
# from core.request.supplier_add_product_request import SupplierNewProductRequest
from core.request.choose_order_item_by_supplier import BaseOrderProcessStatusesRequest
from core.request.supplier_daily_purchase_list import SupplierDailyPurchaseListRequest
# from core.request.update_product_info_request import SupplierUpdateProductRequest
from core.request.search_on_product_request import SearchOnProductsRequest
from core.request.supplier_delete_product_request import SupplierDeleteProductRequest
from core.request.supplier_manage_product_info_request import SupplierManageProductInfoRequest
from core.request.list_of_product_request import ListOfProductRequest
from core.validation.helpers import is_http_request_valid, unrecognized_request, bad_schema_response
from routers.endpoints import Endpoints
from routers.util import login_required

suppliers = Blueprint('supplier', __name__)


@suppliers.route(Endpoints.ADD_NEW_PRODUCT, methods=[Keys.METHOD_POST])
@login_required
def add_new_product():
    if not is_http_request_valid(request):
        return unrecognized_request()

    new_product = SupplierManageProductInfoRequest(request.json)
    result_deserialize = new_product.deserialize()

    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])

    converter = JSONConverter()
    new_product_controller = SupplierManageProductInfoController(result_deserialize[1], converter)
    result = new_product_controller.execute()
    return result


@suppliers.route(Endpoints.EDIT_PRODUCT_INFO + Endpoints.VARIABLE_PRODUCTS, methods=[Keys.METHOD_PUT])
@login_required
def edit_product_info(product_id):
    if not is_http_request_valid(request):
        return unrecognized_request()

    new_product = SupplierManageProductInfoRequest(request.json)
    result_deserialize = new_product.deserialize()

    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])

    converter = JSONConverter()
    new_product_controller = SupplierManageProductInfoController(result_deserialize[1], converter)
    result = new_product_controller.execute()
    return result


@suppliers.route(Endpoints.DELETE_PRODUCT_INFO + Endpoints.VARIABLE_PRODUCTS, methods=[Keys.METHOD_DELETE])
@login_required
def delete_product_info(product_id):
    if not is_http_request_valid(request):
        return unrecognized_request()

    new_product = SupplierDeleteProductRequest(request.json)
    result_deserialize = new_product.deserialize()

    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])

    converter = JSONConverter()
    new_product_controller = SupplierDeleteProductInfoController(result_deserialize[1], converter)
    result = new_product_controller.execute()
    return result


@suppliers.route(Endpoints.GET_PRODUCT_LIST, methods=[Keys.METHOD_GET])
@login_required
def get_list_of_product():
    if not is_http_request_valid(request):
        return unrecognized_request()
    list_of_product = ListOfProductRequest()
    result_deserialize = list_of_product.deserialize()
    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])

    converter = JSONConverter()
    list_of_product_controller = ListOfProductsController(result_deserialize[1], converter)
    result = list_of_product_controller.execute()
    return result


@suppliers.route(Endpoints.SEARCH_FOR_PRODUCT, methods=[Keys.METHOD_GET])
@login_required
def get_wanted_products():
    if not is_http_request_valid(request):
        return unrecognized_request()
    list_of_wanted_product = SearchOnProductsRequest(request.json)
    result_deserialize = list_of_wanted_product.deserialize()
    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])

    converter = JSONConverter()
    list_of_wanted_product_controller = SearchOnProductController(result_deserialize[1], converter)
    result = list_of_wanted_product_controller.execute()
    return result


@suppliers.route(Endpoints.SUPPLIER_DAILY_PURCHASE_LIST, methods=[Keys.METHOD_GET])
@login_required
def return_daily_purchase_list():
    if not is_http_request_valid(request):
        return unrecognized_request()

    purchase_list = SupplierDailyPurchaseListRequest()
    result_deserialize = purchase_list.deserialize()

    if not result_deserialize[0]:
        return bad_schema_response(result_deserialize[1])

    converter = JSONConverter()
    daily_purchases_controller = SupplierDailyPurchaseListController(result_deserialize[1], converter)
    result = daily_purchases_controller.execute()
    return result


@suppliers.route(Endpoints.SUPPLIER_CHANGE_ORDER_STATUS, methods=[Keys.METHOD_PUT])
@login_required
def change_status_order():
    if not is_http_request_valid(request):
        return unrecognized_request()

    accept_deny_request = BaseOrderProcessStatusesRequest.deserialize(request.json)
    if not accept_deny_request[0]:
        return bad_schema_response(accept_deny_request[1])

    converter = JSONConverter()
    list_controller = BaseOrderProcessStatusesController(accept_deny_request[1], accept_deny_request[2], converter)
    result = list_controller.execute()
    return result


