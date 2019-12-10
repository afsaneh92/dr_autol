#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from flask import json, session

from app import db, app
from config import DataBaseConfig
from core.messages import HttpStatus
from core.messages.keys import Keys
from persistence.database.entity.user.supplier import Supplier
from persistence.database.entity.user.user import User
from routers.authintication import authentication
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
            # pass
            init_db()

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
        res = self.app.post(Endpoints.LOGIN, data=data,
                            content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
        return res

    def test_login_true_iws(self):
        data = {
            Keys.PHONE_NUMBER: "09125200200",
            Keys.PASSWORD: "Amish1234",
            Keys.REG_ID: "9888",
            Keys.OS: "android",
            Keys.USER_TYPE: Keys.CAR_OWNER
        }
        data1 = json.dumps(data)
        with self.app as client:
            response = self.make_post_request(data1)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], HttpStatus.OK)
            self.assertEqual(session[Keys.PHONE_NUMBER], data[Keys.PHONE_NUMBER])

    def test_login_true_supplier(self):
        data = {
            Keys.PHONE_NUMBER: "09125200112",
            Keys.PASSWORD: "Amish1234",
            Keys.USER_TYPE: Keys.SUPPLIER
        }
        data1 = json.dumps(data)
        with self.app as client:
            response = self.make_post_request(data1)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], HttpStatus.OK)
            self.assertEqual(session[Keys.PHONE_NUMBER], data[Keys.PHONE_NUMBER])

    def test_login_false_regex(self):
        data = {
            Keys.PHONE_NUMBER: "09125200100",
            Keys.PASSWORD: "Amish",
            Keys.REG_ID: "9888",
            Keys.OS: "android",
            Keys.USER_TYPE: Keys.CAR_OWNER
        }
        data = json.dumps(data)
        with self.app as client:
            response = self.make_post_request(data)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], HttpStatus.BAD_REQUEST)
            self.assertEqual(Keys.PHONE_NUMBER in session, False)

    def test_login_not_registered(self):
        data = {
            Keys.PHONE_NUMBER: "09125200113",
            Keys.PASSWORD: "Amish1234",
            Keys.REG_ID: "9888",
            Keys.OS: "android",
            Keys.USER_TYPE: Keys.CAR_OWNER
        }
        data = json.dumps(data)
        with self.app as client:
            response = self.make_post_request(data)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], HttpStatus.NOT_FOUND)
            self.assertEqual(Keys.PHONE_NUMBER in session, False)


if __name__ == '__main__':
    unittest.main()
