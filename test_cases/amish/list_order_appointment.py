#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
9 (9) As a car owner I want to choose a service(common, plus, premium) So that my car needs to fix
"""

import json
import unittest

from app import app
from config import DataBaseConfig
from routers.admin import admin
from routers.authintication import authentication
from routers.car_owner import car_owner
from routers.choose_services import choose_service_grade
from routers.index import index_route
from test_cases.fill_db import init_db


class ListOrderAppointmentTest(unittest.TestCase):
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

    def _get_request(self, url):
        response = self.app.get(url, content_type='application/json')
        print(response.data)
        return response

    # success scenario

    def _test_list_car_owner_orders(self, expected_response):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self._get_request('/car_owner/jobs/2')
            print(response)
            dct = json.loads(response.data)
            self.assertEqual(expected_response, len(dct["param"]))

    def test_list_job_order_(self):
        self._test_list_car_owner_orders(1)


if __name__ == '__main__':
    unittest.main()
