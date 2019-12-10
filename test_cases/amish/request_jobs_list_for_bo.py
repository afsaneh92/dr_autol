# !/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import unittest

from app import app
from config import DataBaseConfig
from core.messages.keys import Keys
from routers.business_owner import business_owner
from routers.endpoints import Endpoints
from routers.index import index_route
from test_cases.fill_db import init_db


class RequestJobsListForBO(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config[
            'SQLALCHEMY_DATABASE_URI'] = DataBaseConfig.generate_database_uri()
        app.register_blueprint(index_route)
        app.register_blueprint(business_owner)

        self.app = app.test_client()
        init_db()

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def _start_request(self, url, data):
        json_obj = json.dumps(data)

        response = self.app.post(url, data=json_obj, content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
        print(response.data)
        return response

    def _test_list_job_request(self, data, expected_response, expected_params=None, expected_stat=8):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self._start_request(Endpoints.LIST_JOBS_FOR_BUSINESS_OWNER, data)
            response_dict = json.loads(response.data)
            self.assertEqual(expected_response, response.status_code)
            return response_dict
    def test_list_with_length_0(self):
        data = {
            Keys.STATUS: [Keys.STATUS_PENDING],
        }
        response_dict = self._test_list_job_request(data, 200)
        self.assertEqual(0, len(response_dict['params']))

    def test_list_with_length_1(self):
        data = {
            Keys.STATUS: [Keys.STATUS_DONE],
        }
        response_dict = self._test_list_job_request(data, 200)
        self.assertEqual(1, len(response_dict['params']))

    def test_list_accepted(self):
        data = {
            Keys.STATUS: [Keys.STATUS_ACCEPTED_BY_BUSINESS_OWNER],
        }
        response_dict = self._test_list_job_request(data, 200)
        self.assertEqual(2, len(response_dict['params']))


if __name__ == '__main__':
    unittest.main()
