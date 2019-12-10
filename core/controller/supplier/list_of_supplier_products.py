from core.controller import BaseController
from core.messages.translator.messages_keys import MessagesKeys
from core.result import Result
from core.result.failure.not_found_product import NotFoundProduct
from core.result.failure.not_found_user import UserNotFound
from core.result.success.success_list_of_products import ListOfSupplierProducts
from persistence.database.entity.product import Product
from persistence.database.entity.user.supplier import Supplier


class ListOfProductsController(BaseController):
    def __init__(self, req_info, converter):
        self.converter = converter
        self.req_info = req_info
        self.phone_number = req_info.phone_number
        self.supplier_id = req_info.supplier_id

    def execute(self):
        error_free, result_supplier_existence = self._is_supplier_exist()
        if not error_free:
            dct = result_supplier_existence.dictionary_creator()
            return self.serialize(dct, converter=self.converter)
        result = self._find_own_products()
        dct = result[1].dictionary_creator()
        return self.serialize(dct, self.converter)

    def _is_supplier_exist(self):
        error_free, result = Supplier.find(phone_number=self.phone_number)
        if not error_free:
            return False, result
        if result is None:
            return False, UserNotFound(status=404, message=MessagesKeys.ID_IS_NOT_IN_DB, params=None)
        return True, result

    def _find_own_products(self):
        result = Product.find_all_product_one_supplier_add(self.supplier_id)
        if len(result) == 0:
            return False, NotFoundProduct(status=404, message=MessagesKeys.NOT_FOUND_PRODUCT, params=None)

        return True, ListOfSupplierProducts(status=200, message=MessagesKeys.FOUND_LIST, params=result)
