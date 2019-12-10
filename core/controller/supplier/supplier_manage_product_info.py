from app import db
from core.controller import BaseController
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result.failure.company_brand_are_not_match import CompanyBrandNotMatch
from core.result.failure.company_not_exist import CompanyNotFound
from core.result.failure.not_found_brand import BrandNotFound
from core.result.failure.not_found_user import UserNotFound
from core.result.failure.product_added_before import ProductAddedBefore
from core.result.failure.supplier_id_and_phone_number_not_match import SupplierIdPhoneNumberNotMatch
from persistence.database.entity.brand import Brand
from persistence.database.entity.comany.comapny import Company
from persistence.database.entity.company_to_brand import CompanyToBrand
from persistence.database.entity.product import Product
from persistence.database.entity.user.supplier import Supplier


class SupplierManageProductInfoController(BaseController):
    def __init__(self, product_info, converter):
        self.product_info = product_info
        self.phone_number = product_info.phone_number
        self.converter = converter
        self.sub_category_id = product_info.json_obj[Keys.SUB_CATEGORY_ID]
        self.company_id = product_info.json_obj[Keys.COMPANY_ID]
        self.brand_id = product_info.json_obj[Keys.BRAND_ID]
        self.code = product_info.json_obj[Keys.CODE]
        self.product = product_info.product
        self.price = product_info.json_obj[Keys.PRICE]
        self.supplier_id = product_info.supplier_id

    def execute(self):
        error_free, supplier_existence_result = self._is_supplier_exist()
        if not error_free:
            dct = supplier_existence_result.dictionary_creator()
            return self.serialize(dct, converter=self.converter)
        error_free, company_existence_result = self._is_company_exist()
        if not error_free:
            dct = company_existence_result.dictionary_creator()
            return self.serialize(dct, converter=self.converter)
        error_free, brand_existence_result = self._is_brand_exist()
        if not error_free:
            dct = brand_existence_result.dictionary_creator()
            return self.serialize(dct, converter=self.converter)
        error_free, brand_and_company_match_result = self._is_brand_and_company_match()
        if not error_free:
            dct = brand_and_company_match_result.dictionary_creator()
            return self.serialize(dct, converter=self.converter)
        result_is_product_has_id = self._is_product_has_id()
        if not result_is_product_has_id[0]:
            error_free, result_supplier_id_and_phone_number_match = self._is_supplier_update_own_product()
            if not error_free:
                dct = result_supplier_id_and_phone_number_match.dictionary_creator()
                return self.serialize(dct, converter=self.converter)
            result_update_product_info = self._update_product_info()
            dct = result_update_product_info[1].dictionary_creator()
            return self.serialize(dct, self.converter)
        else:
            error_free, result_product_added_before = self._is_supplier_and_product_code_unique()
            if not error_free:
                dct = result_product_added_before.dictionary_creator()
                return self.serialize(dct, converter=self.converter)
            result = self._add_new_product()
            dct = result[1].dictionary_creator()
            return self.serialize(dct, self.converter)

    def _is_company_exist(self):
        error_free, result = Company.find(id=self.company_id)
        if not error_free:
            return False, result
        if len(result) == 0:
            return False, CompanyNotFound(status=404, message=MessagesKeys.ID_IS_NOT_IN_DB, params=None)
        self.job_id = result[0].id
        return True, result[0]

    def _is_brand_exist(self):
        error_free, result = Brand.find(id=self.brand_id)
        if not error_free:
            return False, result
        if len(result) == 0:
            return False, BrandNotFound(status=404, message=MessagesKeys.ID_IS_NOT_IN_DB, params=None)
        self.job_id = result[0].id
        return True, result[0]

    def _is_supplier_exist(self):
        error_free, result = Supplier.find(phone_number=self.phone_number)
        if not error_free:
            return False, result
        if len(result) == 0 or result is None:
            return False, UserNotFound(status=404, message=MessagesKeys.ID_IS_NOT_IN_DB, params=None)
        return True, result

    def _is_supplier_and_product_code_unique(self):
        supplier_products_info = Product.find_all_product_one_supplier_add(self.supplier_id)
        codes = []
        for item in supplier_products_info:
            codes.append(item.code)
        if self.code in codes:
            return False, ProductAddedBefore(status=404, message=MessagesKeys.PRODUCT_ADDED_BEFORE, params=None)
        return True, self.supplier_id

    def _is_brand_and_company_match(self):
        error_free, result = CompanyToBrand.is_brand_and_company_match(self.company_id, self.brand_id)
        if not error_free:
            return False, result
        if result is None:
            return False, CompanyBrandNotMatch(status=404, message=MessagesKeys.COMPANY_AND_BRAND_NOT_MATCH,
                                               params=None)
        return True, result

    def _is_product_has_id(self):
        json_obj_list = []
        for items in self.product_info.json_obj:
            json_obj_list.append(items)
        if Keys.ID in self.product_info.json_obj:
            return False, self.product_info.json_obj[Keys.ID]
        else:
            return True, self.supplier_id

    def _is_supplier_update_own_product(self):
        error_free, result = Supplier.check_id_and_phone_number_match(self.product_info.json_obj[Keys.ID], self.phone_number)
        if not error_free:
            return False, result
        if result is None:
            return False, SupplierIdPhoneNumberNotMatch(status=404, message=MessagesKeys.ID_AND_PHONE_NUMBER_NOT_MATCH,
                                                        params=None)
        return True, self.supplier_id

    def _update_product_info(self):
        return Product.update_by_id(self.product_info.json_obj[Keys.ID], db, self.product_info.json_obj)

    def _add_new_product(self):
        return self.product.add(db_connection=db)
