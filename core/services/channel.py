#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import random

from core.services.sms_handler.kandu import Kandu


class CodeValidationChannel:
    __metaclass__ = ABCMeta
    name = ""
    destination = ""
    message = ""

    def __init__(self, name, destination, message):
        pass

    @abstractmethod
    def send_validation_code(self):
        pass

    @abstractmethod
    def create_validation_code(self):
        pass

    @staticmethod
    def create_random_code():
        return random.randint(1000, 10000)


class SMSCodeValidation(CodeValidationChannel):
    def __init__(self, name, destination, code):
        self.name = name
        self.destination = destination
        self.code = code
        # self.user_id = user_id

    def create_validation_code(self):
        return self.create_random_code()

    def send_validation_code(self):
        Kandu.send_sms(self.destination, self.name + u' عزیز ' + u'کد شما: ' + str(self.code))
        # print("send a sms to" + self.name + " " + self.destination)
        # # code = self.create_validation_code()
        # # print "code is: " + str(self.message)
        # # try:
        # #
        # # except:

        return False, self.code


class EmailCodeValidation(CodeValidationChannel):
    def __init__(self, name, destination, message):
        self.name = name
        self.destination = destination
        self.message = message

    def send_validation_code(self):
        print("send an email to" + self.name + " " + self.destination)
        return False

    def create_validation_code(self):
        return self.create_random_code()
