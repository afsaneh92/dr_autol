#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from flask import json, session

from app import db, app
from config import DataBaseConfig
from core.messages.keys import Keys
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
        res = self.app.post(Endpoints.LOGIN_IWS, data=data,
                            content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
        return res

    def test_login_true(self):
        data = {
            "phone_number": "09125200100",
            "password": "Amish1234",
            "reg_id": "9888",
            "os": "android"
        }
        BO = User(phone_number="09125200113", password="Amish1234", name='aaffA1298', validate=True)
        result = BO.add(db)
        data = json.dumps(data)
        with self.app as client:
            # with client.session_transaction() as sess:
            #     sess['user_id'] = 1
            response = self.make_post_request(data)
            dct = json.loads(response.data)
            self.assertEqual(dct['status'], 200)
            self.assertEqual(session['logged_in'], True)

    def test_login_false_regex(self):
        data = {
            "phone_number": "09125200100",
            "password": "Amish",
            "reg_id": "9888",
            "os": "android"
            # "name": "امیر",
            # "user_type": "1"
        }
        data = json.dumps(data)
        with self.app as client:
            # with client.session_transaction() as sess:
            #     sess['user_id'] = 1
            response = self.make_post_request(data)
            dct = json.loads(response.data)
            self.assertEqual(dct['status'], 400)

    def test_login_not_registered(self):
        data = {
            "phone_number": "09125200113",
            "password": "Amish1234",
            "reg_id": "9888",
            "os": "android"
            # "name": "امیر",
            # "user_type": "1"
        }
        data = json.dumps(data)
        with self.app as client:
            # with client.session_transaction() as sess:
            #     sess['user_id'] = 1
            response = self.make_post_request(data)
            dct = json.loads(response.data)
            self.assertEqual(dct['status'], 404)


if __name__ == '__main__':
    unittest.main()
