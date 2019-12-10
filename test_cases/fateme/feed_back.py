#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from app import db, app
from config import DataBaseConfig
from core.messages.keys import Keys
from routers.admin import admin
from routers.authintication import authentication
from routers.car_owner import car_owner
from routers.business_owner import business_owner
from routers.choose_services import choose_service_grade
from routers.index import index_route
from test_cases.fill_db import init_db
import unittest
from routers.endpoints import Endpoints
from test_cases.test_keys import TestKeys


class TestFeedBack(unittest.TestCase):
    # executed prior to each test

    def setUp(self):
        app.config[TestKeys.TESTING] = True
        app.config[TestKeys.WTF_CSRF_ENABLED] = False
        app.config[TestKeys.DEBUG] = False
        app.config[
            TestKeys.SQLALCHEMY_DATABASE_URI] = DataBaseConfig.generate_database_uri()

        app.register_blueprint(index_route)
        app.register_blueprint(car_owner)
        app.register_blueprint(business_owner)
        app.register_blueprint(authentication)
        app.register_blueprint(admin)
        app.register_blueprint(choose_service_grade)
        self.app = app.test_client()
        if self._testMethodName == "test_no_db":
            db.drop_all()
        else:
            db.drop_all()
            init_db()

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_update_rate(self):
        update_data = {
            Keys.JOB_ID: 1,
            Keys.RATE: [-2, 2, 1]
        }

        json_obj = json.dumps(update_data)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 1
                sess[Keys.PHONE_NUMBER] = "09125200202"
                sess[Keys.TYPE_USER] = 'CarOwnerUser'
            response = client.put(Endpoints.RATE_BUSINESS_OWNER_BY_CAR_OWNER, data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 200)

    def test_rate_car_owner_to_exactly_his_job_true(self):
        update_data = {
            Keys.JOB_ID: 1,
            Keys.RATE: [-2, 1, 0]
        }

        json_obj = json.dumps(update_data)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 7
                sess[Keys.PHONE_NUMBER] = "09125200200"
                sess[Keys.TYPE_USER] = 'CarOwnerUser'
            response = client.put(Endpoints.RATE_BUSINESS_OWNER_BY_CAR_OWNER, data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 200)

    def test_rate_car_owner_to_exactly_his_job_false(self):
        update_data = {
            Keys.JOB_ID: 1,
            Keys.RATE: [-2, 1, 0]
        }

        json_obj = json.dumps(update_data)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 1
                sess[Keys.PHONE_NUMBER] = "09125200201"
                sess[Keys.TYPE_USER] = 'CarOwnerUser'
            response = client.put(Endpoints.RATE_BUSINESS_OWNER_BY_CAR_OWNER, data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_rate_is_out_of_range(self):
        update_data = {
            Keys.JOB_ID: 1,
            Keys.RATE: [1, 9, 5]
        }

        json_obj = json.dumps(update_data)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = True
                sess[Keys.PHONE_NUMBER] = "09125200202"
                sess[Keys.TYPE_USER] = 'CarOwnerUser'
            response = client.put(Endpoints.RATE_BUSINESS_OWNER_BY_CAR_OWNER, data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_rate_is_not_int(self):
        update_data = {
            Keys.JOB_ID: 1,
            Keys.RATE: [1, 'hi', 0]
        }

        json_obj = json.dumps(update_data)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = True
                sess[Keys.PHONE_NUMBER] = "09125200202"
                sess[Keys.TYPE_USER] = 'CarOwnerUser'
            response = client.put(Endpoints.RATE_BUSINESS_OWNER_BY_CAR_OWNER, data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 400)

    def test_perfect_rate_just_to_first_question_false(self):
        update_data = {
            Keys.JOB_ID: 1,
            Keys.RATE: [2, 0, 0]
        }

        json_obj = json.dumps(update_data)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = True
                sess[Keys.PHONE_NUMBER] = "09125200202"
                sess[Keys.TYPE_USER] = 'CarOwnerUser'
            response = client.put(Endpoints.RATE_BUSINESS_OWNER_BY_CAR_OWNER, data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_rate_none_to_second_question_false(self):
        update_data = {
            Keys.JOB_ID: 1,
            Keys.RATE: [1, None, 0]
        }

        json_obj = json.dumps(update_data)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = True
                sess[Keys.PHONE_NUMBER] = "09125200202"
                sess[Keys.TYPE_USER] = 'CarOwnerUser'
            response = client.put(Endpoints.RATE_BUSINESS_OWNER_BY_CAR_OWNER, data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_rate_none_to_second_question_true(self):
        update_data = {
            Keys.JOB_ID: 1,
            Keys.RATE: [1, None, None]
        }

        json_obj = json.dumps(update_data)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = True
                sess[Keys.PHONE_NUMBER] = "09125200202"
                sess[Keys.TYPE_USER] = 'CarOwnerUser'
            response = client.put(Endpoints.RATE_BUSINESS_OWNER_BY_CAR_OWNER, data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 200)

    def test_bad_schema(self):
        data = {
            Keys.JOB_ID: 1,
        }

        json_obj = json.dumps(data)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = True

            response = client.put(Endpoints.RATE_BUSINESS_OWNER_BY_CAR_OWNER, data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 400)

    def test_job_rated_before_false(self):
        found_data = {
            Keys.JOB_ID: 3,
            Keys.RATE: [-2, 1, 0]
        }
        json_obj = json.dumps(found_data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 1
                sess[Keys.PHONE_NUMBER] = "09125200201"
                sess[Keys.TYPE_USER] = 'CarOwnerUser'
            response = client.put(Endpoints.RATE_BUSINESS_OWNER_BY_CAR_OWNER, data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_job_rated_before_true(self):
        update_data = {
            Keys.JOB_ID: 1,
            Keys.RATE: [-2, 1, 0]
        }
        json_obj = json.dumps(update_data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = True
                sess[Keys.PHONE_NUMBER] = "09125200202"
                sess[Keys.TYPE_USER] = 'CarOwnerUser'
            response = client.put(Endpoints.RATE_BUSINESS_OWNER_BY_CAR_OWNER, data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 200)

    def test_is_job_not_finished_true(self):
        update_data = {
            Keys.JOB_ID: 1,
            Keys.RATE: [-2, 1, 0]
        }
        json_obj = json.dumps(update_data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 1
                sess[Keys.PHONE_NUMBER] = "09125200202"
                sess[Keys.TYPE_USER] = 'CarOwnerUser'
            response = client.put(Endpoints.RATE_BUSINESS_OWNER_BY_CAR_OWNER, data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 200)

    def test_is_job_not_finished_false(self):
        not_found_data = {
            Keys.JOB_ID: 3,
            Keys.RATE: [-2, 1, 0]
        }

        json_obj = json.dumps(not_found_data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = True
                sess[Keys.PHONE_NUMBER] = "09125200201"
                sess[Keys.TYPE_USER] = 'CarOwnerUser'
            response = client.put(Endpoints.RATE_BUSINESS_OWNER_BY_CAR_OWNER, data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_is_car_owner_not_exist_true(self):
        update_data = {
            Keys.JOB_ID: 1,
            Keys.RATE: [-2, 1, 0]
        }

        json_obj = json.dumps(update_data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 1
                sess[Keys.PHONE_NUMBER] = "09125200202"
                sess[Keys.TYPE_USER] = 'CarOwnerUser'
            response = client.put(Endpoints.RATE_BUSINESS_OWNER_BY_CAR_OWNER, data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 200)

    def test_is_car_owner_not_exist_false(self):
        not_found_data = {
            Keys.JOB_ID: 1,
            Keys.RATE: [-2, 1, 0]
        }

        json_obj = json.dumps(not_found_data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 1
                sess[Keys.PHONE_NUMBER] = "09125200787"
                sess[Keys.TYPE_USER] = 'CarOwnerUser'
            response = client.put(Endpoints.RATE_BUSINESS_OWNER_BY_CAR_OWNER, data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_is_job_not_exist_false(self):
        not_found_data = {
            Keys.JOB_ID: 25,
            Keys.RATE: [-2, 1, 0]
        }

        json_obj = json.dumps(not_found_data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 1
                sess[Keys.PHONE_NUMBER] = "09125200200"
                sess[Keys.TYPE_USER] = 'CarOwner'
            response = client.put(Endpoints.RATE_BUSINESS_OWNER_BY_CAR_OWNER, data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_number_of_question_more_than_answers_is_true(self):
        update_data = {
            Keys.JOB_ID: 1,
            Keys.RATE: [-2, 1, 0]
        }
        json_obj = json.dumps(update_data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 1
                sess[Keys.PHONE_NUMBER] = "09125200202"
                sess[Keys.TYPE_USER] = 'CarOwnerUser'
            response = client.put(Endpoints.RATE_BUSINESS_OWNER_BY_CAR_OWNER, data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 200)

    def test_number_of_answers_more_than_questions_is_false(self):
        wrong_data = {
            Keys.JOB_ID: 1,
            Keys.RATE: [-2, 1, 1, 1]

        }
        json_obj = json.dumps(wrong_data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 1
                sess[Keys.PHONE_NUMBER] = "09125200202"
                sess[Keys.TYPE_USER] = 'CarOwnerUser'
            response = client.put(Endpoints.RATE_BUSINESS_OWNER_BY_CAR_OWNER, data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_no_db(self):
        data = {
            Keys.JOB_ID: 1,
            Keys.RATE: [-2, 1, 0]
        }

        json_obj = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = True
                sess[Keys.PHONE_NUMBER] = '09125200202'
                sess[Keys.TYPE_USER] = 'CarOwnerUser'
            response = client.put(Endpoints.RATE_BUSINESS_OWNER_BY_CAR_OWNER, data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 500)

    def test_send_poll_to_user(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 6
            response = self.app.get(Endpoints.LAST_EVENT, content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 200)


if __name__ == '__main__':
    unittest.main()
