#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import global_logger
from core.controller import BaseController
from core.messages.translator.messages_keys import MessagesKeys
from core.result.success.success_in_qeue_jobs import SuccessInQueueJobs
from persistence.database.entity.job_.job import Job

logger = global_logger


class ListJobsByStatusController(BaseController):
    def __init__(self, business_owner, status, converter):
        self.business_owner = business_owner
        self.status_list = status
        self.converter = converter

    def execute(self):
        job_list = self.load_jobs()
        dct = job_list.dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    def load_jobs(self):
        error_free, results = Job.load_jobs_by_statuses_for_business_owner(business_owner=self.business_owner,
                                                                           statuses=self.status_list)
        if not error_free:
            return results
        return SuccessInQueueJobs(status=200, message=MessagesKeys.SUCCESS_IN_QUEUE_JOBS, params=results)
