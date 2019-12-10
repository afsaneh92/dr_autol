#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from app import db
from core.controller import BaseController
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result.failure.bad_range_rates import BadRangRate
from core.result.failure.job_and_car_owner_are_not_match import JobAndCarOwnerNotMatch
from core.result.failure.not_finished_job import NotFinishedJob
from core.result.failure.not_found_job import JobNotFound
from core.result.failure.not_found_user import UserNotFound
from core.result.failure.rated_before import RatedBefore
from persistence.database.entity.job_.job import Job
from persistence.database.entity.user.car_owner import CarOwner

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class RateJobsController(BaseController):
    def __init__(self, request_info, converter):
        self.rate = request_info.rate
        self.converter = converter
        self.job_id = request_info.job_id
        self.phone_number = request_info.phone_number

    def execute(self):
        error_free, job_result = self._is_job_existence()
        if not error_free:
            dct = job_result.dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        error_free, existence_car_owner_result = self._is_car_owner_existence()
        if not error_free:
            dct = existence_car_owner_result.dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        error_free, match_job_to_car_owner = self._is_car_owner_and_his_job_matched(existence_car_owner_result,
                                                                                    job_result)
        if not error_free:
            dct = match_job_to_car_owner.dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        error_free, job_finished_result = self._is_job_finished(job_result)
        if not error_free:
            dct = job_finished_result.dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        error_free, not_rated_before = self._is_rated_before(job_result)
        if not error_free:
            dct = not_rated_before.dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        error_free, limit_rating_result = self._limit_rating(job_result, self.rate)
        if not error_free:
            dct = limit_rating_result.dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        error_free, check_rate_result = self._check_rate_range()
        if not error_free:
            dct = check_rate_result.dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        result = self._update_rate(job_result, self.rate)
        dct = result[1].dictionary_creator()
        return self.serialize(dct, self.converter)

    def _is_job_existence(self):
        error_free, result = Job.find(id=self.job_id)
        if not error_free:
            return False, result
        if len(result) == 0:
            return False, JobNotFound(status=404, message=MessagesKeys.ID_IS_NOT_IN_DB, params=None)
        self.job_id = result[0].id
        return True, result[0]

    def _is_car_owner_existence(self):
        error_free, result = CarOwner.find(phone_number=self.phone_number)
        if not error_free:
            return False, result
        if len(result) == 0:
            return False, UserNotFound(status=404, message=MessagesKeys.ID_IS_NOT_IN_DB, params=None)
        return True, result

    @staticmethod
    def _update_rate(job, rate):
        data = {Keys.RATE: rate}
        return Job.update_by_id(job.id, db, data)

    @staticmethod
    def _limit_rating(job, rate):
        list_of_questions_in_a_question_set = Job.count_questions_in_question_set(job)

        if len(list_of_questions_in_a_question_set) >= len(rate):
            return True, list_of_questions_in_a_question_set
        else:
            return False, RatedBefore(status=404, message=MessagesKeys.JOB_RATED_BEFORE, params=None)

    @staticmethod
    def _is_car_owner_and_his_job_matched(car_owner, job):
        selected_car_owner_id = car_owner[0].id
        session_id = job.car_owner_id
        if selected_car_owner_id == session_id:
            return True, job.id
        else:
            return False, JobAndCarOwnerNotMatch(status=404, message=MessagesKeys.JOB_AND_CAR_OWNER_ARE_NOT_MATCH,
                                                 params=None)

    @staticmethod
    def _is_job_finished(job):
        if Job.is_job_finished() == job.status_id:
            return True, job
        else:
            return False, NotFinishedJob(status=404, message=MessagesKeys.JOB_IS_NOT_FINISHED, params=None)

    @staticmethod
    def _is_rated_before(job):
        rate_of_job = job.rate
        if len(rate_of_job) == 0:
            return True, job
        else:
            return False, RatedBefore(status=404, message=MessagesKeys.JOB_RATED_BEFORE, params=None)

    def _check_rate_range(self):
        range_rate = []
        true_rate = []
        if self.rate[1] is None:
            if -2 <= self.rate[0] <= 2:
                range_rate.append(self.rate[0])
                for rates in self.rate[1:]:
                    if rates is None:
                        range_rate.append(rates)
                if len(range_rate) < len(self.rate):
                    return False, BadRangRate(status=404, message=MessagesKeys.BAD_RANGE_RATE, params=None)
                else:
                    return True, self.rate

        elif self.rate[0] == 2:
            for rate in self.rate:
                if rate == 2:
                    range_rate.append(rate)
            if len(range_rate) < len(self.rate):
                return False, BadRangRate(status=404, message=MessagesKeys.BAD_RANGE_RATE, params=None)
            else:
                return True, self.rate

        else:
            for point in self.rate:
                if -2 <= point <= 2:
                    true_rate.append(point)

            if len(true_rate) < len(self.rate):
                return False, BadRangRate(status=404, message=MessagesKeys.BAD_RANGE_RATE, params=None)
            else:
                return True, self.rate
