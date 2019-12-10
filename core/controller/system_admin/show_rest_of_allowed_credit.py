from core.controller import BaseController
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result.failure.list_is_empty import EmptyList
from core.result.failure.more_than_allowed_credit import MoreThanAllowed
from core.result.success.allow_credit import AllowCredit
from core.result.success.list_of_allowed_and_rest_credit import ListOfAllowedAndUsedCredit
from core.result.success.used_credit import UsedCredit
from core.validation.helpers import read_data_from_excel_file, special_time
from persistence.database.entity.user.auto_service import AutoServiceBusinessOwner


class BusinessOwnerRestCreditController(BaseController):
    def __init__(self, req_info, converter):
        self.converter = converter
        self.req_info = req_info
        self.phone_number = req_info.phone_number
        self.business_owner_id = req_info.business_owner_id

    def execute(self):
        error_free, allow_credit_result = self.read_and_find_allowed_credit_from_excel()
        if not error_free:
            dct = allow_credit_result.dictionary_creator()
            return self.serialize(dct, converter=self.converter)
        error_free, result_order_list = self.find_order_item()
        if not error_free:
            dct = result_order_list.dictionary_creator()
            return self.serialize(dct, converter=self.converter)
        error_free, result_used_credit = self.how_much_business_owner_buy_in_special_time()
        if not error_free:
            dct = result_used_credit.dictionary_creator()
            return self.serialize(dct, converter=self.converter)
        result = self.check_rest_of_allowed_credit(allow_credit_result.params[0], result_used_credit.params)
        dct = result[1].dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    def check_rest_of_allowed_credit(self, allowed_credit, used_credit):
        rest_of_allowed_credit = allowed_credit - used_credit
        if rest_of_allowed_credit <= 0:
            return False, MoreThanAllowed(status=404, message=MessagesKeys.MORE_THAN_ALLOWED_CREDIT, params=None)
        dct = {Keys.ALLOWED_CREDIT: allowed_credit, Keys.USED_CREDIT: used_credit,
               Keys.BUSINESS_OWNER_ID: self.business_owner_id, Keys.REST_OF_ALLOW_CREDIT: rest_of_allowed_credit}

        return True, ListOfAllowedAndUsedCredit(status=200, message=MessagesKeys.LIST_OF_USED_AND_REST_CREDIT,
                                                params=dct)

    def read_and_find_allowed_credit_from_excel(self):
        sheet = read_data_from_excel_file(Keys.EXCEL_PASS)[1]
        error_free, allowed_credit = AutoServiceBusinessOwner.read_allow_credit_from_excel(sheet, self.phone_number)
        if not error_free:
            return False, allowed_credit

        return True, AllowCredit(status=200, message=MessagesKeys.ALLOW_CREDIT, params=allowed_credit)

    def find_order_item(self):
        from_to = special_time()
        error_free, orders_in_special_time = AutoServiceBusinessOwner.order_items_modified_and_done_in_special_time(
            self.business_owner_id, from_to[0], from_to[1])
        if not error_free:
            return False, orders_in_special_time
        if orders_in_special_time == []:
            return False, EmptyList(status=404, message=MessagesKeys.FAIL_LIST, params=None)
        if orders_in_special_time is None:
            return False, EmptyList(status=404, message=MessagesKeys.FAIL_LIST, params=None)

        return True, orders_in_special_time

    def how_much_business_owner_buy_in_special_time(self):
        used_credit = 0
        order_list = self.find_order_item()[1]
        if order_list == []:
            return False, EmptyList(status=404, message=MessagesKeys.FAIL_LIST, params=None)
        for order in order_list:
            used_credit = used_credit + float(order.accepted_number * order.product.price)
        return True, UsedCredit(status=200, message=MessagesKeys.USED_CREDIT, params=used_credit)
