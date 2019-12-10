from app import db
from core.controller import BaseController
from core.messages.translator.messages_keys import MessagesKeys
from core.result.failure.not_found_user import UserNotFound
from core.result.failure.supplier_id_and_phone_number_not_match import SupplierIdPhoneNumberNotMatch
from persistence.database.entity.product import Product
from persistence.database.entity.user.supplier import Supplier


class SupplierDeleteProductInfoController(BaseController):
    def __init__(self, product_info, converter):
        self.product_info = product_info
        self.converter = converter
        self.phone_number = self.product_info.phone_number
        self.supplier_id = self.product_info.supplier_id
        self.product_id = self.product_info.product_id

    def execute(self):
        error_free, result_product_exist = self._is_product_exist()
        if not error_free:
            dct = result_product_exist.dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        error_free, result_supplier_delete_own_product = self._is_supplier_delete_own_product()
        if not error_free:
            dct = result_supplier_delete_own_product.dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        result = self._delete_product()
        dct = result[1].dictionary_creator()
        return self.serialize(dct, self.converter)

    def _is_supplier_delete_own_product(self):
        error_free, result = Supplier.check_id_and_phone_number_match(self.product_id, self.phone_number)
        if not error_free:
            return False, result
        if result is None:
            return False, SupplierIdPhoneNumberNotMatch(status=404, message=MessagesKeys.ID_AND_PHONE_NUMBER_NOT_MATCH,
                                                        params=None)
        return True, self.product_id

    def _is_product_exist(self):
        error_free, result = Product.find(id=self.product_id)
        if not error_free:
            return False, result
        if len(result) == 0 or result is None:
            return False, SupplierIdPhoneNumberNotMatch(status=404, message=MessagesKeys.NOT_FOUND_PRODUCT,
                                                        params=None)
        return True, self.product_id

    def _delete_product(self):
        return Product.delete_by_id(db, self.product_id)
