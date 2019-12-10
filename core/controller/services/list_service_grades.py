#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import global_logger
from core.controller import BaseController
from persistence.database.entity.service_grade import ServiceGrade

logger = global_logger



class ListServiceGradesController(BaseController):
    def __init__(self, converter):
        self.converter = converter

    def execute(self):
        result = ListServiceGradesController._list_service_grades()
        if not result[0]:
            dct = result[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        dct = result[1].dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    @staticmethod
    def _list_service_grades():
        list_returned = ServiceGrade.list_service_grades()
        if not list_returned[0]:
            return list_returned

        return True, list_returned[1]
