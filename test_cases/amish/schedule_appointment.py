#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import unittest


from app import  app
from config import DataBaseConfig
from core.messages.keys import Keys

from routers.admin import admin
from routers.authintication import authentication
from routers.car_owner import car_owner
from routers.choose_services import choose_service_grade
from routers.endpoints import Endpoints
from routers.index import index_route
from test_cases.fill_db import init_db


class SetAnAppointmentTest(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        POSTGRES = {
            'user': 'postgres',
            'pw': 'postgres',
            'db': 'dr-autol-test',
            'host': 'localhost',
            'port': '5432',
        }
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

    def _post_request(self, url, data):
        json_obj = json.dumps(data)
        response = self.app.post(url, data=json_obj, content_type='application/json')
        print(response.data)
        return response

    def _test_search_iws(self, data, expected_response):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = True
            response = self._post_request(Endpoints.CAR_OWNER_SET_APPOINTMENT, data)
            print(response)
            self.assertEqual(expected_response, response.status_code)

    def test_set_appointment(self):
        data = {
            Keys.USER_TYPE: 'auto_service_job',
            "job": {
                "car_owner": 1,
                "business_owner": 1,
                "car_id": 1,
                "car_problem": {
                    Keys.SERVICE_GRADE: "Common",
                    Keys.SERVICE_CATEGORY: "AutoService",
                    Keys.SERVICE_DEFINITIONS: {
                        Keys.PRODUCTABLE_ITEMS: {1: 1, 2: 1},
                        Keys.NON_PRODUCTABLE_ITEMS: [1]
                    },
                },
                Keys.START_SCHEDULE: "2018-06-06 18:30:33"
            }
        }
        self._test_search_iws(data, 200)


if __name__ == '__main__':
    unittest.main()
