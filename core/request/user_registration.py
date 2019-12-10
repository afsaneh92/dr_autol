#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.interfaces.serialization import Serializable
from core.messages.keys import Keys
from core.request.base_request import RequestBaseClass
from core.validation.helpers import password_regex_checker, phone_number_regex_checker, name_regex_checker


class UserRegistrationRequest(RequestBaseClass):

    def __init__(self, json_obj):
        self.name = None
        self.password = None
        self.phone_number = None
        self.user_type = None
        self.reg_id = None
        self.json_obj = json_obj

    def validate_pattern(self):
        invalid_params = []

        result = self._password_checker(self.password)
        if not result[0]:
            invalid_params.append(result[1])
        result = self._phone_number_checker(self.phone_number)
        if not result[0]:
            invalid_params.append(result[1])
        result = self._name_checker(self.name)
        if not result[0]:
            invalid_params.append(result[1])

        if len(invalid_params) > 0:
            return False, {"invalid_params": invalid_params}
        return True, "regex is valid"

    def _password_checker(self, password):
        return password_regex_checker(password)

    def _phone_number_checker(self, phone_number):
        return phone_number_regex_checker(phone_number)

    def _name_checker(self, name):
        return name_regex_checker(name)

    @staticmethod
    def pre_deserialize(json_dict):
        """
        before deserializing, run this method. It is pre-conditions
        :param json_dict:
        :return:
        """
        missed_params = []
        if 'name' not in json_dict:
            missed_params.append("missing_name_in_json")
        if 'password' not in json_dict:
            missed_params.append("missing_password_in_json")
        if 'phone_number' not in json_dict:
            missed_params.append("missing_phone_number_in_json")
        if Keys.REG_ID not in json_dict:
            missed_params.append("missing_reg_id_in_json")
        if len(missed_params) > 0:
            return False, {"missed_params": missed_params}

        return True,

    def post_deserialize(self):
        return self.validate_pattern()

    def deserialize(self):
        if not type(self.json_obj) is dict:
            json_dict = Serializable.convert_input_to_dict(self.json_obj)
        else:

            json_dict = self.json_obj
        result = UserRegistrationRequest.pre_deserialize(json_dict)
        if result[0]:
            self.name = json_dict['name']
            self.password = json_dict['password']
            self.phone_number = json_dict['phone_number']
            # self.user_type = json_dict['user_type']
            self.reg_id = json_dict[Keys.REG_ID]
            result_pattern = self.post_deserialize()
            if not result_pattern[0]:
                return result_pattern
            return True, self
        return result
