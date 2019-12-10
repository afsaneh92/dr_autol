from core.controller import BaseController
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result.failure.list_is_empty import EmptyList

from core.result.success.list_of_produvt_search_list import SuccessProductSearchList
from core.result.success.success_product_search_list_details import SuccessProductSearchListDetails
from persistence.database.entity.user.supplier import Supplier


class SearchOnProductController(BaseController):
    def __init__(self, product_search_parameter, converter):
        self.product_search_parameter = product_search_parameter
        self.converter = converter

    def execute(self):
        result_all = self._find_all_product_info()
        dct = result_all[1].dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    def _select_an_order_item_from_a_product(self, list_of_product):
        order = []
        for product in list_of_product:
            for order_item in product.order_items:
                if self.product_search_parameter.supplier_status_id is not None:
                    if order_item.supplier_status_id == self.product_search_parameter.supplier_status_id:
                        order.append(order_item)
                if self.product_search_parameter.accepted_number is not None:
                    if order_item.accepted_number == self.product_search_parameter.accepted_number:
                        order.append(order_item)
                if self.product_search_parameter.requested_number is not None:
                    if order_item.requested_number == self.product_search_parameter.requested_number:
                        order.append(order_item)
        if len(order) > 0:
            orders = set()
            for item in order:
                orders.add(item)
            return True, SuccessProductSearchList(status=200, message=MessagesKeys.FOUND_LIST, params=orders)

        return False, EmptyList(status=404, message=MessagesKeys.FAIL_LIST, params=None)

    def _find_all_product_info(self):
        product_info = Supplier.search_on_products(self.product_search_parameter)
        if not product_info[0]:
            return product_info

        if len(product_info[1]) == 0:
            return False, EmptyList(status=404, message=MessagesKeys.FAIL_LIST, params=None)
        list_result = product_info[1]
        if self.product_search_parameter.supplier_status_id is not None:
            return self._select_an_order_item_from_a_product(list_result)
        if self.product_search_parameter.accepted_number is not None:
            return self._select_an_order_item_from_a_product(list_result)
        if self.product_search_parameter.requested_number is not None:
            return self._select_an_order_item_from_a_product(list_result)

        return True, SuccessProductSearchListDetails(status=200, message=MessagesKeys.FOUND_LIST,
                                                     params=list_result)
