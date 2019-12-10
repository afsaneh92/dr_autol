from core.interfaces.serialization import Serializable
from core.messages.keys import Keys
from core.request.base_request import RequestBaseClass
from core.result import Result
from core.validation.session_helper.session_manager import SessionManager
from persistence.database.entity.user.supplier import Supplier


class SupplierDeleteProductRequest(RequestBaseClass):
    def __init__(self, json_obj):
        self.json_obj = json_obj
        self.product_id = self.json_obj[Keys.PRODUCT_ID]
        self.phone_number = None
        self.supplier_id = None

    def validate_pattern(self):
        res = self._id_checker(self.product_id)
        if not res[0]:
            return False,
        return res

    @staticmethod
    def _id_checker(id):
        if id is int:
            return False,
        return True,

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
        if Keys.PRODUCT_ID not in json_dict:
            missed_params.append(Result.language.MISSING_PRODUCT_ID_IN_JSON)
        if len(missed_params) > 0:
            return False, missed_params

        return True,

    def post_deserialize(self):
        return self.validate_pattern()

    def deserialize(self):
        if not type(self.json_obj) is dict:
            json_dict = Serializable.convert_input_to_dict(self.json_obj)
        else:
            json_dict = self.json_obj
        result = SupplierDeleteProductRequest.pre_deserialize(json_dict)
        res = self.is_session_valid()
        if not res:
            return False, Result.language.SESSION_KEY_IS_NOT_VALID
        if result[0]:
            self.phone_number = SessionManager.retrieve_session_value_by_key(key=Keys.PHONE_NUMBER)
            self.supplier_id = SessionManager.retrieve_session_value_by_key(key=Keys.USER_ID)
            # check_supplier = Supplier.check_supplier(self.phone_number)
            # if check_supplier[0]:
            #     self.supplier_id = check_supplier[1]

        result = SupplierDeleteProductRequest.pre_deserialize(json_dict)
        if result[0]:
            self.product_id = json_dict[Keys.PRODUCT_ID]
            result_pattern = self.post_deserialize()
            if not result_pattern[0]:
                return result_pattern
            return True, self
        return result
