#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from flask import json

from app import app, db
from config import DataBaseConfig
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result import Result
from persistence.database.entity.car import Car
from persistence.database.entity.user.user import User
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
            'SQLALCHEMY_DATABASE_URI'] = DataBaseConfig.DB_DIALECT + DataBaseConfig.USER_NAME \
                                         + ':' + DataBaseConfig.PASSWORD + '@' + DataBaseConfig.SERVER_ADDRESS \
                                         + ':' + DataBaseConfig.PORT + '/' + DataBaseConfig.DATABASE_NAME
        app.register_blueprint(authentication)
        app.register_blueprint(admin)

        app.register_blueprint(index_route)

        app.register_blueprint(business_owner)
        app.register_blueprint(authentication)
        app.register_blueprint(car_owner)
        app.register_blueprint(choose_service_grade)

        self.app = app.test_client()
        # init_db()
        # if self._testMethodName == "test_no_db":
        # db.drop_all()
        #
        db.drop_all()
        # # db.create_all()
        # else:
        #     # pass
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

    def make_post_request(self, data1):
        res = self.app.get(Endpoints.PAYABLE_LIST, data=data1, content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
        return res

    def test_give_payment_list_success(self):
        data = {
            "car_owner_id": 6
            # "car_id": 2
        }
        data1 = json.dumps(data)

        ccar = Car(vin_number="iRFC93R21SN497647", plate_number="77ط749-33", auto_type_id=1)
        User.query.filter(User.name == "MahD").first().cars.append(ccar)
        db.session.commit()

        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 6
            response = self.make_post_request(data1)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 200)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.SUCCESS_LIST)
            # self.assertEqual(dct[Keys.PARAMS], None)

    def test_give_payment_list_success_has_payed_list(self):
        # this id has payable and not payable job
        data = {
            "car_owner_id": 5
            # "car_id": 2
        }
        data1 = json.dumps(data)

        ccar = Car(vin_number="iRFC93R21SN497647", plate_number="77ط749-33", auto_type_id=1)
        User.query.filter(User.name == "HaD").first().cars.append(ccar)
        db.session.commit()

        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 6
            response = self.make_post_request(data1)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 200)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.SUCCESS_LIST)
            # self.assertEqual(dct[Keys.PARAMS], None)
            print dct[Keys.PARAMS]

    def test_give_payment_list_hasnt_not_payed_job(self):
        # this id hs no job
        data = {
            "car_owner_id": 4
            # "car_id": 2
        }
        data1 = json.dumps(data)

        # ccar = Car(vin_number="iRFC93R21SN497647", plate_number="77ط749-33", auto_type_id=1)
        # User.query.filter(User.name == "Amish").first().cars.append(ccar)
        # db.session.commit()

        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 6
            response = self.make_post_request(data1)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 404)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.NOT_FOUND_JOB)
            self.assertEqual(dct[Keys.PARAMS], None)

    def test_give_payment_list_not_exist_user(self):
        # this id hs no job
        data = {
            "car_owner_id": 14
            # "car_id": 2
        }
        data1 = json.dumps(data)

        # ccar = Car(vin_number="iRFC93R21SN497647", plate_number="77ط749-33", auto_type_id=1)
        # User.query.filter(User.name == "Amish").first().cars.append(ccar)
        # db.session.commit()

        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 6
            response = self.make_post_request(data1)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 404)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.NOT_FOUND_JOB)
            self.assertEqual(dct[Keys.PARAMS], None)

    def test_give_payment_list_false_regex_1(self):
        # this id hs no job
        data = {
            # "car_owner_id": 4
            # "car_id": 2
        }
        data1 = json.dumps(data)

        # ccar = Car(vin_number="iRFC93R21SN497647", plate_number="77ط749-33", auto_type_id=1)
        # User.query.filter(User.name == "Amish").first().cars.append(ccar)
        # db.session.commit()

        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 6
            response = self.make_post_request(data1)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 400)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.BAD_SCHEMA)
            # print dct[Keys.PARAMS]
            # self.assertEqual(dct[Keys.PARAMS], Result.language.MISSING_CAR_OWNER_IN_JSON)

    def test_give_payment_list_false_regex_2(self):
        # this id hs no job
        data = {
            "car_owner_id": '4'
            # "car_id": 2
        }
        data1 = json.dumps(data)

        # ccar = Car(vin_number="iRFC93R21SN497647", plate_number="77ط749-33", auto_type_id=1)
        # User.query.filter(User.name == "Amish").first().cars.append(ccar)
        # db.session.commit()

        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 6
            response = self.make_post_request(data1)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 400)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.BAD_SCHEMA)
            # print dct[Keys.PARAMS]
            # self.assertEqual(dct[Keys.PARAMS], Result.language.MISSING_CAR_OWNER_IN_JSON)


if __name__ == '__main__':
    unittest.main()
