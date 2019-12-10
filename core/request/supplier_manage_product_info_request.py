from core.interfaces.serialization import Serializable
from core.messages.keys import Keys
from core.request.base_request import RequestBaseClass
from core.result import Result
from core.validation.session_helper.session_manager import SessionManager
from persistence.database.entity.product import Product
from persistence.database.entity.user.supplier import Supplier


class SupplierManageProductInfoRequest(RequestBaseClass):
    def __init__(self, json_obj):
        self.json_obj = json_obj
        self.phone_number = None
        self.product = None
        self.supplier_id = None
        # self.product_id = json_obj[Keys.ID]

    def validate_pattern(self):
        invalid_params = []
        result_id_existence = self.check_optional_item_is_in_dict(self.json_obj, Keys.ID)
        if result_id_existence[0]:
            if not isinstance(self.json_obj[Keys.ID], int):
                invalid_params.append(Result.language.ID_IS_NOT_INTEGER)
        if not isinstance(self.json_obj[Keys.COMPANY_ID], int):
            invalid_params.append(Result.language.COMPANY_ID_IS_NOT_INTEGER)
        if not isinstance(self.json_obj[Keys.MINIMUM_ORDER], int):
            invalid_params.append(Result.language.MINIMUM_ORDER_IS_NOT_INT)
        if not isinstance(self.json_obj[Keys.BRAND_ID], int):
            invalid_params.append(Result.language.BRAND_ID_IS_NOT_INTEGER)
        if not isinstance(self.json_obj[Keys.SUB_CATEGORY_ID], int):
            invalid_params.append(Result.language.SUB_CATEGORY_ID_IS_NOT_INTEGER)
        if isinstance(self.json_obj[Keys.PRICE], int):
            if self.json_obj[Keys.PRICE] <= 0:
                invalid_params.append(Result.language.PRICE_IS_NOT_VALID)
        else:
            invalid_params.append(Result.language.PRICE_IS_NOT_VALID)
        if len(invalid_params) > 0:
            return False, {Keys.INVALID_PARAMS: invalid_params}
        return True, Keys.REGEX_IS_VALID

    @staticmethod
    def is_session_valid():
        return SessionManager.is_key_exist(key=Keys.PHONE_NUMBER)

    @staticmethod
    def pre_deserialize(json_dict):
        """
        before deserializing, run this method. It help to check json and confirm it's schema.
        :param json_dict:
        :return:
        """
        missed_params = []
        if Keys.SUB_CATEGORY_ID not in json_dict:
            missed_params.append(Result.language.MISSING_PRODUCT_ID_IN_JSON)
        if Keys.COMPANY_ID not in json_dict:
            missed_params.append(Result.language.MISSING_COMPANY_ID_IN_JSON)
        if Keys.PRICE not in json_dict:
            missed_params.append(Result.language.MISSING_PRICE_IN_JSON)
        if Keys.BRAND_ID not in json_dict:
            missed_params.append(Result.language.MISSING_BRAND_ID_IN_JSON)
        if Keys.CODE not in json_dict:
            missed_params.append(Result.language.MISSING_CODE_IN_JSON)
        if Keys.MINIMUM_ORDER not in json_dict:
            missed_params.append(Result.language.MISSING_MINIMUM_ORDER_IN_JSON)
        if len(missed_params) > 0:
            return False, missed_params

        return True,

    @staticmethod
    def check_optional_item_is_in_dict(dictionary, optional_item):
        list_of_optional_item = []
        for item in dictionary:
            if item == optional_item:
                list_of_optional_item.append(optional_item)
        if len(list_of_optional_item) > 0:
            return True, optional_item
        else:
            return False,

    def post_deserialize(self):
        return self.validate_pattern()

    def deserialize(self):
        if not type(self.json_obj) is dict:
            json_dict = Serializable.convert_input_to_dict(self.json_obj)
        else:
            json_dict = self.json_obj
        result = SupplierManageProductInfoRequest.pre_deserialize(json_dict)
        res = self.is_session_valid()
        if not res:
            return False, Result.language.SESSION_KEY_IS_NOT_VALID
        if result[0]:
            self.phone_number = SessionManager.retrieve_session_value_by_key(key=Keys.PHONE_NUMBER)
            self.supplier_id = SessionManager.retrieve_session_value_by_key(key=Keys.USER_ID)

            code = json_dict[Keys.CODE]
            company_id = json_dict[Keys.COMPANY_ID]
            sub_category_id = json_dict[Keys.SUB_CATEGORY_ID]
            brand_id = json_dict[Keys.BRAND_ID]
            price = json_dict[Keys.PRICE]
            minimum_order = json_dict[Keys.MINIMUM_ORDER]
            check_id_existence = self.check_optional_item_is_in_dict(json_dict, Keys.ID)
            if check_id_existence[0]:
                id = json_dict[Keys.ID]
            description_result = self.check_optional_item_is_in_dict(json_dict, Keys.DESCRIPTION)
            if description_result[0]:
                description = json_dict[Keys.DESCRIPTION]
                product = Product(minimum_order=minimum_order, company_id=company_id, code=code,
                                  sub_category_id=sub_category_id,
                                  price=price
                                  , supplier_id=self.supplier_id
                                  , brand_id=brand_id, description=description)
            else:
                product = Product(minimum_order=minimum_order, company_id=company_id, code=code,
                                  sub_category_id=sub_category_id,
                                  price=price, supplier_id=self.supplier_id,
                                  brand_id=brand_id)
            self.product = product
            result_pattern = self.post_deserialize()
            if not result_pattern[0]:
                return result_pattern
            return True, self

        return result
