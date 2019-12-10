from core.interfaces.serialization import Serializable
from core.messages.keys import Keys
from core.request.base_request import RequestBaseClass
from core.result import Result
from core.validation.helpers import plate_number_regex_checker, vin_number_regex_checker
from persistence.database.entity.car import Car


class NewCarRequest(RequestBaseClass):

    def __init__(self, json_obj):
        self.car_owner = None
        self.car = None
        self.json_obj = json_obj

    def validate_pattern(self):
        res = self._car_info_checker()
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

    @staticmethod
    def pre_deserialize(json_dict):
        """
        before deserializing, run this method. It help to check json and confirm it's schema.
        :param json_dict:
        :return:
        """
        missed_params = []
        if Keys.CAR_OWNER not in json_dict:
            missed_params.append(Result.language.MISSING_CAR_OWNER_IN_JSON)
        if Keys.CAR_INFO not in json_dict:
            missed_params.append(Result.language.MISSING_CAR_INFO_IN_JSON)
        elif Keys.CAR_INFO in json_dict:
            car_info = json_dict[Keys.CAR_INFO]
            # if Keys.VIN_NUMBER not in car_info:
            #     missed_params.append(Result.language.MISSING_VIN_NUMBER_IN_JSON)
            if Keys.PLATE_NUMBER not in car_info:
                missed_params.append(Result.language.MISSING_PLATE_NUMBER_IN_JSON)
            if Keys.AUTO_TYPE not in car_info:
                missed_params.append(Result.language.MISSING_AUTO_TYPE_ID_IN_JSON)
            if Keys.AUTO_MODEL not in car_info:
                missed_params.append(Result.language.MISSING_AUTO_MODEL_ID_IN_JSON)
            if Keys.CAR_COLOR not in car_info:
                missed_params.append(Result.language.MISSING_COLOR_ID_IN_JSON)
            if Keys.CURRENT_KILOMETER not in car_info:
                missed_params.append(Result.language.MISSING_CURRENT_KILOMETER_IN_JSON)

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
        result = NewCarRequest.pre_deserialize(json_dict)
        if result[0]:
            car_info = json_dict[Keys.CAR_INFO]
            vin_number = ''
            if Keys.VIN_NUMBER not in car_info:
                vin_number = json_dict[Keys.CAR_INFO][Keys.VIN_NUMBER]

            plate_number = json_dict[Keys.CAR_INFO][Keys.PLATE_NUMBER]
            auto_type = json_dict[Keys.CAR_INFO][Keys.AUTO_TYPE]
            color = json_dict[Keys.CAR_INFO][Keys.CAR_COLOR]
            auto_model = json_dict[Keys.CAR_INFO][Keys.AUTO_MODEL]
            current_kilometer = json_dict[Keys.CAR_INFO][Keys.CURRENT_KILOMETER]
            car = Car(vin_number=vin_number, plate_number=plate_number, auto_type_id=auto_type,
                      color_id=color, current_kilometer=current_kilometer, auto_model_id=auto_model)
            self.car_owner = json_dict[Keys.CAR_OWNER]

            self.car = car
            result_pattern = self.post_deserialize()
            if not result_pattern[0]:
                return result_pattern
            return True, self
        return result
