#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db, global_logger
from core.controller import BaseController
from core.messages import HttpStatus
from core.result.failure.invalid_service_grade import InvalidServiceGrade
from core.result.success.success_service_type_registration import SuccessServiceTypeRegistration
from persistence.database.entity.service_grade import ServiceGrade

logger = global_logger


class ServiceTypeRegistrationController(BaseController):
    def __init__(self, service, converter):
        self.converter = converter
        self.service_type = service.service_type
        self.service_grades = service.service_grades

    def execute(self):
        result = self._add_service_grade()
        if not result[0]:
            dct = result[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        dct = result[1].dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    def _add_service_grade(self):
        error = None
        loaded_grades_result = self._load_grades()
        if not loaded_grades_result[0]:
            return loaded_grades_result

        loaded_grades = loaded_grades_result[1]
        db.session.begin(subtransactions=True)
        try:
            for grade in loaded_grades:
                register_result = ServiceGrade.register_service_type(grade, self.service_type, db)
                if not register_result[0]:
                    error = register_result[1]
                    raise Exception()
        except:
            db.session.rollback()
            return False, error

        return True, SuccessServiceTypeRegistration(status=HttpStatus.OK,
                                                    message="Types registered in grades",
                                                    params=[])

    def _load_grades(self):
        grades = []
        result = True, grades
        for grade_id in self.service_grades:
            loaded_grade = ServiceGrade.load_service_grade(grade_id)
            if loaded_grade is None:
                result = False, InvalidServiceGrade(status=HttpStatus.NOT_FOUND,
                                                    message="invalid grade id: " + str(grade_id),
                                                    params=[])
                break
            grades.append(loaded_grade)

        return result
