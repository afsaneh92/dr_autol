#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from flask import json

from app import app, db
from config import DataBaseConfig
from core.messages.keys import Keys
from core.result import Result
from persistence.database.entity.calendar import Calendar
from persistence.database.entity.user.business_owner import BusinessOwner
from routers.admin import admin
from routers.authintication import authentication
from routers.business_owner import business_owner
from routers.car_owner import car_owner
from routers.choose_services import choose_service_grade
from routers.endpoints import Endpoints
from routers.index import index_route
from test_cases.fill_db import init_db


class MyTestCase(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config[
            'SQLALCHEMY_DATABASE_URI'] = DataBaseConfig.generate_database_uri()
        app.register_blueprint(authentication)
        app.register_blueprint(admin)

        app.register_blueprint(index_route)

        app.register_blueprint(business_owner)
        app.register_blueprint(authentication)
        app.register_blueprint(car_owner)
        app.register_blueprint(choose_service_grade)

        self.app = app.test_client()
        if self._testMethodName == "test_no_db":
            db.drop_all()

        # db.drop_all()
        # db.create_all()
        else:
            # pass
            init_db()

    # executed after each test
    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def make_post_request(self, data):
        res = self.app.post(Endpoints.INSERT_IN_CALENDAR, data=data, content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
        return res

    def test_no_db(self):
        data = {
            Keys.BUSINESS_OWNER_ID: 1,
            Keys.START_TIME: '2019-08-22 12:56:00',
            Keys.FINISH_TIME: '2019-08-22 14:56:00'
        }
        json_obj = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 500)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.SOMETHING_WENT_WRONG)
            # self.assertEqual(dct[Keys.PARAMS], None)

    def test_insert_job_b_o_calendar_exist_free(self):
        data = {
            Keys.BUSINESS_OWNER_ID: 1,
            Keys.START_TIME: '2019-06-22 12:56:00',
            Keys.FINISH_TIME: '2019-06-22 14:56:00'
        }
        json_obj = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            # self.assertEqual(dct[Keys.PARAMS], None)
            self.assertEqual(dct[Keys.STATUS], 200)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.SUCCESS_ADD_NEW_JOB)
            _, iws = Calendar.find(start_time=data[Keys.START_TIME], finish_time=data[Keys.FINISH_TIME],
                                   business_owner_id=data[Keys.BUSINESS_OWNER_ID])
            # print self. businessowner.id
            self.assertEqual(1, iws[0].id)

    def test_insert_job_b_o_calendar_exist_busy(self):
        data = {
            Keys.BUSINESS_OWNER_ID: 1,
            Keys.START_TIME: '2019-04-22 12:56:00',
            Keys.FINISH_TIME: '2019-04-22 14:56:00'
            # 03/21/2018 @ 9-11:00am (UTC)
            # "job": "تعویض روغن",
        }
        json_obj = json.dumps(data)
        # data = {id: data["business_owner_id"]}

        business_owner = BusinessOwner.find(id=data[Keys.BUSINESS_OWNER_ID])
        if business_owner[0]:
            self.business_owner = business_owner[1][0]
            calendar = Calendar(start_time=data[Keys.START_TIME], finish_time=data[Keys.FINISH_TIME],
                                business_owner_id=data[Keys.BUSINESS_OWNER_ID])
            result = calendar.add(db, calendar)
            self.business_owner.calendars.extend([calendar])

        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 404)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.BUSINESS_OWNER_IS_BUSY)
            self.assertEqual(dct[Keys.PARAMS], None)
            # _, iws = Calendar.is_free_business_owner(business_owner_id=data[Keys.BUSINESS_OWNER_ID],
            #                                          start_time=data[Keys.START_TIME], finish_time=data[Keys.FINISH_TIME])
            # print iws
            # self.assertEqual(iws, 1)

    def test_insert_job_b_o_calendar_not_exist(self):
        data = {

            Keys.BUSINESS_OWNER_ID: 505,
            Keys.START_TIME: '2019-04-22 12:56:00',
            Keys.FINISH_TIME: '2019-04-22 14:56:00'
        }
        json_obj = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1

            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            _, iws = Calendar.find(business_owner_id=data[Keys.BUSINESS_OWNER_ID])
            self.assertEqual(len(iws), 0)
            self.assertEqual(dct[Keys.STATUS], 404)
            # self.assertEqual(dct[Keys.PARAMS], None)

    def test_insert_job_b_o_calendar_false_regex(self):
        data = {
            Keys.BUSINESS_OWNER_ID: "5",
            Keys.START_TIME: '2018 3 12 ',
            Keys.FINISH_TIME: '2018 3 12  '
        }
        json_obj = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            # iws = Calendar.query.filter_by(business_owner_id=data[Keys.BUSINESS_OWNER_ID],
            #                                          start_time=data[Keys.START_TIME], finish_time=data[Keys.FINISH_TIME])
            print dct[Keys.MESSAGE], "jjj", dct[Keys.PARAMS]
            self.assertEqual(dct[Keys.STATUS], 400)
            # self.assertEqual(dct[Keys.PARAMS], None)????????????

    def test_insert_job_b_o_calendar_time_wrong(self):
        data = {
            Keys.BUSINESS_OWNER_ID: 1,
            Keys.START_TIME: '2019-04-23 12:56:00',
            Keys.FINISH_TIME: '2019-04-22 14:56:00'
        }
        json_obj = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 400)
            self.assertEqual(Result.language.BAD_SCHEMA, dct[Keys.MESSAGE])
            # _, iws = Calendar.find(start_time=data[Keys.START_TIME], finish_time=data[Keys.FINISH_TIME],
            #                        business_owner_id=data[Keys.BUSINESS_OWNER_ID])
            # # print self. businessowner.id
            # self.assertEqual(1, iws[0].id)

    def test_insert_job_b_o_calendar_time_not_exist_1(self):

        data = {
            Keys.BUSINESS_OWNER_ID: 1,
            Keys.START_TIME: '2019-04-22 11:00:00',
            Keys.FINISH_TIME: '2019-04-22 14:30:00'
        }

        json_obj = json.dumps(data)
        aaa = BusinessOwner.find(id=data[Keys.BUSINESS_OWNER_ID])
        if aaa[0]:
            self.business_owner = aaa[1][0]
            calendar = Calendar(start_time='2019-04-22 12:00:00', finish_time='2019-04-22 14:00:00',
                                business_owner_id=data[Keys.BUSINESS_OWNER_ID])
            result = calendar.add(db, calendar)

            self.business_owner.calendars.extend([calendar])
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 404)
            # self.assertEqual(dct[Keys.PARAMS], None)
            self.assertEqual(Result.language.BUSINESS_OWNER_IS_BUSY, dct[Keys.MESSAGE])
            # _, iws = Calendar.find(start_time=data[Keys.START_TIME], finish_time=data[Keys.FINISH_TIME],
            #                        business_owner_id=data[Keys.BUSINESS_OWNER_ID])
            # # print self. businessowner.id
            # self.assertEqual(1, iws[0].id)

    def test_insert_job_b_o_calendar_time_not_exist_2(self):

        data = {
            Keys.BUSINESS_OWNER_ID: 1,
            Keys.START_TIME: '2019-04-22 12:30:00',
            Keys.FINISH_TIME: '2019-04-22 14:30:00'
        }

        json_obj = json.dumps(data)
        aaa = BusinessOwner.find(id=data[Keys.BUSINESS_OWNER_ID])
        if aaa[0]:
            self.business_owner = aaa[1][0]
            calendar = Calendar(start_time='2019-04-22 12:00:00', finish_time='2019-04-22 14:00:00',
                                business_owner_id=data[Keys.BUSINESS_OWNER_ID])
            result = calendar.add(db, calendar)

            self.business_owner.calendars.extend([calendar])
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 404)
            self.assertEqual(Result.language.BUSINESS_OWNER_IS_BUSY, dct[Keys.MESSAGE])
            # _, iws = Calendar.find(start_time=data[Keys.START_TIME], finish_time=data[Keys.FINISH_TIME],
            #                        business_owner_id=data[Keys.BUSINESS_OWNER_ID])
            # # print self. businessowner.id
            # self.assertEqual(1, iws[0].id)

    def test_insert_job_b_o_calendar_time_not_exist_3(self):

        data = {
            Keys.BUSINESS_OWNER_ID: 1,
            Keys.START_TIME: '2019-04-22 11:00:00',
            Keys.FINISH_TIME: '2019-04-22 12:30:00'
        }

        json_obj = json.dumps(data)
        aaa = BusinessOwner.find(id=data[Keys.BUSINESS_OWNER_ID])
        if aaa[0]:
            self.business_owner = aaa[1][0]
            calendar = Calendar(start_time='2019-04-22 12:00:00', finish_time='2019-04-22 14:00:00',
                                business_owner_id=data[Keys.BUSINESS_OWNER_ID])
            result = calendar.add(db, calendar)

            self.business_owner.calendars.extend([calendar])
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 404)
            self.assertEqual(Result.language.BUSINESS_OWNER_IS_BUSY, dct[Keys.MESSAGE])
            # _, iws = Calendar.find(start_time=data[Keys.START_TIME], finish_time=data[Keys.FINISH_TIME],
            #                        business_owner_id=data[Keys.BUSINESS_OWNER_ID])
            # # print self. businessowner.id
            # self.assertEqual(1, iws[0].id)

    def test_insert_job_b_o_calendar_time_not_exist_4(self):

        data = {
            Keys.BUSINESS_OWNER_ID: 1,
            Keys.START_TIME: '2019-04-22 13:00:00',
            Keys.FINISH_TIME: '2019-04-22 14:00:00'
        }

        json_obj = json.dumps(data)
        aaa = BusinessOwner.find(id=data[Keys.BUSINESS_OWNER_ID])
        if aaa[0]:
            self.business_owner = aaa[1][0]
            calendar = Calendar(start_time='2019-04-22 12:00:00', finish_time='2019-04-22 14:00:00',
                                business_owner_id=data[Keys.BUSINESS_OWNER_ID])
            result = calendar.add(db, calendar)

            self.business_owner.calendars.extend([calendar])
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 404)
            self.assertEqual(Result.language.BUSINESS_OWNER_IS_BUSY, dct[Keys.MESSAGE])
            # _, iws = Calendar.find(start_time=data[Keys.START_TIME], finish_time=data[Keys.FINISH_TIME],
            #                        business_owner_id=data[Keys.BUSINESS_OWNER_ID])
            # # print self. businessowner.id
            # self.assertEqual(1, iws[0].id)

    def test_insert_job_b_o_calendar_past_time_not_exist(self):
        data = {
            Keys.BUSINESS_OWNER_ID: 1,
            Keys.START_TIME: '2018-03-12 13:00:00',
            Keys.FINISH_TIME: '2018-03-12 14:00:00'
        }

        json_obj = json.dumps(data)
        # aaa = BusinessOwner.find(id=data[Keys.BUSINESS_OWNER_ID])
        # if aaa[0]:
        #     self.business_owner = aaa[1][0]
        #     calendar = Calendar(start_time='2018-03-12 12:00:00', finish_time='2018-03-12 14:00:00',
        #                         business_owner_id=data[Keys.BUSINESS_OWNER_ID])
        #     result = calendar.add(db, calendar)
        #     self.business_owner.calendars.extend([calendar])

        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 400)

    def test_insert_job_b_o_calendar_miss_business_owner_id(self):
        data = {

            Keys.START_TIME: '2018-03-12 13:00:00',
            Keys.FINISH_TIME: '2018-03-12 14:00:00'
        }

        json_obj = json.dumps(data)

        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 400)

    def test_insert_job_b_o_calendar_miss_start_time(self):
        data = {
            Keys.BUSINESS_OWNER_ID: 1,
            Keys.FINISH_TIME: '2018-03-12 14:00:00'
        }

        json_obj = json.dumps(data)

        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 400)

    def test_insert_job_b_o_calendar_miss_finish_time(self):
        data = {
            Keys.BUSINESS_OWNER_ID: 1,
            Keys.START_TIME: '2018-03-12 13:00:00'
        }

        json_obj = json.dumps(data)

        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 400)


if __name__ == '__main__':
    unittest.main()
