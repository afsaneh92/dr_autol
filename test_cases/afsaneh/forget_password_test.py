#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from flask import json, session
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from app import db, app
from config import DataBaseConfig
from core.controller.forget_password.forget_password import States
from core.messages.keys import Keys
from core.result import Result
from persistence.database.entity.business_owner import BusinessOwners
from persistence.database.entity.user.user import User
from routers.authintication import authentication
from routers.endpoints import Endpoints
from test_cases.fill_db import init_db


class MyTestCase(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config[
            'SQLALCHEMY_DATABASE_URI'] = DataBaseConfig.DB_DIALECT + DataBaseConfig.USER_NAME + ':' + DataBaseConfig.PASSWORD + '@' + DataBaseConfig.SERVER_ADDRESS + ':' + DataBaseConfig.PORT + '/' + DataBaseConfig.DATABASE_NAME
        # app.register_blueprint(index_route)
        # app.register_blueprint(car_owner)
        app.register_blueprint(authentication)
        # app.register_blueprint(admin)
        # app.register_blueprint(choose_service_grade)

        self.app = app.test_client()
        if self._testMethodName == "test_no_db":
            db.drop_all()
        # db.drop_all()
        # db.create_all()
        else:
            init_db()
        # b_o_list = [
        #     {
        #         "name": u"احمذ",
        #         "phone_number": "09125200780",
        #         "validate": True,
        #         "password": "Amish1234",
        #         "code": "1234"
        #     },
        #     {
        #         "name": u"امید",
        #         "phone_number": "09125200781",
        #         "validate": True,
        #         "password": "Amish1234",
        #         "code": "1234"
        #     },
        #     {
        #         "name": u"حسن",
        #         "phone_number": "09125200782",
        #         "validate": True,
        #         "password": "Amish1234",
        #         "code": "1234"
        #     },
        #     {
        #         "name": u"محمود",
        #         "phone_number": "09125200783",
        #         "validate": True,
        #         "password": "Amish1234",
        #         "code": "1234"
        #     },
        #     {
        #         "name": u"پدرام",
        #         "phone_number": "09125200784",
        #         "validate": True,
        #         "password": "Amish1234",
        #         "code": "1234"
        #     },
        #     {
        #         "name": u"پرهام",
        #         "phone_number": "09125200785",
        #         "validate": True,
        #         "password": "Amish1234",
        #         "code": "1234"
        #     },
        #
        # ]
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

    def make_post_request(self, data):
        res = self.app.post(Endpoints.FORGET_PASSWORD, data=data, content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
        return res
        # with self.app as client:
        #     return client.post('/forget_password', data=data, content_type='application/json')

    # def test_forgetPassword_root(self):
    #     data = {
    #         "phone_number": "09124274836",
    #         "user_type": "1"
    #     }
    #     json_obj = json.dumps(data)
    #     with self.app as client:
    #         response = client.post('/forget_password', data=json_obj, content_type='application/json')
    #         self.assertEqual(response.status_code, 200)
    #
    # def test_forget_password_request(self):
    #     iws_reuest = {
    #         "phone_number": "09124274836",
    #     }
    #     json_obj = json.dumps(iws_reuest)
    #     iws = ForgetPasswordRequest.deserialize(json_obj)
    #     self.assertEqual(True, iws[0])
    #
    # def test_require_code_controller(self):
    #     # iws_reuest = {
    #     #     "phone_number": "09124274836",
    #     #     "user_type": "iws owner"
    #     # }
    #     # json_obj = json.dumps(iws_reuest)
    #     converter = JSONConverter()
    #     request_info = ForgetPasswordRequest(phone_number="09125200780")
    #     forget_password_controller = ForgetPasswordController(request_info, converter)
    #     ret = forget_password_controller.execute()
    #     print(ret)
    #     # self.assertEqual(200, ret["status"])
    #     # self.assertEqual(Result.language.CODE_SEND_SUCCESSFULLY, ret["message"])
    #     # self.assertEqual(None, ret["params"])
    #

    def test_no_db(self):
        data = {
            Keys.PHONE_NUMBER: "09125200780",
            Keys.TYPE_USER: Keys.BUSINESS_OWNER,
            "user_type": "1"
        }

        json_obj = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['logged_in'] = True
                sess[Keys.FORGET_PASS] = {}
                sess[Keys.FORGET_PASS][Keys.TYPE_USER] = Keys.BUSINESS_OWNER
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 500)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.SOMETHING_WENT_WRONG)

    def test_not_exist_number_endpoint(self):
        data = {
            Keys.PHONE_NUMBER:"09124274836",
            "user_type": "1",
            Keys.TYPE_USER: Keys.BUSINESS_OWNER
        }
        json_obj = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.FORGET_PASS] = {}
                sess[Keys.FORGET_PASS][Keys.TYPE_USER] = Keys.BUSINESS_OWNER
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 404)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.NOT_REGISTERED_BEFORE)
            self.assertEqual(dct[Keys.PARAMS][Keys.PHONE_NUMBER], data[Keys.PHONE_NUMBER])
            self.assertEqual(session[Keys.FORGET_PASS][Keys.STATE_ID], States.PHONE_NUMBER)

    def test_false_regex_number_endpoint_1(self):
        data = {
            Keys.TYPE_USER: Keys.BUSINESS_OWNER,
            Keys.PHONE_NUMBER: "",
            "user_type": "1"
        }
        json_obj = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.FORGET_PASS] = {}
                sess[Keys.FORGET_PASS][Keys.TYPE_USER] = Keys.BUSINESS_OWNER
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 400)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.BAD_SCHEMA)
            # self.assertEqual(dct[Keys.PARAMS][Keys.PHONE_NUMBER], data[Keys.PHONE_NUMBER])
            self.assertEqual(session[Keys.FORGET_PASS][Keys.STATE_ID], States.PHONE_NUMBER)

    def test_false_regex_number_endpoint_2(self):
        data = {
            Keys.TYPE_USER: Keys.BUSINESS_OWNER,
            Keys.PHONE_NUMBER: "09124273",
            "user_type": "1"
        }
        json_obj = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.FORGET_PASS] = {}
                sess[Keys.FORGET_PASS][Keys.TYPE_USER] = Keys.BUSINESS_OWNER
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 400)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.BAD_SCHEMA)
            # self.assertEqual(dct[Keys.PARAMS][Keys.PHONE_NUMBER], data[Keys.PHONE_NUMBER])
            self.assertEqual(session[Keys.FORGET_PASS][Keys.STATE_ID], States.PHONE_NUMBER)

    def test_false_regex_number_endpoint_3(self):
        data = {
            Keys.TYPE_USER: Keys.BUSINESS_OWNER,
            "user_type": "1"
        }
        json_obj = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.FORGET_PASS] = {}
                sess[Keys.FORGET_PASS][Keys.TYPE_USER] = Keys.BUSINESS_OWNER
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 400)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.BAD_SCHEMA)
            # self.assertEqual(dct[Keys.PARAMS][Keys.PHONE_NUMBER], data[Keys.PHONE_NUMBER])
            self.assertEqual(session[Keys.FORGET_PASS][Keys.STATE_ID], States.PHONE_NUMBER)

    def test_true_phone_number_endpoint(self):
        data = {

            Keys.PHONE_NUMBER: "09125200100",
            Keys.TYPE_USER: Keys.BUSINESS_OWNER,
            "user_type": "1"
        }
        json_obj = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.FORGET_PASS] = {}  # States.PHONE_NUMBER
                # sess[Keys.FORGET_PASS][Keys.TYPE_USER] = Keys.BUSINESS_OWNER
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 200)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.CODE_SEND_SUCCESSFULLY)
            self.assertEqual(dct[Keys.PARAMS], None)
            self.assertEqual(session[Keys.FORGET_PASS][Keys.STATE_ID], States.CODE)
            # self.assertEqual(sess.update({Keys.FORGET_PASS: {Keys.STATE_ID: }}), States.CODE)

    def test_true_send_code(self):
        data = {
            Keys.CODE: "1912",
            Keys.PHONE_NUMBER: '09125200100'
        }
        json_obj = json.dumps(data)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.FORGET_PASS] = {}
                sess[Keys.FORGET_PASS][Keys.STATE_ID] = States.CODE
                # session[Keys.STATE_ID] = sess[Keys.FORGET_PASS][Keys.STATE_ID]
                sess[Keys.FORGET_PASS][Keys.CODE] = data[Keys.CODE]
                sess[Keys.FORGET_PASS][Keys.PHONE_NUMBER] = data[Keys.PHONE_NUMBER]
                sess[Keys.FORGET_PASS][Keys.USER_ID] = data[Keys.PHONE_NUMBER]
                sess[Keys.FORGET_PASS][Keys.TYPE_USER] = Keys.BUSINESS_OWNER
            #  print "sess:", sess
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 200)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.CODE_RECEIVE_SUCCESSFULLY)
            self.assertEqual(dct[Keys.PARAMS], None)
            self.assertEqual(session[Keys.FORGET_PASS][Keys.STATE_ID], States.PASSWORD)

    def test_not_exist_send_code(self):
        data = {
            Keys.PHONE_NUMBER: '09125200100',
            Keys.CODE: '7777'
        }

        json_obj = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.FORGET_PASS] = {}
                sess[Keys.FORGET_PASS][Keys.STATE_ID] = Keys.CODE
                sess[Keys.FORGET_PASS][Keys.CODE] = '6666'
                sess[Keys.FORGET_PASS][Keys.TYPE_USER] = Keys.BUSINESS_OWNER
                sess[Keys.FORGET_PASS][Keys.PHONE_NUMBER] = data[Keys.PHONE_NUMBER]
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 404)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.CODE_RECEIVE_FAILED)
            # self.assertEqual(dct[Keys.PARAMS], None)
            self.assertEqual(session[Keys.FORGET_PASS][Keys.STATE_ID], States.RESEND_CODE)

    def test_not_exist_send_code_if_user_wants_the_other_code(self):
        data = {
            Keys.PHONE_NUMBER: '09125200100',
            Keys.CODE: '7777'
        }

        json_obj = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.FORGET_PASS] = {}
                sess[Keys.FORGET_PASS][Keys.STATE_ID] = Keys.CODE
                sess[Keys.FORGET_PASS][Keys.CODE] = '6666'
                sess[Keys.FORGET_PASS][Keys.TYPE_USER] = Keys.BUSINESS_OWNER
                sess[Keys.FORGET_PASS][Keys.PHONE_NUMBER] = data[Keys.PHONE_NUMBER]
                sess[Keys.FORGET_PASS][Keys.NAME] = "Afsane"
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 404)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.CODE_RECEIVE_FAILED)
            # self.assertEqual(dct[Keys.PARAMS], None)
            self.assertEqual(session[Keys.FORGET_PASS][Keys.STATE_ID], States.RESEND_CODE)

    def test_not_exist_send_code_and_send_new_code(self):
        data = {
            Keys.PHONE_NUMBER: '09125200100',
        }

        json_obj = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.FORGET_PASS] = {}
                sess[Keys.FORGET_PASS][Keys.STATE_ID] = "fgffffff"#Keys.RESEND_CODE
                sess[Keys.FORGET_PASS][Keys.CODE] = '6666'
                sess[Keys.FORGET_PASS][Keys.TYPE_USER] = Keys.BUSINESS_OWNER
                sess[Keys.FORGET_PASS][Keys.USER_ID] = data[Keys.PHONE_NUMBER]
                sess[Keys.FORGET_PASS][Keys.NAME] = "Afsane"
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            print dct[Keys.MESSAGE]
            self.assertEqual(dct[Keys.STATUS], 200)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.CODE_SEND_SUCCESSFULLY)
            # self.assertEqual(dct[Keys.PARAMS], None)
            self.assertEqual(session[Keys.FORGET_PASS][Keys.STATE_ID], States.CODE)

    def test_false_regex_send_code_1(self):
        data = {
            Keys.CODE: '',
            Keys.PHONE_NUMBER: '09125200780'
        }
        json_obj = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.FORGET_PASS] = {}
                sess[Keys.FORGET_PASS][Keys.STATE_ID] = Keys.CODE
                sess[Keys.FORGET_PASS][Keys.CODE] = '6666'
                sess[Keys.FORGET_PASS][Keys.TYPE_USER] = Keys.BUSINESS_OWNER
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 400)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.BAD_SCHEMA)
            # self.assertEqual(dct[Keys.PARAMS], None)
            self.assertEqual(session[Keys.FORGET_PASS][Keys.STATE_ID], States.PHONE_NUMBER)

    def test_false_regex_send_code_2(self):
        data = {
            Keys.CODE: '999999',
            Keys.PHONE_NUMBER: '09125200780'
        }
        json_obj = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.FORGET_PASS] = {}
                sess[Keys.FORGET_PASS][Keys.STATE_ID] = Keys.CODE
                sess[Keys.FORGET_PASS][Keys.CODE] = '6666'
                sess[Keys.FORGET_PASS][Keys.TYPE_USER] = Keys.BUSINESS_OWNER
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 400)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.BAD_SCHEMA)
            # self.assertEqual(dct[Keys.PARAMS], None)
            self.assertEqual(session[Keys.FORGET_PASS][Keys.STATE_ID], States.PHONE_NUMBER)

    def test_false_regex_send_code_3(self):
        data = {
            Keys.PHONE_NUMBER: '09125200780'
        }
        json_obj = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.FORGET_PASS] = {}
                sess[Keys.FORGET_PASS][Keys.STATE_ID] = Keys.CODE
                sess[Keys.FORGET_PASS][Keys.CODE] = '6666'
                sess[Keys.FORGET_PASS][Keys.TYPE_USER] = Keys.BUSINESS_OWNER
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 400)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.BAD_SCHEMA)
            # self.assertEqual(dct[Keys.PARAMS], None)
            self.assertEqual(session[Keys.FORGET_PASS][Keys.STATE_ID], States.PHONE_NUMBER)

    def test_true_send_password(self):
        data = {
            Keys.PASSWORD: "Ah5h4hhh",
            Keys.PHONE_NUMBER: '09125200100',
            Keys.TYPE_USER: Keys.BUSINESS_OWNER
        }
        json_obj = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.FORGET_PASS] = {}
                sess[Keys.FORGET_PASS][Keys.STATE_ID] = States.PASSWORD
                sess[Keys.FORGET_PASS][Keys.CODE] = data[Keys.PASSWORD]
                sess[Keys.FORGET_PASS][Keys.PHONE_NUMBER] = data[Keys.PHONE_NUMBER]
                sess[Keys.FORGET_PASS][Keys.USER_ID] = data[Keys.PHONE_NUMBER]
                sess[Keys.FORGET_PASS][Keys.TYPE_USER] = Keys.BUSINESS_OWNER
                # sess.update({Keys.FORGET_PASS: {Keys.STATE_ID: States.PASSWORD}})
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 200)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.PASSWORD_CHANGE_SUCCESSFULLY)
            self.assertEqual(dct[Keys.PARAMS], None)
            # self.assertEqual(session[Keys.FORGET_PASS][Keys.STATE_ID],  "")
            _, iws = User.find(phone_number=data[Keys.PHONE_NUMBER])
            # dct = json.loads(response.data)
            result = pbkdf2_sha256.verify(data[Keys.PASSWORD], iws[0].password)
            self.assertTrue(result)

    def test_false_regex_password_1(self):
        data = {
            Keys.PASSWORD: "hhhhhh",
            Keys.TYPE_USER: Keys.BUSINESS_OWNER,
            Keys.PHONE_NUMBER: '09125200100'
        }
        json_obj = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.FORGET_PASS] = {}
                sess[Keys.FORGET_PASS][Keys.STATE_ID] = States.PASSWORD
                # sess[Keys.FORGET_PASS][Keys.CODE] = data[Keys.PASSWORD]
                sess[Keys.FORGET_PASS][Keys.PHONE_NUMBER] = data[Keys.PHONE_NUMBER]
                # sess.update({Keys.FORGET_PASS: {Keys.STATE_ID: States.PASSWORD}})
                sess[Keys.FORGET_PASS][Keys.TYPE_USER] = Keys.BUSINESS_OWNER
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 400)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.BAD_SCHEMA)
            # self.assertEqual(dct[Keys.PARAMS], None)
            self.assertEqual(session[Keys.FORGET_PASS][Keys.STATE_ID], States.PASSWORD)

            _, iws = User.find(phone_number=data[Keys.PHONE_NUMBER])
            print iws
            # dct = json.loads(response.data)
            result = pbkdf2_sha256.verify(data[Keys.PASSWORD], iws[0].password)
            self.assertFalse(result)

    def test_false_regex_password_2(self):
        data = {
            Keys.PHONE_NUMBER: '09125200780'
        }
        json_obj = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.FORGET_PASS] = {}
                sess[Keys.FORGET_PASS][Keys.STATE_ID] = States.PASSWORD
                # sess[Keys.FORGET_PASS][Keys.CODE] = data[Keys.PASSWORD]
                sess[Keys.FORGET_PASS][Keys.PHONE_NUMBER] = data[Keys.PHONE_NUMBER]
                sess[Keys.FORGET_PASS][Keys.TYPE_USER] = Keys.BUSINESS_OWNER
                # sess.update({Keys.FORGET_PASS: {Keys.STATE_ID: States.PASSWORD}})
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 400)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.BAD_SCHEMA)
            # self.assertEqual(dct[Keys.PARAMS], None)
            self.assertEqual(session[Keys.FORGET_PASS][Keys.STATE_ID], States.PASSWORD)

            # _, iws = BusinessOwner.find(phone_number=data['phone_number'])
            # print iws
            # # dct = json.loads(response.data)
            # result = pbkdf2_sha256.verify(data['password'], iws[0].password)
            # self.assertFalse(result)

    def test_false_regex_password_3(self):
        data = {
            Keys.PASSWORD: " ",
            Keys.TYPE_USER: Keys.BUSINESS_OWNER,
            Keys.PHONE_NUMBER: '09125200100'
        }
        json_obj = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.FORGET_PASS] = {}
                sess[Keys.FORGET_PASS][Keys.STATE_ID] = States.PASSWORD
                # sess[Keys.FORGET_PASS][Keys.CODE] = data[Keys.PASSWORD]
                sess[Keys.FORGET_PASS][Keys.PHONE_NUMBER] = data[Keys.PHONE_NUMBER]
                sess[Keys.FORGET_PASS][Keys.TYPE_USER] = "BusinessOwner"
                # sess.update({Keys.FORGET_PASS: {Keys.STATE_ID: States.PASSWORD}})
            response = self.make_post_request(json_obj)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 400)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.BAD_SCHEMA)
            # self.assertEqual(dct[Keys.PARAMS], None)
            self.assertEqual(session[Keys.FORGET_PASS][Keys.STATE_ID], States.PASSWORD)

            _, iws = User.find(phone_number=data[Keys.PHONE_NUMBER])
            print iws
            # dct = json.loads(response.data)
            result = pbkdf2_sha256.verify(data[Keys.PASSWORD], iws[0].password)
            self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
