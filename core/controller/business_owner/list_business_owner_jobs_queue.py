#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import global_logger
from core.controller import BaseController
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result.success.success_in_qeue_jobs import SuccessInQueueJobs
from persistence.database.entity.job_.job import Job

logger = global_logger


class JobsQueueListController(BaseController):

    def __init__(self, business_owner, converter):
        self.business_owner = business_owner
        self.converter = converter

    def execute(self):
        result_find_job = self._load_jobs_in_queue()
        dct = result_find_job[1].dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    def _load_jobs_in_queue(self):
        error_free, results = Job.load_jobs_by_statuses_for_business_owner(self.business_owner,
                                                                           [Keys.STATUS_ACCEPTED_BY_BUSINESS_OWNER])
        if not error_free:
            return results
        return SuccessInQueueJobs(status=200, message=MessagesKeys.SUCCESS_IN_QUEUE_JOBS, params=results)
