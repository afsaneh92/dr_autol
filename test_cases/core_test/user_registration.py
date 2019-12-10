#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest

from app import db
from core.request.user_registration import UserRegistrationRequest
from core.services.channel import *


class UserRegistrationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_code_validation_request(self):
        from core.request.code_validation import CodeValidationRequest
        user_request = {
            "phone_number": "09372943761",
            "name": "maind22@amir.com",
            "password": "123",
            "code": "register_car_owner_user"
        }

        json_obj = json.dumps(user_request)

        code_obj = CodeValidationRequest(json_obj)
        res = code_obj.deserialize()
        self.assertEqual(False, res[0])

        user_request = {
            "phone_number": "09372943761",
            "code": "1234asd"
        }

        json_obj = json.dumps(user_request)

        code_obj = CodeValidationRequest(json_obj)
        res = code_obj.deserialize()
        self.assertEqual(False, res[0])

        user_request = {
            "phone_number": "09372943761",
            "code": "4563"
        }

        json_obj = json.dumps(user_request)

        code_obj = CodeValidationRequest(json_obj)
        res = code_obj.deserialize()
        self.assertEqual(True, res[0])

    def test_user_registration_request(self):
        user_request = {
            "phone_number": "09372943761",
            "name": "maind22@amir.com",
            "password": "123",
            "__request_type__": "register_car_owner_user"
        }

        json_obj = json.dumps(user_request)

        user = UserRegistrationRequest(json_obj)
        res = user.deserialize()

        self.assertEqual(False, res[0])

        user_request = {
            "phone_number": "09372943761",
            "name": "amir@iws.com",
            "password": "123Amish3",
            "user_type": 'car_owner'
        }

        json_obj = json.dumps(user_request)

        user = UserRegistrationRequest(json_obj)
        res = user.deserialize()

        self.assertEqual(res[0], False)

        user_request = {
            "phone_number": "0937294376",
            "name": "amir@iws.com",
            "password": "123Amish3",
            "user_type": 'car_owner'
        }

        json_obj = json.dumps(user_request)

        user = UserRegistrationRequest(json_obj)
        res = user.deserialize()
        self.assertEqual(res[0], False)

        user_request = {
            "phone_number": "0937294376",
            "name": "amir@iws.com",
            "password": "1232",
            "user_type": 'car_owner'
        }

        json_obj = json.dumps(user_request)

        user = UserRegistrationRequest(json_obj)
        res = user.deserialize()
        self.assertEqual(res[0], False)

        user_request = {
            "phone_number": "09372943761",
            "name": "امیر شعبانی",
            "password": "123Amish3",
            "user_type": 'car_owner'
        }

        json_obj = json.dumps(user_request)

        user = UserRegistrationRequest(json_obj)
        res = user.deserialize()
        self.assertEqual(res[0], True)

    def test_register_user_in_database(self):
        from persistence.database.entity.car_owner import CarOwners
        from persistence.database.entity.car import Car
        user_request = {
            "phone_number": "09124274836",
            "name": "امیر شعبانی",
            "password": "123Amish3",
            "user_type": 'car_owner'
        }

        json_obj = json.dumps(user_request)

        user = UserRegistrationRequest(json_obj)
        res = user.deserialize()
        user = res[1]

        user = CarOwners(name=user.name, phone_number=user.phone_number, code="1234", user_type='1',
                         password=user.password)
        if user.is_registered():
            self.assertEqual(True, user.is_registered())
        if user.is_valid():
            pass

        if user.is_registered():
            if user.is_valid():
                print("dadach ghablan sabte nam kardi")
            elif user.is_invalid():
                rand = random.randint(1000, 10000)
                dct = {"code": str(rand)}
                user.update(db, dct)
        else:
            db.session.add(user)
            db.session.commit()
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
