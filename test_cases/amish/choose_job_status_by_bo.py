# !/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import random
import unittest

from app import app, db
from config import DataBaseConfig
from core.messages.keys import Keys
from core.result import Result
from persistence.database.entity.job_.job import Job
from routers.business_owner import business_owner
from routers.endpoints import Endpoints
from routers.index import index_route
from test_cases.fill_db import init_db


class ChooseAcceptDenyByBO(unittest.TestCase):
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

    def _put_accept_request(self, url, data):
        json_obj = json.dumps(data)

        response = self.app.put(url, data=json_obj, content_type='application/json')
        print(response.data)
        return response

    def _put_deny_request(self, url, data):
        json_obj = json.dumps(data)
        response = self.app.put(url, data=json_obj, content_type='application/json')
        print(response.data)
        return response

    def _test_choose_job_request(self, data, expected_response, expected_message, expected_stat_id,
                                 expected_params=None):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self._put_accept_request(Endpoints.BUSINESS_OWNER_JOB_REQUEST, data)
            response_dict = json.loads(response.data)
            self.assertEqual(expected_response, response.status_code)
            self.assertEqual(expected_message, response_dict[Keys.MESSAGE])
            if expected_params is not None:
                self.assertEqual(expected_params, response_dict[Keys.PARAMS])
            if self._testMethodName != "test_no_db" and self._testMethodName != "test_no_job" and self._testMethodName != "test_bad_schema":
                actual_stat = Job.query.filter(Job.id == data[Keys.JOB_ID]).with_entities(Job.status_id).first()[0]
                self.assertEqual(expected_stat_id, actual_stat)

    def test_accept_job_successfully(self):
        data = {
            Keys.USER_TYPE: 'accept',
            Keys.JOB_ID: 1
        }
        self._test_choose_job_request(data, 200, Result.language.SUCCESS_ACCEPT_JOB, 5)

    def test_deny_job_successfully(self):
        data = {
            Keys.USER_TYPE: 'deny',
            Keys.JOB_ID: 1
        }
        self._test_choose_job_request(data, 200, Result.language.SUCCESS_DENY_JOB, 6)

    def test_no_db(self):
        arr = ['deny', 'accept']
        rand = random.randint(0, 1)
        data = {
            Keys.USER_TYPE: arr[rand],
            Keys.JOB_ID: 1
        }
        self._test_choose_job_request(data, 500, Result.language.SOMETHING_WENT_WRONG, 6)

    def test_no_job(self):
        arr = ['deny', 'accept']
        rand = random.randint(0, 1)
        data = {
            Keys.USER_TYPE: arr[rand],
            Keys.JOB_ID: 11
        }
        self._test_choose_job_request(data, 404, Result.language.NOT_FOUND_JOB, 6)

    def test_bad_schema(self):
        data = {
            Keys.JOB: 'bad',
            Keys.JOB_ID: 1
        }
        self._test_choose_job_request(data, 400, 'bad schema', 5)

    def test_cancel_job_successfully(self):
        data = {
            Keys.USER_TYPE: Keys.CANCEL_JOB_BY_BUSINESS_OWNER_REQUEST,
            Keys.JOB_ID: 1
        }
        self._test_choose_job_request(data, 200, Result.language.SUCCESS_START_JOB, 4)


if __name__ == '__main__':
    unittest.main()
