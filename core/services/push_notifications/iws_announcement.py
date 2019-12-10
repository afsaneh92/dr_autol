#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.messages.keys import Keys
from core.result import Result
from core.services.push_notifications.new_request import PushNotification
from persistence.database.entity.car import Car
from persistence.database.entity.user.user import User


class IWSAnnouncement(object):
    @staticmethod
    def request_notification(car_problems, business_owner_id, car_id, job_id, time):
        business_owner = User.load_user_reg_id(business_owner_id)
        car = Car.load_car(car_id)
        message = IWSAnnouncement.message_creator(car.name,car_problems, time)
        service_types = IWSAnnouncement.service_type_creator(car_problems)
        data = {
            'info': {
                Keys.CAR_INFO: {Keys.NAME: car.name},
                Keys.PROBLEM: {
                    Keys.GRADE: car_problems[0].services_definition.service_grade,
                    Keys.TYPES: service_types,
                    Keys.JOB_ID: job_id,
                },
                Keys.USER_TYPE: Keys.NEW_JOB_REQUEST,
            },
            Keys.ACTIONS: Result.language.ACCEPT_DENY_ACTIONS,
            Keys.MESSAGE: message,
            Keys.TITLE: Result.language.NEW_REQUEST_NOTIFICATION_TITLE,



            Keys.BUSINESS_OWNER: {
                Keys.NAME: business_owner.name,
                Keys.REG_ID: business_owner.reg_id
            }
        }
        response = PushNotification.push(data[Keys.BUSINESS_OWNER][Keys.REG_ID], data)
        return response

    @staticmethod
    def cancel_job(job):
        business_owner = User.load_user_reg_id(job.business_owner_id)
        car = Car.load_car(job.car_id)
        info = {
            Keys.USER_TYPE: Keys.CANCEL_JOB,
            Keys.CAR_INFO: {Keys.NAME: car.name},
            Keys.BUSINESS_OWNER: {
                Keys.NAME: business_owner.name,
                Keys.REG_ID: business_owner.reg_id
            }
        }
        response = PushNotification.push([info[Keys.BUSINESS_OWNER][Keys.REG_ID]], info)
        return response

    @staticmethod
    def message_creator(name, car_problems, time):
        msg = name + " "
        for car_problem in car_problems:
            msg += car_problem.services_definition.service_type.name + u" و "
        last_and = msg.rfind(u'و')
        msg = msg[:last_and] + u" " + time
        return msg

    @staticmethod
    def send_payment_result_notification(car, business_owner):
        info = {
            Keys.USER_TYPE: Keys.PAYMENT_JOB,
            Keys.CAR_INFO: {Keys.NAME: car.auto_type_.name, Keys.PLATE_NUMBER: car.plate_number},
            Keys.BUSINESS_OWNER: {
                Keys.NAME: business_owner.name,
                Keys.REG_ID: business_owner.reg_id
            }
        }
        response = PushNotification.push([info[Keys.BUSINESS_OWNER][Keys.REG_ID]], info)
        return response

    @staticmethod
    def service_type_creator(car_problems):
        service_types = []
        for car_problem in car_problems:
            message = car_problem.services_definition.service_type.name
            if car_problem.consumable_item is not None:
                message += " " + car_problem.consumable_item.product_name + " " + car_problem.consumable_item.product_name

            service_types.append(message)
        return service_types
