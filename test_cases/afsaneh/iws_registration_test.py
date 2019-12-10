#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import unittest

from flask import json

from app import db, app
from config import DataBaseConfig
from core.messages.keys import Keys
# from persistence.database.entity.business_owner import BusinessOwner
from core.controller.iws_registration import IwsRegistrationController
from core.request.iws_register_request import IWSRegisterRequest
from persistence.database.entity.user.user import User
from routers.authintication import authentication
from routers import admin
from routers.endpoints import Endpoints
from test_cases.fill_db import init_db


class MyTestCase(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config[
            'SQLALCHEMY_DATABASE_URI'] = DataBaseConfig.DB_DIALECT + DataBaseConfig.USER_NAME + ':' + DataBaseConfig.PASSWORD + '@' + DataBaseConfig.SERVER_ADDRESS + ':' + DataBaseConfig.PORT + '/' + DataBaseConfig.DATABASE_NAME
        app.register_blueprint(authentication)

        self.app = app.test_client()
        if self._testMethodName == "test_no_db":
            db.drop_all()

        # db.drop_all()
        # db.create_all()
        else:
            pass
            # init_db()

    # executed after each test
    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def make_post_request(self, data):
        res = self.app.post(Endpoints.REGISTER_IWS, data=data,
                            content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
        return res

    def test_registration_false_regex_1(self):
        data = {
            "phone_number": "32113222222",
            "password": "Amish1234",
            "reg_id": "9888",
            "name": "ابببسیسث"
        }
        data = json.dumps(data)
        response = self.make_post_request(data)
        dct = json.loads(response.data)
        self.assertEqual(response.status_code, 400)

    def test_registration_false_regex_2(self):
        data = {
            "phone_number": "09888888888",
            "name": "ابببسیسث",
            "password": "khsss",
            "reg_id": "9888",
            "user_type": "iws owner"
        }
        data = json.dumps(data)
        response = self.make_post_request(data)
        dct = json.loads(response.data)
        self.assertEqual(response.status_code, 400)

    def test_iws_registration_regisered(self):
        data = {
            "phone_number": "09125200100",
            "name": "ابببسیسث",
            "password": "Amish1234",
            "user_type": "iws owner",
            "reg_id": "9888"

        }
        BO = User(phone_number="09125200100", password="Amish1234", name='aaffA1298', validate=True)
        result = BO.add(db)
        data = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            data = json.dumps(data)
            response = self.make_post_request(data)
            dct = json.loads(response.data)
            self.assertEqual(response.status_code, 404)

    def test_add_user_true(self):
        data = {
            "phone_number": "09120000002",
            "password": "Amish1234",
            "name": "امیر",
            "reg_id": "9888",
            "user_type": "AutoService1",
        }
        json_obj = json.dumps(data)
        response = self.app.post('/register/iws', data=json_obj, content_type='application/json')
        # response = self.app.get('/car_owner/cars', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
