from app import global_logger
from core.controller import BaseController
from persistence.database.entity.car import Car

logger = global_logger



class ListCarsController(BaseController):

    def __init__(self, user_id, converter):
        self.user_id = user_id
        self.converter = converter

    def execute(self):
        result_find_all = self._find_all()
        if not result_find_all[0]:
            dct = result_find_all[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        dct = result_find_all[1].dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    def _find_all(self):
        return Car.find_all(user_id=self.user_id, deleted=False)
