from core.interfaces.serialization import Serializable
from core.messages.keys import Keys
from core.request.base_request import RequestBaseClass
from core.result import Result
from core.validation.helpers import name_regex_checker, password_regex_checker, phone_number_regex_checker, \
    business_license_regex_checker
from persistence.database.entity.user.supplier import Supplier


class SupplierRegistrationRequest(RequestBaseClass):

    def __init__(self, json_obj):
        self.supplier = None
        self.json_obj = json_obj

    def validate_pattern(self):
        invalid_params = []
        if not isinstance(self.supplier.address, unicode):
            return False, Result.language.POST_VALIDATION_CALENDAR_ID

        result = self._password_checker(self.supplier.password)
        if not result[0]:
            invalid_params.append(result[1])
        result = self._phone_number_cheker(self.supplier.phone_number)
        if not result[0]:
            invalid_params.append(result[1])
        result = self._business_license_checker(self.supplier.business_license)
        if not result[0]:
            invalid_params.append(result[1])
        result = self._name_checker(self.supplier.name)
        if not result[0]:
            invalid_params.append(result[1])

        if len(invalid_params) > 0:
            return False, {Keys.INVALID_PARAMS: invalid_params}
        return True, Keys.REGEX_IS_VALID

    def _password_checker(self, password):
        return password_regex_checker(password)

    def _business_license_checker(self, phone_number):
        return business_license_regex_checker(phone_number)

    def _phone_number_cheker(self, phone_number):
        return phone_number_regex_checker(phone_number)

    def _name_checker(self, name):
        return name_regex_checker(name)

    @staticmethod
    def pre_deserialize(json_dict):
        """
        before deserializing, run this method. It help to check json and confirm it's schema.
        :param json_dict:
        :return:
        """
        missed_params = []
        if Keys.PHONE_NUMBER not in json_dict:
            missed_params.append(Result.language.MISSING_PHONE_NUMBER_IN_JSON)
        if Keys.NAME not in json_dict:
            missed_params.append(Result.language.MISSING_NAME_IN_JSON)
        if Keys.ADDRESS not in json_dict:
            missed_params.append(Result.language.MISSING_ADDRESS_IN_JSON)
        if Keys.BUSINESS_LICENSE not in json_dict:
            missed_params.append(Result.language.MISSING_BUSINESS_LICENSE_IN_JSON)
        if Keys.PASSWORD not in json_dict:
            missed_params.append(Result.language.MISSING_PASSWORD_IN_JSON)

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
        result = SupplierRegistrationRequest.pre_deserialize(json_dict)
        if result[0]:
            supplier = Supplier(name=json_dict[Keys.NAME], password=json_dict[Keys.PASSWORD],
                                business_license=json_dict[Keys.BUSINESS_LICENSE],
                                phone_number=json_dict[Keys.PHONE_NUMBER],
                                address=json_dict[Keys.ADDRESS])
            self.supplier = supplier
            result_pattern = self.post_deserialize()
            if not result_pattern[0]:
                return result_pattern
            return True, self
        return result
