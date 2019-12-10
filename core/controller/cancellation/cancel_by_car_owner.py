#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from app import db, global_logger
from core.controller import BaseController
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result.failure.is_not_cancellable import NotCancellable
from core.result.failure.not_found_job import JobNotFound
from core.services.push_notifications.iws_announcement import IWSAnnouncement
from core.validation.helpers import convert_datetime_to_timestamp
from persistence.database.entity.job_.job import Job
from persistence.database.entity.stauts import Status

logger = global_logger


class CancellationByCarOwnerController(BaseController):

    def __init__(self, job, car_owner, converter):
        self.job = job
        self.car_owner = car_owner
        self.converter = converter

    def execute(self):
        result_find_job = self._find_job()
        if not result_find_job[0]:
            dct = result_find_job[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        if result_find_job[1] is None:
            dct = CancellationByCarOwnerController.create_not_found_job_message().dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        self.job = result_find_job[1]
        error_free, result = self.is_job_belongs_to_user()
        if not error_free:
            dct = result.dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        start_timestamp = convert_datetime_to_timestamp(self.job.start_schedule)
        is_cancellable = self.is_cancellable(start_timestamp)
        if not is_cancellable[0]:
            dct = is_cancellable[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        cancellation_result = self.cancel_job()
        if not cancellation_result[0]:
            dct = cancellation_result[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)
        self.push_notification_to_business_owner()

        dct = cancellation_result[1].dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    def _find_job(self):
        return Job.load_job(self.job.id)

    @staticmethod
    def create_not_found_job_message():
        return JobNotFound(status=404, message=MessagesKeys.NOT_FOUND_JOB)

    def is_job_belongs_to_user(self):
        if self.job != self.car_owner:
            return False, JobNotFound
        return True,

    def is_cancellable(self, start_timestamp):
        result = True,
        current = time.time()
        start_timestamp = start_timestamp + (40 * 60)
        if current < start_timestamp:
            return False, NotCancellable(status=400, message=MessagesKeys.IS_NOT_CANCELLABLE)
        return result

    def cancel_job(self):
        status = Status.query.filter(Status.name == Keys.STATUS_CANCELLED_BY_BUSINESS_OWNER).first()
        data = {Keys.STATUS_ID: status.id}
        return Job.cancel_job(self.job, data, db)

    def push_notification_to_business_owner(self):
        IWSAnnouncement.cancel_job(self.job)
