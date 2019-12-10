# !/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import unittest

from app import app, db
from config import DataBaseConfig
from core.messages.keys import Keys
from persistence.database.entity.car_problem import CarProblem
from persistence.database.entity.job_.autoservice_job import AutoServiceJob
from persistence.database.entity.job_.job import Job
from persistence.database.entity.stauts import Status
from routers.business_owner import business_owner
from routers.endpoints import Endpoints
from routers.index import index_route
from test_cases.fill_db import init_db


class StartAJob(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
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
        elif self._testMethodName == "test_wrong_status_type":
            pass
        elif self._testMethodName == "test_overlap_in_starting_job":
            data = [
                {"service_type": 3, "service_grade": 1},
                {"service_type": 4, "service_grade": 1},
            ]
            car_problems = []
            for car_problem in data:
                c_p = CarProblem(consumable_item_id=1, services_definition_id=1)
                car_problems.append(c_p)
            status = Status.query.filter(Status.name == Keys.STATUS_START).first()
            job = AutoServiceJob(business_owner_id=1, car_owner_id=1, car_id=2, status_=status,
                      start_schedule="2019-01-05 16:29:45", finish_schedule= "2019-01-07 16:43", price=1236)
            job.car_problems.extend(car_problems)
            db.session.add(job)
            db.session.commit()

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

    def _start_request(self, url, data):
        json_obj = json.dumps(data)

        response = self.app.put(url, data=json_obj, content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
        print(response.data)
        return response

    def _test_start_job_request(self, data, expected_response, expected_params=None, expected_stat=8):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self._start_request(Endpoints.BUSINESS_OWNER_JOB, data)
            response_dict = json.loads(response.data)
            self.assertEqual(expected_response, response.status_code)
            if self._testMethodName != "test_no_db" and self._testMethodName != "test_bad_schema" and self._testMethodName != "test_wrong_status_type" and self._testMethodName != "test_overlap_in_starting_job":
                self.assertEqual(expected_params, response_dict[Keys.PARAMS])
            if self._testMethodName == "test_start_job_successfully":
                stat = Job.query.filter(Job.id == data[Keys.JOB_ID]).with_entities(Job.status_id).first()[0]
                self.assertEqual(expected_stat, stat)

    def test_start_job_successfully(self):
        data = {
            Keys.JOB_ID: 1,
            Keys.USER_TYPE: Keys.START_JOB_REQUEST
        }
        self._test_start_job_request(data, 200)

    def test_wrong_status_type(self):
        data = {
            Keys.JOB_ID: 1,
            Keys.USER_TYPE: Keys.START_JOB_REQUEST

        }
        self._test_start_job_request(data, 404, None)

    def test_not_existence_job(self):
        data = {
            Keys.JOB_ID: 7,
            Keys.USER_TYPE: Keys.START_JOB_REQUEST
        }
        self._test_start_job_request(data, 404, None)

    def test_overlap_in_starting_job(self):
        data = {
            Keys.JOB_ID: 1,
            Keys.USER_TYPE: Keys.START_JOB_REQUEST
        }
        self._test_start_job_request(data, 404, None)

    def test_no_db(self):
        data = {
            Keys.JOB_ID: 1,
            Keys.USER_TYPE: Keys.START_JOB_REQUEST
        }
        self._test_start_job_request(data, 500, 6)

    def test_bad_schema(self):
        data = {
            Keys.BUSINESS_OWNER_ID: 'should be integer'
        }
        self._test_start_job_request(data, 400, 5)


if __name__ == '__main__':
    unittest.main()
