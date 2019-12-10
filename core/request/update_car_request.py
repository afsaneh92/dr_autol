from core.interfaces.serialization import Serializable
from core.messages.keys import Keys
from core.request.base_request import RequestBaseClass
from core.validation.helpers import vin_number_regex_checker, plate_number_regex_checker
from core.validation.session_helper.session_manager import SessionManager
from persistence.database.entity.car import Car


class UpdateCarRequest(RequestBaseClass):

    def __init__(self, json_obj):
        self.car = None
        self.json_obj = json_obj

    def validate_pattern(self):
        res = self._car_info_checker()
        if not res[0]:
            return res

        res = self._id_checker(self.car.id)
        if not res[0]:
            return res

        return True,

    def _vin_number_checker(self, phone_number):
        return vin_number_regex_checker(phone_number)

    def _plate_number_checker(self, plate_number):
        return plate_number_regex_checker(plate_number)

    def _car_info_checker(self):
        invalid_params = []
        plate_result = self._plate_number_checker(self.car.plate_number)
        if not plate_result[0]:
            invalid_params.append(plate_result[1])
        if len(self.car.vin_number) > 0:
                vin_result = self._vin_number_checker(self.car.vin_number)
                if not vin_result[0]:
                    invalid_params.append(vin_result[1])

        if len(invalid_params) > 0:
            return False, invalid_params

        return True,

    def _id_checker(self, id):
        if id is int:
            return False,
        return True,

    @staticmethod
    def pre_deserialize(json_dict):
        """
        before deserializing, run this method. It help to check json and confirm it's schema.
        :param json_dict:
        :return:
        """
        missed_params = []
        if 'car_id' not in json_dict:
            missed_params.append("missing_car_id_in_json")
        if 'car_info' not in json_dict:
            missed_params.append("missing_new_info_in_json")
        elif 'car_info' in json_dict:
            new_info = json_dict["car_info"]
            if 'vin_number' not in new_info:
                missed_params.append("missing_vin_number_in_json")
            if 'plate_number' not in new_info:
                missed_params.append("missing_plate_number_in_json")
            if 'auto_type' not in new_info:
                missed_params.append("missing_auto_type_in_json")

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
        result = UpdateCarRequest.pre_deserialize(json_dict)
        if result[0]:
            vin_number = json_dict['car_info']['vin_number']
            plate_number = json_dict['car_info']['plate_number']
            auto_type = json_dict['car_info']['auto_type']
            car_id = json_dict['car_id']
            car = Car(id=car_id, vin_number=vin_number, plate_number=plate_number,
                      auto_type_id=auto_type, car_owner_id=SessionManager.retrieve_session_value_by_key(Keys.USER_ID))
            self.car = car
            result_pattern = self.post_deserialize()
            if not result_pattern[0]:
                return result_pattern
            return True, self
        return result
