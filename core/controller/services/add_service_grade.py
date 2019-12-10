#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db, global_logger
from core.controller import BaseController

logger = global_logger


class AddServiceGradesController(BaseController):
    def __init__(self, service_grade, converter):
        self.converter = converter
        self.service_grade = service_grade.service_grade

    def execute(self):
        result = self._add_service_grade()
        if not result[0]:
            dct = result[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        dct = result[1].dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    def _add_service_grade(self):
        result = self.service_grade.add_service_grade(db_connection=db)
        if not result[0]:
            return result

        return True, result[1]
