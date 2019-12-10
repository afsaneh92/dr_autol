from app import db, global_logger
from core.controller import BaseController
from core.messages.translator.messages_keys import MessagesKeys
from core.result.failure.car_not_exist import CarNotExist
from persistence.database.entity.car import Car

logger = global_logger



class DeleteCarController(BaseController):

    def __init__(self, car_info, converter):
        self.car_info = car_info
        self.converter = converter

    def execute(self):
        result_existence = self._is_car_existence()
        if not result_existence[0]:
            dct = result_existence[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        result_delete = self._delete_car()
        dct = result_delete[1].dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    def _is_car_existence(self):
        result = Car.find(id=self.car_info.car_id, deleted=False)
        if not result[0]:
            return result

        if len(result[1]) == 0:
            params = {"car_id": self.car_info.car_id}
            fail = CarNotExist(status=400, message=MessagesKeys.CAR_NOT_EXIST, params=params)
            return False, fail

        return True,

    def _delete_car(self):
        return Car.delete_by_id(db, self.car_info.car_id)
