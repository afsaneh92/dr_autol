# !/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import unittest

from app import app, db
from config import DataBaseConfig
from core.messages.keys import Keys
from routers.business_owner import business_owner
from routers.endpoints import Endpoints
from routers.index import index_route
from test_cases.fill_db import init_db


class ListBOJobs(unittest.TestCase):
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
        app.register_blueprint(business_owner)

        self.app = app.test_client()

        # db.create_all()
        if self._testMethodName == "test_no_db":
            db.drop_all()
        else:
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

    def _get_list_jobs(self, url, data):
        json_obj = json.dumps(data)

        response = self.app.get(url, data=json_obj, content_type='application/json')
        print(response.data)
        return response

    def _test_list_jobs_request(self, data, expected_response, expected_params_length):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self._get_list_jobs(Endpoints.BUSINESS_OWNER_JOBS + '/' + str(data[Keys.BUSINESS_OWNER_ID]),
                                           data)
            response_dict = json.loads(response.data)
            self.assertEqual(expected_response, response.status_code)
            if self._testMethodName != "test_no_db" and self._testMethodName != "test_bad_schema":
                self.assertEqual(expected_params_length, len(response_dict[Keys.PARAMS]))

    def test_list_jobs_successfully(self):
        data = {
            Keys.BUSINESS_OWNER_ID: 1
        }
        self._test_list_jobs_request(data, 200, 1)

    def test_list_zero_jobs_successfully(self):
        data = {
            Keys.BUSINESS_OWNER_ID: 7
        }
        self._test_list_jobs_request(data, 200, 0)

    def test_no_db(self):
        data = {
            Keys.BUSINESS_OWNER_ID: 1
        }
        self._test_list_jobs_request(data, 500, 6)

    def test_bad_schema(self):
        data = {
            Keys.BUSINESS_OWNER_ID: 'should be integer'
        }
        self._test_list_jobs_request(data, 400, 5)


if __name__ == '__main__':
    unittest.main()
