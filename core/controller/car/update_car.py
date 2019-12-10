from app import db, global_logger
from core.controller import BaseController
from core.messages.translator.messages_keys import MessagesKeys
from core.result.failure.car_not_exist import CarNotExist
from core.result.failure.car_registered_before import CarRegisteredBefore
from persistence.database.entity.car import Car

logger = global_logger


class UpdateCarController(BaseController):

    def __init__(self, car, converter):
        self.car = car
        self.converter = converter

    def execute(self):
        result_existence = self._is_car_existence()
        if not result_existence[0]:
            dct = result_existence[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        result_belongs = self._is_belongs_to_this_user(result_existence[1])
        if not result_belongs[0]:
            dct = result_belongs[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        result_update = self._update_car()
        dct = result_update[1].dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    def _is_car_existence(self):
        result = Car.find(id=self.car.id, deleted=False)
        if not result[0]:
            return result

        if len(result[1]) == 0:
            params = {"car_id": self.car.id}
            fail = CarNotExist(status=400, message=MessagesKeys.CAR_NOT_EXIST, params=params)
            return False, fail

        return True, result[1][0]

    def _update_car(self):
        if len(self.car.vin_number) == 0:
            vin_number = None
        else:
            vin_number = self.car.vin_number
        data = {"vin_number": vin_number, "plate_number": self.car.plate_number,
                "auto_type_id": self.car.auto_type_id}
        return self.car.update(db, data)

    def _is_belongs_to_this_user(self, car):

        if self.car.car_owner_id != car.car_owner_id:
            params = {"plate_number": self.car.plate_number}
            fail = CarRegisteredBefore(status=400, message=MessagesKeys.CAR_REGISTERED_BEFORE, params=params)
            return False, fail
        return True,
        # result = Car.find(plate_number=self.car.plate_number)
        # if not result[0]:
        #     return result
        #
        # if len(result[1]) > 0:
        #     params = {"plate_number": self.car.plate_number}
        #     fail = CarRegisteredBefore(status=400, message=MessagesKeys.CAR_REGISTERED_BEFORE, params=params)
        #     return False, fail
        #
        # return True,
