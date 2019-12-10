#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
9 (9) As a car owner I want to choose a service(common, plus, premium) So that my car needs to fix
"""

import json
import unittest

from app import app
from config import DataBaseConfig
from core.messages.keys import Keys
from core.result import Result
from routers.admin import admin
from routers.authintication import authentication
from routers.car_owner import car_owner
from routers.choose_services import choose_service_grade
from routers.endpoints import Endpoints
from routers.index import index_route
from test_cases.fill_db import init_db


class CancelAppointmentTest(unittest.TestCase):
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
        # db.create_all()
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

    def _put_request(self, url, data):
        response = self.app.put(url, data=data, content_type='application/json')
        print(response.data)
        return response

    def _test_cancel_job_by_car_owner(self, expected_data, data):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self._put_request(Endpoints.CANCEL_JOB_BY_CAR_OWNER, data=data)
            print(response)
            dct = json.loads(response.data)
            self.assertEqual(expected_data[Keys.STATUS], dct[Keys.STATUS])
            self.assertEqual(expected_data[Keys.MESSAGE], dct[Keys.MESSAGE])
            self.assertEqual(expected_data[Keys.PARAMS], dct[Keys.PARAMS])

    def test_list_job_order_(self):
        data = {
            Keys.JOB_ID: "1"
        }
        json_obj = json.dumps(data)
        expected_data = {Keys.STATUS: 200, Keys.MESSAGE: Result.language.SUCCESS_CANCEL_JOB,
                         Keys.PARAMS: None}
        self._test_cancel_job_by_car_owner(expected_data, json_obj)


if __name__ == '__main__':
    unittest.main()
