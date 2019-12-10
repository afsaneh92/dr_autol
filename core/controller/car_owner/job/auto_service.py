#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jdatetime

from app import db, global_logger
from core.controller import BaseController
from core.messages.keys import Keys
from core.result import Result
from core.result.failure.auto_service_bad_consumable_items import BadCarProblemConsumableItems
from core.result.failure.not_found_product import NotFoundProduct
from core.result.failure.not_in_same_category import NotInSameCategory
from core.result.failure.not_in_same_grade import NotInSameGrade
from core.services.push_notifications.iws_announcement import IWSAnnouncement
from persistence.database.entity.car_problem import CarProblem
from persistence.database.entity.consumable_item import ConsumableItem
from persistence.database.entity.job_.job import Job
from persistence.database.entity.service_definition import ServicesDefinition
from utilities import calculate_duration, calculate_finish_schedule

logger = global_logger


class AutoServiceRequestController(BaseController):

    def __init__(self, job, converter):
        self.job = job
        self.car_problems = job.car_problems
        self.service_definitions = None
        self.service_grade = job.service_definition
        self.converter = converter

    def execute(self):
        error_free, service_definitions = self._load_services()
        if not error_free:
            dct = service_definitions.dictionary_creator()
            return self.serialize(dct, converter=self.converter)
        self.service_definitions = service_definitions
        same_def_result = AutoServiceRequestController.is_in_same_definition(self.service_definitions,
                                                                             self.service_grade)
        if not same_def_result[0]:
            dct = same_def_result[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        result_finish_schedule = self._calculate_finish_schedule()
        if not result_finish_schedule[0]:
            dct = result_finish_schedule[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        self._create_car_problems()
        price_result = self._calculate_price()
        if not price_result[0]:
            dct = price_result[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)
        self.job.job.question_set_id = service_definitions[0].question_set_id
        result_registration_status = self._add_job()

        if not result_registration_status[0]:
            dct = result_registration_status[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)
        job_id = result_registration_status[1].params[Keys.ID]
        persian_time = self.convert_greo_to_jalali(self.job.job.start_schedule)
        self.send_notification(job_id, persian_time)
        dct = result_registration_status[1].dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    def _add_job(self):
        return Job.register_problem(db, self.job.job, self.car_problems)

    def _create_car_problems(self):
        car_problems = []

        productable_items = self.car_problems[Keys.PRODUCTABLE_ITEMS]
        for service_definition_id, consumable_item_id in productable_items.iteritems():
            car_problem = CarProblem(services_definition_id=service_definition_id,
                                     consumable_item_id=consumable_item_id)
            car_problems.append(car_problem)

        non_productable_items = self.car_problems[Keys.NON_PRODUCTABLE_ITEMS]
        for service_definition_id in non_productable_items:
            car_problem = CarProblem(services_definition_id=service_definition_id)
            car_problems.append(car_problem)
        self.car_problems = car_problems

    def _calculate_price(self):
        total_price = 0
        for problem in self.car_problems:
            if problem.consumable_item_id is not None:
                item = ConsumableItem.query.filter(ConsumableItem.id == problem.consumable_item_id).first()
                if item is None:
                    return False, NotFoundProduct(status=404, params={'id':ConsumableItem.id })
                total_price += item.price
        for definition in self.service_definitions:
            total_price += definition.pay
        self.job.job.price = total_price
        return True,

    def send_notification(self, job_id, time):
        IWSAnnouncement.request_notification( self.car_problems, self.job.job.business_owner_id, self.job.job.car_id, job_id, time)

    def _calculate_finish_schedule(self):
        service_types = []
        for problem in self.service_definitions:
            # ServicesDefinition.query.all()
            # AutoServiceRequestController.load_duration(problem)
            service_types.append(problem.id)
        result = calculate_duration(self.service_definitions)
        if not result[0]:
            return False, result[1]
        self.job.job.finish_schedule = calculate_finish_schedule(self.job.job.start_schedule, result[1])
        return True,

    # @staticmethod
    # def load_service_grade(grade):
    #     return ServiceGrade.load_service_grade(grade)

    # def execute(self):
    #     is_valid = self._load_job()
    #     if not is_valid[0]:
    #         dct = is_valid[1].dictionary_creator()
    #         return self.serialize(dct, converter=self.converter)
    #     is_exist = BaseJobController.is_exist(is_valid[1])
    #     if not is_exist[0]:
    #         dct = is_exist[1].dictionary_creator()
    #         return self.serialize(dct, converter=self.converter)
    #     self.job = is_valid[1]
    #     update_result = self._update_job()
    #     if not update_result[0]:
    #         dct = update_result[1].dictionary_creator()
    #         return self.serialize(dct, converter=self.converter)
    #
    #     self.push_notification_to_car_owner()
    #
    #     dct = update_result[1].dictionary_creator()
    #     return self.serialize(dct, converter=self.converter)
    #
    # def _load_job(self):
    #     return Job.load_job(self.job.id)
    #
    # def _update_job(self):
    #     status = Status.query.filter(Status.name == Keys.STATUS_ACCEPTED_BY_BUSINESS_OWNER).first()
    #     data = {Keys.STATUS_ID: status.id}
    #     return AutoServiceJob.accept_deny_job(self.job, data, db)
    #
    # def push_notification_to_car_owner(self):
    #     CarOwnerAnnouncement.accept_job(self.job)

    # @staticmethod
    # def load_duration(problem):
    #     s_d =ServicesDefinition.query.filter(ServicesDefinition.id == problem.services_definition_id).first()
    #     return s_d.service_types[0].duration

    def _load_services(self):
        service_definitions = []
        has = self.car_problems[Keys.PRODUCTABLE_ITEMS]
        try:
            for service_definition_id, service_type_id in has.iteritems():
                error_free, service_definition = ServicesDefinition.load_service_by_id(service_definition_id)
                if not error_free or len(service_definition.service_type.consumable_items) == 0:
                    raise Exception()
                service_definitions.append(service_definition)
        except:
            return False, BadCarProblemConsumableItems(status=404, message= Result.language.CAR_PROBLEM_WITHOUT_CONSUMABLE_ITEMS)

        not_has = self.car_problems[Keys.NON_PRODUCTABLE_ITEMS]
        try:
            for service_definition_id in not_has:
                error_free, service_definition = ServicesDefinition.load_service_by_id(service_definition_id)
                # if not error_free or len(service_definition.service_type.consumable_items) > 0:
                #     raise Exception()
                if not error_free or service_definition is None:
                    raise Exception()
                service_definitions.append(service_definition)
        except:
            return False, BadCarProblemConsumableItems(status=404, message= Result.language.CAR_PROBLEM_WITH_CONSUMABLE_ITEMS)
        return True, service_definitions

        # self.car_problems['has_not_product']
        # for problem in self.job.car_problems:
        #     self.service_definitions.append(ServicesDefinition.load_service_by_id(problem.services_definition_id))

    @staticmethod
    def is_in_same_definition(service_definitions, service_grade):
        result = True,
        for service_definition in service_definitions:
            if not service_grade[Keys.SERVICE_GRADE].lower() == service_definition.service_grade.lower():
                result = False, NotInSameGrade(status=404)
                break
            if not service_grade[Keys.SERVICE_CATEGORY].lower() == service_definition.service_category.lower():
                result = False, NotInSameCategory(404)
                break
        return result

    def convert_greo_to_jalali(self, time):
        hour = time.hour
        min = time.minute
        weekday = jdatetime.date.fromgregorian(date=time).j_weekdays_fa[jdatetime.date.fromgregorian(date=time).weekday()]
        month = jdatetime.date.fromgregorian(date=time).j_months_fa[jdatetime.date.fromgregorian(date=time).month -1]
        day = jdatetime.date.fromgregorian(date=time).day
        return weekday + " " + str(day) + " " + month + " " + u"ساعت:" + str(hour) + u" دقیقه: " + str(min)

    def add_question_set(self):
        pass