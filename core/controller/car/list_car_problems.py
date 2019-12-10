import logging

from app import global_logger
from core.controller import BaseController
from persistence.database.entity.jobs import Jobs
from persistence.database.entity.job_.autoservice_job import AutoServiceJob

logger = global_logger



class CarProblemListController(BaseController):

    def __init__(self, car_owner_id, converter):
        self.car_owner_id = car_owner_id
        self.converter = converter

    def execute(self):
        result_find_all = self._find_all()
        if not result_find_all[0]:
            dct = result_find_all[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        dct = result_find_all[1].dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    def _find_all(self):
        return AutoServiceJob.find_order_list(car_owner_id=self.car_owner_id)
