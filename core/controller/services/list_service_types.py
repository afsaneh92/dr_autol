# !/usr/bin/env python
# -*- coding: utf-8 -*-

from app import global_logger
from core.controller import BaseController
from persistence.database.entity.service_grade import ServiceGrade

logger = global_logger


class ListServiceTypesController(BaseController):
    def __init__(self, service_grade_id, converter):
        self.converter = converter
        self.service_grade_id = service_grade_id

    def execute(self):
        result = self._list_service_types()
        if not result[0]:
            dct = result[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        dct = result[1].dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    def _list_service_types(self):
        list_returned = ServiceGrade.list_service_types(self.service_grade_id)
        if not list_returned[0]:
            return list_returned

        return True, list_returned[1]
