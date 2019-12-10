# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
from core.messages.keys import Keys
from core.result import Result
from core.services.push_notifications.new_request import PushNotification
from persistence.database.entity.user.car_owner import CarOwner
from persistence.database.entity.question_to_question_set import QuestionToQuestionSet


class CarOwnerAnnouncement(object):

    @staticmethod
    def accept_job(job):
        car_owner = CarOwner.load_car_owner(job.car_owner_id)
        info = {
            Keys.USER_TYPE: Keys.ACCEPT_JOB_REQUEST,
            Keys.CAR_OWNER: {Keys.NAME: car_owner.name, Keys.REG_ID: car_owner.reg_id},
            Keys.MESSAGE: Result.language.ACCEPT_JOB_BY_BUSINESS_OWNER,
        }

        response = PushNotification.push(info[Keys.CAR_OWNER][Keys.REG_ID], info)
        return response

    @staticmethod
    def deny_job(job):
        car_owner = CarOwner.load_car_owner(job.car_owner_id)
        info = {
            Keys.USER_TYPE: Keys.DENY_JOB_REQUEST,
            Keys.CAR_OWNER: {Keys.NAME: car_owner.name, Keys.REG_ID: car_owner.reg_id},
            Keys.MESSAGE: Result.language.DENY_JOB_BY_BUSINESS_OWNER,

        }
        response = PushNotification.push(info[Keys.CAR_OWNER][Keys.REG_ID], info)
        return response
