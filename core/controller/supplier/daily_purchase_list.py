from core.controller import BaseController
from core.messages import HttpStatus
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result import Result
from core.result.failure.not_found_order_items import NotFoundOrderItem
from core.result.failure.not_found_user import UserNotFound
from persistence.database.entity.brand import Brand
from persistence.database.entity.order_items import OrderItem
from persistence.database.entity.sub_category import SubCategory
from persistence.database.entity.user.supplier import Supplier


class SupplierDailyPurchaseListController(BaseController):
    def __init__(self, json, converter):
        self.phone_number = json.phone_number
        self.converter = converter
        self.supplier_id = json.user_id

    def execute(self):
        error_free, supplier = self._find_requesting_supplier()
        if not error_free:
            dct = supplier.dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        if not len(supplier) == 0:
            error_free, purchase_list = self._get_daily_purchase_list()
            if not error_free:
                dct = purchase_list.dictionary_creator()
                return self.serialize(dct, converter=self.converter)
            if not len(purchase_list) == 0:
                purchase_list = self._dictionary_creator(purchase_list)
                return self.serialize(purchase_list, converter=self.converter)
            not_found = NotFoundOrderItem(status=HttpStatus.NOT_FOUND, message=MessagesKeys.NOT_FOUND_ORDER_ITEM,
                                          params=None)
            dct = not_found.dictionary_creator()
            return self.serialize(dct, converter=self.converter)

    def _find_requesting_supplier(self):
        error_free, result = Supplier.find(phone_number=self.phone_number)
        if not error_free:
            return False, result
        if len(result) == 0 or result is None:
            return False, UserNotFound(status=HttpStatus.NOT_FOUND, message=MessagesKeys.ID_IS_NOT_IN_DB, params=None)
        return True, result

    def _get_daily_purchase_list(self):
        return OrderItem.get_daily_purchase_list_of_supplier(self.supplier_id)

    def _dictionary_creator(self, myList):
        purchase = []
        for list_item in myList:
            dic = {
                Keys.PRODUCT_ID: list_item.product_id,
                Keys.NUMBER: list_item.requested_number,
                Keys.PRICE: str(list_item.product.price),
                Keys.BUSINESS_OWNER_ID: list_item.business_owner_id,
                Keys.ORDER_ID: list_item.order_id,
                Keys.CODE: list_item.product.code
            }

            error_free, result = Brand.find(id=list_item.product.brand_id)
            if not error_free:
                return False, result
            if not len(result) == 0:
                dic[Keys.COMPANY] = result[0].name

            error_free, result = SubCategory.load_by_id(id=list_item.product.sub_category_id)
            if not error_free:
                return False, result
            if not len(result) == 0:
                dic[Keys.NAME] = result[0].name

            purchase.append(dic)

        return {Keys.STATUS: HttpStatus.OK, Keys.MESSAGE: Result.language.SUCCESS_LIST, Keys.PARAMS: purchase}
