#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
9 (9) As a car owner I want to choose a service(common, plus, premium) So that my car needs to fix
"""

import json
import unittest


from app import db, app
from config import DataBaseConfig
from persistence.database.entity.base import encode_auth_token, decode_auth_token
from persistence.database.entity.service_grade import ServiceGrade
from persistence.database.entity.service_type import ServiceType
from routers.admin import admin
from routers.authintication import authentication
from routers.car_owner import car_owner
from routers.choose_services import choose_service_grade
from routers.index import index_route
from test_cases.fill_db import init_db


class RegistersTest(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config[
            'SQLALCHEMY_DATABASE_URI'] = DataBaseConfig.DB_DIALECT + DataBaseConfig.USER_NAME + ':' + DataBaseConfig.PASSWORD + '@' + DataBaseConfig.SERVER_ADDRESS + ':' + DataBaseConfig.PORT + '/' + DataBaseConfig.DATABASE_NAME
        app.register_blueprint(index_route)
        app.register_blueprint(car_owner)
        app.register_blueprint(authentication)
        app.register_blueprint(admin)
        app.register_blueprint(choose_service_grade)

        self.app = app.test_client()

        # db.drop_all()
        init_db()

        # Disable sending emails during unit testing
        # self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    # success scenario

    def test_encode_decode(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'my_precious')
        auth_token = encode_auth_token(10)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(decode_auth_token(auth_token) == 10)


        # list_returned = ServiceGrade.list_service_grades()
        # list_returned1 = ServiceGrade.list_service_grades()
        # self.assertEqual(list_returned[1], list_returned[1])


if __name__ == '__main__':
    unittest.main()
