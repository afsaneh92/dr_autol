#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
9 (9) As a car owner I want to choose a service(common, plus, premium) So that my car needs to fix
"""

import json
import unittest

from app import db, app
from config import DataBaseConfig
from routers.admin import admin
from routers.authintication import authentication
from routers.car_owner import car_owner
from routers.choose_services import choose_service_grade
from routers.endpoints import Endpoints
from routers.index import index_route
from test_cases.fill_db import init_db
from utilities import calculate_duration, calculate_finish_schedule


class ChooseServiceGradeTest(unittest.TestCase):
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

    # success scenario

    def _post_request(self, url, data):
        json_obj = json.dumps(data)
        response = self.app.post(url, data=json_obj, content_type='application/json')
        print(response.data)
        return response

    def _test_search_iws(self, data, expected_response):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['logged_in'] = True
            response = self._post_request(Endpoints.LIST_IWS_BY_SEARCH, data)
            print(response)
            self.assertEqual(expected_response, response.status_code)

    def test_search_iws_some_result(self):
        data = {
            "grade_id": "Common",
            "options": {
                # "region": [{'lat': 36.6830, 'lng': 48.5087}, {'lat': -77.0364, 'lng': 38.8951},
                #            {'lat': 36.2605, 'lng': 59.6168}, {'lat': 36.6830, 'lng': 48.5087}],
                # "name": "Changizi",
                "type": [3],
                "start_schedule": "2019-03-05 16:35:00"
            }
        }
        self._test_search_iws(data, 200)

    def test_search_iws_zero_result(self):
        data = {
            "grade_id": 100,
            "options": {
                "region": [{'lat': "36.6830", 'lng': 48.5087}, {'lat': -77.0364, 'lng': 38.8951},
                           {'lat': 36.2605, 'lng': 59.6168}, {'lat': 36.6831, 'lng': 48.5087}],
                "name": "Ahmad"
            }
        }
        self._test_search_iws(data, 400)

    def test_search_iws_bad_request_name(self):
        data = {
            "grade_id": 1,
            "options": {
                "region": [52, 65],
                "name": 54
            }
        }
        self._test_search_iws(data, 400)

    def test_search_iws_bad_request_no_grade(self):
        data = {
            "options": {
                "region": [52, 65],
                "name": "فقط اف جی"
            }
        }
        self._test_search_iws(data, 400)

    def test_search_iws_bad_request_no_type_array(self):
        data = {
            "grade_id": 2,
            "options": {
                "region": [{'lat': 10, 'lng': 20}, {'lat': 10, 'lng': 20}, {'lat': 10, 'lng': 20}],
                "name": "فقط اف جی",
                "type": 1
            }
        }
        self._test_search_iws(data, 400)

    def test_search_iws_no_filter(self):
        data = {
            "grade_id": 1,
            "options": {
                "type": [3, 5, 2, 1]
            }
        }
        self._test_search_iws(data, 200)

    def test_only_region(self):
        data = {
            "grade_id": 2,
            "options": {
                "region": [{'lat': 36.6830, 'lng': 48.5087}, {'lat': -77.0364, 'lng': 38.8951},
                           {'lat': 36.2605, 'lng': 59.6168}, {'lat': 36.6830, 'lng': 48.5087}],
            }
        }
        self._test_search_iws(data, 200)

    def test_calculate_duration(self):
        _, duration = calculate_duration([1, 2])
        self.assertEqual(30, duration)

    def test_calculate_finish_schedule(self):
        start = "2018-03-06 12:25:00"
        finish = calculate_finish_schedule(start, 24 * 60)
        self.assertEqual("2018-03-07 12:25:00", finish)


if __name__ == '__main__':
    unittest.main()
