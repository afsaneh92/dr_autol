# !/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import unittest

from app import app, db
from config import DataBaseConfig
from core.messages.keys import Keys
from persistence.database.entity.jobs import Jobs
from routers.car_owner import car_owner
from routers.endpoints import Endpoints
from test_cases.fill_db import init_db


class PaymentTest(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config[
            'SQLALCHEMY_DATABASE_URI'] = DataBaseConfig.DB_DIALECT + DataBaseConfig.USER_NAME + ':' + DataBaseConfig.PASSWORD + '@' + DataBaseConfig.SERVER_ADDRESS + ':' + DataBaseConfig.PORT + '/' + DataBaseConfig.DATABASE_NAME
        app.register_blueprint(car_owner)

        self.app = app.test_client()

        # db.create_all()
        if self._testMethodName == "test_no_db":
            db.drop_all()
        else:
            pass
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

        response = self.app.post(url, data=json_obj, content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
        print(response.data)
        return response

    def _test_payment_operation_request(self, data, expected_response, expected_params=None, expected_stat=8):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self._start_request(Endpoints.CAR_OWNER_PAYMENTS, data)
            response_dict = json.loads(response.data)
            self.assertEqual(expected_response, response.status_code)
            if self._testMethodName != "test_no_db" and self._testMethodName != "test_bad_schema" and self._testMethodName != "test_no_payment_type" and self._testMethodName != "test_overlap_in_starting_job":
                self.assertEqual(expected_params, response_dict[Keys.PARAMS])
            if self._testMethodName == "test_start_job_successfully":
                stat = Jobs.query.filter(Jobs.id == data[Keys.JOB_ID]).with_entities(Jobs.status_id).first()[0]
                self.assertEqual(expected_stat, stat)

    def test_no_db(self):
        data = {
            Keys.JOB_ID: 1,
            Keys.USER_TYPE: Keys.FULL_PAYMENT_REQUEST,
            Keys.PAYMENT_TYPE: 1,
            Keys.TRANSACTION_NUMBER: '1010',
            Keys.PAYMENT_AMOUNT: 6000
        }
        self._test_payment_operation_request(data, 500, 6)

    def test_bad_schema(self):
        data = {
            Keys.JOB_ID: 'dfdf',
            Keys.USER_TYPE: Keys.FULL_PAYMENT_REQUEST,
            Keys.PAYMENT_TYPE: 'dfdsf',
            Keys.TRANSACTION_NUMBER: '1010',
            Keys.PAYMENT_AMOUNT: 'dfdsfdsf'
        }
        self._test_payment_operation_request(data, 400, 5)

    def test_no_job(self):
        data = {
            Keys.JOB_ID: 16456,
            Keys.USER_TYPE: Keys.FULL_PAYMENT_REQUEST,
            Keys.PAYMENT_TYPE: 1,
            Keys.TRANSACTION_NUMBER: '1010',
            Keys.PAYMENT_AMOUNT: 6000
        }
        self._test_payment_operation_request(data, 404, None, None)

    def test_wrong_amount(self):
        data = {
            Keys.JOB_ID: 1,
            Keys.USER_TYPE: Keys.FULL_PAYMENT_REQUEST,
            Keys.PAYMENT_TYPE: 1,
            Keys.TRANSACTION_NUMBER: '1010',
            Keys.PAYMENT_AMOUNT: 60001
        }
        self._test_payment_operation_request(data, 404, None, None)

    def test_cannot_pay(self):
        data = {
            Keys.JOB_ID: 1,
            Keys.USER_TYPE: Keys.FULL_PAYMENT_REQUEST,
            Keys.PAYMENT_TYPE: 1,
            Keys.TRANSACTION_NUMBER: '1010',
            Keys.PAYMENT_AMOUNT: 6000
        }
        job = Jobs.load_job(data[Keys.JOB_ID])
        update_data = {
            'status_id': 3
        }
        Jobs.update_status(job[1], update_data, db)
        self._test_payment_operation_request(data, 404, None, None)

    def test_no_payment_type(self):
        data = {
            Keys.JOB_ID: 1,
            Keys.USER_TYPE: Keys.FULL_PAYMENT_REQUEST,
            Keys.PAYMENT_TYPE: 1212,
            Keys.TRANSACTION_NUMBER: '1010',
            Keys.PAYMENT_AMOUNT: 6000
        }
        self._test_payment_operation_request(data, 404, None, None)

    def test_do_payment(self):
        data = {
            Keys.JOB_ID: 1,
            Keys.USER_TYPE: Keys.FULL_PAYMENT_REQUEST,
            Keys.PAYMENT_TYPE: 1,
            Keys.TRANSACTION_NUMBER: '1010',
            Keys.PAYMENT_AMOUNT: 96369
        }
        self._test_payment_operation_request(data, 200, None, None)


if __name__ == '__main__':
    unittest.main()
