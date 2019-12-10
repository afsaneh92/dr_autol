from core.interfaces.serialization import Serializable
from core.messages.keys import Keys
from core.request.base_request import RequestBaseClass
from core.validation.helpers import name_regex_checker, password_regex_checker, phone_number_regex_checker
from persistence.database.entity.user.auto_service import AutoServiceBusinessOwner
from persistence.database.entity.user.car_wash import CarWashBusinessOwner


class IWSRegisterRequest(RequestBaseClass):

    def __init__(self, json_obj):
        self.iws = None
        self.json_obj = json_obj

    def validate_pattern(self):
        invalid_params = []

        result = self._password_checker(self.iws.password)
        if not result[0]:
            invalid_params.append(result[1])
        result = self._phone_number_cheker(self.iws.phone_number)
        if not result[0]:
            invalid_params.append(result[1])
        result = self._name_checker(self.iws.name)
        if not result[0]:
            invalid_params.append(result[1])

        if len(invalid_params) > 0:
            return False, {"invalid_params": invalid_params}
        return True, "regex is valid"

    def _password_checker(self, password):
        return password_regex_checker(password)

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
        if 'phone_number' not in json_dict:
            missed_params.append("missing_'phone_number'_in_json")
        if 'password' not in json_dict:
            missed_params.append("missing_'password'_in_json")
        if 'name' not in json_dict:
            missed_params.append("missing_'name'_in_json")
        if 'business_owner_type' not in json_dict:
            missed_params.append("missing_business_owner_type_in_json")
        if Keys.REG_ID not in json_dict:
            missed_params.append("missing_reg_id_in_json")
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
        result = IWSRegisterRequest.pre_deserialize(json_dict)
        if result[0]:

            self.iws = self.create_user(json_dict)
            result_pattern = self.post_deserialize()
            if not result_pattern[0]:
                return result_pattern
            return True, self
        return result

    def create_user(self, json_dict):
        if json_dict['business_owner_type'] == "AutoService":
            return AutoServiceBusinessOwner(name=json_dict["name"], password=json_dict["password"],
                                            phone_number=json_dict["phone_number"], reg_id=json_dict[Keys.REG_ID])
        else:
            return CarWashBusinessOwner(name=json_dict["name"], password=json_dict["password"],
                                        phone_number=json_dict["phone_number"], reg_id=json_dict[Keys.REG_ID])
