#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from flask import json

from app import app, db
from config import DataBaseConfig
from core.messages.keys import Keys
from core.result import Result
from persistence.database.entity.calendar import Calendar
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
        app.config['SQLALCHEMY_DATABASE_URI'] = DataBaseConfig.generate_database_uri()
        # app.register_blueprint(car_owner)
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

        else:
            init_db()

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def make_post_request(self, data):
        res = self.app.put(Endpoints.DELETE_FROM_CALENDAR, data=data, content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
        return res

    def test_no_db(self):
        data = {
            Keys.CALENDAR_ID: 1
        }
        json_obj = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 500)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.SOMETHING_WENT_WRONG)

    def test_delete_job_b_o_calender_exist_info(self):
        data = {
            Keys.CALENDAR_ID: 1
        }
        json_obj = json.dumps(data)
        # aaa = BusinessOwner.find(id=data[Keys.BUSINESS_OWNER_ID])
        # if aaa[0]:
        #     self.business_owner = aaa[1][0]
        calendar = Calendar(start_time='2019-04-12 12:56:00', finish_time='2019-04-12 14:56:00',
                            business_owner_id=1)
        result = calendar.add(db, calendar)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)

            self.assertEqual(dct[Keys.STATUS], 200)
            # self.assertEqual(dct[Keys.MESSAGE], Result.language.SUCCESS_UPDATE)
            _, iws = Calendar.find(id=1)
            print iws
            # tedad mosavi 0 bashe
            self.assertEqual(iws[0].flag, {Keys.DELETED: 1})
            # self.assertEqual(dct[Keys.PARAMS], None)

    def test_delete_job_b_o_calender_not_exist_id_calendar(self):
        data = {
            Keys.CALENDAR_ID: 3
        }
        json_obj = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            _, iws = Calendar.find(id=data[Keys.CALENDAR_ID])
            # _, iws = Calendar.find(start_time=data[Keys.START_TIME], finish_time=data[Keys.FINISH_TIME],
            #                        business_owner_id=data[Keys.BUSINESS_OWNER_ID])
            print iws
            self.assertEqual(len(iws), 0)
            self.assertEqual(dct[Keys.STATUS], 404)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.NOT_FOUND_JOB)
            # self.assertEqual(dct[Keys.PARAMS], None)

    def test_delete_job_b_o_calender_not_exist_time(self):
        data = {
            Keys.CALENDAR_ID: 1
        }
        json_obj = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            # iws = Calendar.find(start_time=data[Keys.START_TIME], finish_time=data[Keys.FINISH_TIME],
            #                        business_owner_id=data[Keys.BUSINESS_OWNER_ID])
            self.assertEqual(dct[Keys.STATUS], 404)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.NOT_FOUND_JOB)

    def test_delete_job_b_o_calender_false_regex(self):
        data = {
            Keys.CALENDAR_ID: "1"
        }
        json_obj = json.dumps(data)
        with self.app as client:
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            # iws = Calendar.query.filter_by("busiess_owner_id": "975537", "time_stamp_start": "1521622800",
            #                                    "time_stamp_finish": "1521630000", "job":"تعویض روغن", "condition":"true").first()
            self.assertEqual(dct[Keys.STATUS], 400)
            # self.assertEqual(dct[Keys.PARAMS], None)

    def test_delete_job_b_o_calender_miss_id(self):
        data = {

        }
        json_obj = json.dumps(data)
        with self.app as client:
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            # iws = Calendar.query.filter_by("busiess_owner_id": "975537", "time_stamp_start": "1521622800",
            #                                    "time_stamp_finish": "1521630000", "job":"تعویض روغن", "condition":"true").first()
            self.assertEqual(dct[Keys.STATUS], 400)


if __name__ == '__main__':
    unittest.main()
