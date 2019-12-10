#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from core.controller import BaseController
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.messages.translator.situations import ReflectionControllers
from core.result.failure.not_found_job import JobNotFound
from core.validation.helpers import create_class_dynamically

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class JobBaseController(BaseController):
    dct = {
        Keys.AUTO_SERVICE_JOB_REQUEST: ReflectionControllers.AUTO_SERVICE_JOB_CONTROLLER,
        Keys.INSURANCE_JOB_REQUEST: ReflectionControllers.INSURANCE_JOB_CONTROLLER,
    }

    def __init__(self, job, type_, converter):
        self.job = job
        self.type_ = type_
        self.converter = converter

    def execute(self):
        ret = self.generate_appropriate_controller()
        if not ret[0]:
            dct = ret[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)
        klass = ret[1](self.job, self.converter)
        return klass.execute()

    @staticmethod
    def child_class_deserialize(req, json_dict):
        result = req.deserialize(json_dict)
        if result[0]:
            return result[0], result[1], json_dict[Keys.USER_TYPE]
        return result

    def generate_appropriate_controller(self):
        type_ = JobBaseController.dct[self.type_]
        return create_class_dynamically(logger, type_['module'], type_['class'], self.type_)

    @staticmethod
    def is_exist(job):
        result = True,
        if job is None:
            result = False, JobNotFound(status=404, message=MessagesKeys.NOT_FOUND_JOB)
        else:
            result = True,
        return result
