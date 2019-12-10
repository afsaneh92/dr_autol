# !/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import unittest

from app import app
from core.messages.keys import Keys
from routers.admin import admin
from routers.endpoints import Endpoints
from routers.index import index_route


class StartAJob(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.register_blueprint(index_route)
        app.register_blueprint(admin)

        self.app = app.test_client()

    # executed after each test
    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def _start_request(self, url):
        response = self.app.get(url, content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
        print(response.data)
        return response

    def _test_start_job_request(self, expected_status, need_update, app_name, version):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self._start_request(Endpoints.FORCE_UPDATE + "/" + app_name + "/" + version)
            response_dict = json.loads(response.data)
            self.assertEqual(expected_status, response.status_code)
            self.assertEqual(need_update, response_dict['params'])

    def test_car_owner_do_not_need_update(self):
        self._test_start_job_request(200, False, 'carowner', '1.1.1')

    def test_car_owner_need_update(self):
        self._test_start_job_request(200, True, 'carowner', '0.9')


if __name__ == '__main__':
    unittest.main()
