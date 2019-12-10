from core.interfaces.serialization import Serializable
from core.messages.keys import Keys
from core.request.base_request import RequestBaseClass
from core.result import Result
from core.validation.session_helper.session_manager import SessionManager
from persistence.database.entity.product_search_parameters import ProductsSearchParameters
from persistence.database.entity.user.supplier import Supplier


class SearchOnProductsRequest(RequestBaseClass):
    def __init__(self, json_obj):
        self.json_obj = json_obj
        self.options = None
        self.phone_number = None
        self.supplier_id = None

    def validate_pattern(self):
        res = self._validate_options(self.options)
        if not res[0]:
            return res

        return True, res[1]

    @staticmethod
    def _validate_options(options):
        search = ProductsSearchParameters()
        if not options:
            return True, search
        if Keys.SUB_CATEGORY_ID in options:
            if not isinstance(options[Keys.SUB_CATEGORY_ID], int):
                return False, Result.language.SUB_CATEGORY_ID_IS_NOT_INTEGER
            search.sub_category_id = options[Keys.SUB_CATEGORY_ID]
        if Keys.BRAND_ID in options:
            if not isinstance(options[Keys.BRAND_ID], int):
                return False, Result.language.BRAND_ID_IS_NOT_INTEGER
            search.brand_id = options[Keys.BRAND_ID]
        if Keys.COMPANY_ID in options:
            if not isinstance(options[Keys.BRAND_ID], int):
                return False, Result.language.BRAND_ID_IS_NOT_INTEGER
            search.company_id = options[Keys.COMPANY_ID]
        if Keys.CODE in options:
            if not isinstance(options[Keys.CODE], unicode):
                return False, Result.language.CODE_IS_NOT_STRING
            search.code = options[Keys.CODE]
        if Keys.SUPPLIER_ID in options:
            if not isinstance(options[Keys.SUPPLIER_ID], int):
                return False, Result.language.SUPPLIER_ID_IS_NOT_INTEGER
            search.supplier_id = options[Keys.SUPPLIER_ID]
        if Keys.MINIMUM_ORDER in options:
            if not isinstance(options[Keys.MINIMUM_ORDER], int):
                return False, Result.language.MINIMUM_ORDER_IS_NOT_INT
            search.minimum_order = options[Keys.MINIMUM_ORDER]

        if Keys.REQUESTED_NUMBER in options:
            if not isinstance(options[Keys.REQUESTED_NUMBER], int):
                return False, Result.language.REQUESTED_NUMBER_IS_NOT_INT
            search.requested_number = options[Keys.REQUESTED_NUMBER]
        if Keys.ACCEPTED_NUMBER in options:
            if not isinstance(options[Keys.ACCEPTED_NUMBER], int):
                return False, Result.language.ACCEPTED_NUMBER_IS_NOT_INT
            search.accepted_number = options[Keys.ACCEPTED_NUMBER]
        if Keys.SUPPLIER_STATUS_ID in options:
            if not isinstance(options[Keys.SUPPLIER_STATUS_ID], int):
                return False, Result.language.SUPPLIER_STATUS_ID_IS_NOT_INT
            search.supplier_status_id = options[Keys.SUPPLIER_STATUS_ID]
        if Keys.MAX_PRICE in options:
            if not isinstance(options[Keys.MAX_PRICE], int):
                return False, Result.language.PRICE_IS_NOT_VALID
            if options[Keys.MAX_PRICE] < 0:
                return False, Result.language.PRICE_IS_NOT_VALID
            search.max_price = options[Keys.MAX_PRICE]

        if Keys.MIN_PRICE in options:
            if not isinstance(options[Keys.MIN_PRICE], int):
                return False, Result.language.PRICE_IS_NOT_VALID
            if options[Keys.MIN_PRICE] < 0:
                return False, Result.language.PRICE_IS_NOT_VALID
            search.min_price = options[Keys.MIN_PRICE]

        return True, search

    @staticmethod
    def pre_deserialize(json_dict):
        """
        before deserializing, run this method. It help to check json and confirm it's schema.
        :param json_dict:
        :return:
        """
        missed_params = []
        if Keys.OPTIONS not in json_dict:
            missed_params.append(Result.language.MISSING_OPTIONS_IN_JSON)

        if len(missed_params) > 0:
            return False, missed_params

        return True,

    def post_deserialize(self):
        return self.validate_pattern()

    @staticmethod
    def is_session_valid():
        return SessionManager.is_key_exist(key=Keys.PHONE_NUMBER)

    def deserialize(self):
        if not type(self.json_obj) is dict:
            json_dict = Serializable.convert_input_to_dict(self.json_obj)
        else:
            json_dict = self.json_obj
        result = SearchOnProductsRequest.pre_deserialize(json_dict)
        res = self.is_session_valid()
        if not res:
            return False, Result.language.SESSION_KEY_IS_NOT_VALID
        if result[0]:
            self.options = json_dict[Keys.OPTIONS]
            self.phone_number = SessionManager.retrieve_session_value_by_key(key=Keys.PHONE_NUMBER)
            self.supplier_id = SessionManager.retrieve_session_value_by_key(key=Keys.USER_ID)
            self.options[Keys.SUPPLIER_ID] = self.supplier_id

            result_pattern = self.post_deserialize()

            if not result_pattern[0]:
                return result_pattern
            return True, result_pattern[1]

        return result
