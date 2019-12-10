from app import db, global_logger
from core.controller import BaseController
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result.failure.auto_type_and_model_are_not_match import AutoTypeAndModelNotMatched
from core.result.failure.car_registered_before import CarRegisteredBefore
from persistence.database.entity.auto_type import AutoType
from persistence.database.entity.car import Car

logger = global_logger


class NewCarController(BaseController):

    def __init__(self, car_info, converter):
        self.car_info = car_info
        self.converter = converter

    def execute(self):
        result_registration_status = self._is_registered_before()
        if not result_registration_status[0]:
            dct = result_registration_status[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)
        result_match = self._are_auto_type_and_model_matched()
        if not result_match[0]:
            dct = result_match[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        result = self._add_new_car()
        dct = result[1].dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    def _is_registered_before(self):
        result = Car.find(plate_number=self.car_info.car.plate_number)
        if not result[0]:
            return result

        if len(result[1]) > 0:
            params = {Keys.PLATE_NUMBER: self.car_info.car.plate_number}
            fail = CarRegisteredBefore(status=404, message=MessagesKeys.CAR_REGISTERED_BEFORE, params=params)
            return False, fail

        return True,

    def _add_new_car(self):
        if self.car_info.car.vin_number == "":
            self.car_info.car.vin_number = None
        return self.car_info.car.add(db, self.car_info.car_owner)

    def _are_auto_type_and_model_matched(self):
        auto = AutoType.are_auto_type_and_auto_model_matched(self.car_info.json_obj[Keys.CAR_INFO][Keys.AUTO_TYPE],
                                                             self.car_info.json_obj[Keys.CAR_INFO][Keys.AUTO_MODEL])
        if auto is None:
            return False, AutoTypeAndModelNotMatched(status=404, message=MessagesKeys.AUTO_TYPE_AND_MODEL_ARE_NOT_MATCH,
                                                     params=None)
        else:
            return True, auto
