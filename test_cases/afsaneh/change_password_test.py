#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from flask import session, json
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from app import app, db
from config import DataBaseConfig
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result import Result
from persistence.database.entity.user.user import User
from routers.endpoints import Endpoints
from test_cases.fill_db import init_db
from routers.authintication import authentication


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
        res = self.app.post(Endpoints.CHANGE_PASSWORD, data=data1, content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
        return res

    def test_no_db(self):
        data = {
            Keys.OLD_PASSWORD: "Amish1234",
            Keys.NEW_PASSWORD: "Afsane1234",
            # 'phone_number': '09125200780',
            Keys.TYPE_USER: Keys.BUSINESS_OWNER
        }

        data1 = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
                sess[Keys.PHONE_NUMBER] = '09125200100'
            response = self.make_post_request(data1)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 500)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.SOMETHING_WENT_WRONG)
            # self.assertEqual(dct[Keys.PARAMS], None)
            # self.assertEqual(session['logged_in'], True)
            # _, iws = BusinessOwner.find(phone_number=data[Keys.PHONE_NUMBER])
            # # dct = json.loads(response.data)
            # result = pbkdf2_sha256.verify(data[Keys.NEW_PASSWORD], iws[0].password)
            # self.assertTrue(result)

    def test_true_regex_info_exist_in_db(self):
        data = {
            Keys.OLD_PASSWORD: "Amish1234",
            Keys.NEW_PASSWORD: "Afsane1234",
            # "phone_number": '09125200780',
            Keys.TYPE_USER: Keys.BUSINESS_OWNER
        }

        data1 = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
                sess[Keys.PHONE_NUMBER] = '09125200100'
            response = self.make_post_request(data1)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 200)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.PASSWORD_CHANGE_SUCCESSFULLY)
            self.assertEqual(dct[Keys.PARAMS], None)
            self.assertEqual(session['user_id'], 1)
            _, iws = User.find(phone_number=session[Keys.PHONE_NUMBER])
            # dct = json.loads(response.data)
            result = pbkdf2_sha256.verify(data[Keys.NEW_PASSWORD], iws[0].password)
            self.assertTrue(result)

    def test_false_regex_new_password_exist_in_db_1(self):
        data = {
            Keys.OLD_PASSWORD: "Amish1234",
            Keys.NEW_PASSWORD: "h5h4hhhh",
            # 'phone_number': '09125200780',
            Keys.TYPE_USER: Keys.BUSINESS_OWNER
        }
        data1 = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
                sess[Keys.PHONE_NUMBER] = '09125200100'
            response = self.make_post_request(data1)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 400)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.BAD_SCHEMA)
            # self.assertEqual(dct[Keys.PARAMS], None)
            self.assertEqual(session['user_id'], 1)

            _, iws = User.find(phone_number=session[Keys.PHONE_NUMBER])
            # dct = json.loads(response.data)
            result = pbkdf2_sha256.verify(data[Keys.OLD_PASSWORD], iws[0].password)
            self.assertTrue(result)

    def test_false_regex_new_password_exist_in_db_2(self):
        data = {
            Keys.OLD_PASSWORD: "Amish1234",
            Keys.NEW_PASSWORD: "",
            # 'phone_number': '09125200780',
            Keys.TYPE_USER: Keys.BUSINESS_OWNER
        }
        data1 = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = True
                sess[Keys.PHONE_NUMBER] = '09125200100'
            response = self.make_post_request(data1)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 400)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.BAD_SCHEMA)
            # self.assertEqual(dct[Keys.PARAMS], None)
            self.assertEqual(session['user_id'], 1)

            _, iws = User.find(phone_number=session[Keys.PHONE_NUMBER])
            # dct = json.loads(response.data)
            result = pbkdf2_sha256.verify(data[Keys.OLD_PASSWORD], iws[0].password)
            self.assertTrue(result)

    def test_false_regex_new_password_exist_in_db_3(self):
        data = {
            Keys.OLD_PASSWORD: "Amish1234",
            # 'phone_number': '09125200780',
            Keys.TYPE_USER: Keys.BUSINESS_OWNER
        }
        data1 = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
                sess[Keys.PHONE_NUMBER] = '09125200100'
            response = self.make_post_request(data1)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 400)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.BAD_SCHEMA)
            # self.assertEqual(dct[Keys.PARAMS], None)
            self.assertEqual(session['user_id'], 1)

            _, iws = User.find(phone_number=session[Keys.PHONE_NUMBER])
            # dct = json.loads(response.data)
            result = pbkdf2_sha256.verify(data[Keys.OLD_PASSWORD], iws[0].password)
            self.assertTrue(result)

    def test_old_password_is_not_verified_1(self):
        data = {
            Keys.OLD_PASSWORD: "h5h4hhHH",
            Keys.NEW_PASSWORD: "Ah5h4hhhh",
            # 'phone_number': '09125200780',
            Keys.TYPE_USER: Keys.BUSINESS_OWNER
        }
        data1 = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = True
                sess[Keys.PHONE_NUMBER] = '09125200100'
            response = self.make_post_request(data1)
            dct = json.loads(response.data)
            print dct
            self.assertEqual(dct[Keys.STATUS], 404)
            self.assertEqual(dct[Keys.MESSAGE], MessagesKeys.OLD_PASSWORD_IS_NOT_VALID)
            self.assertEqual(dct[Keys.PARAMS], {"phone_number": session[Keys.PHONE_NUMBER]})
            self.assertEqual(session['user_id'], 1)

            _, iws = User.find(phone_number=session[Keys.PHONE_NUMBER])
            # dct = json.loads(response.data)
            result = pbkdf2_sha256.verify(data[Keys.NEW_PASSWORD], iws[0].password)
            self.assertFalse(result)

    def test_old_password_is_not_verified_2(self):
        data = {
            Keys.OLD_PASSWORD: "",
            Keys.NEW_PASSWORD: "Ah5h4hhhh",
            # 'phone_number': '09125200780',
            Keys.TYPE_USER: Keys.BUSINESS_OWNER
        }
        data1 = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
                sess[Keys.PHONE_NUMBER] = '09125200100'
            response = self.make_post_request(data1)
            dct = json.loads(response.data)
            print dct
            self.assertEqual(dct[Keys.STATUS], 400)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.BAD_SCHEMA)
            self.assertEqual(dct[Keys.PARAMS], {'invalid_params': ['password_is_not_strength']})
            self.assertEqual(session['user_id'], 1)

            _, iws = User.find(phone_number=session[Keys.PHONE_NUMBER])
            result = pbkdf2_sha256.verify(data[Keys.NEW_PASSWORD], iws[0].password)
            self.assertFalse(result)

    def test_old_password_is_not_verified_3(self):
        data = {
            Keys.OLD_PASSWORD: "Ah5h4hhhh",
            # 'phone_number': '09125200780',
            Keys.TYPE_USER: Keys.BUSINESS_OWNER
        }
        data1 = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = True
                sess[Keys.PHONE_NUMBER] = '09125200100'
            response = self.make_post_request(data1)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 400)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.BAD_SCHEMA)
            self.assertEqual(dct[Keys.PARAMS], [Result.language.MISSING_PASSWORD_IN_JSON])
            self.assertEqual(session['user_id'], 1)

            _, iws = User.find(phone_number=session[Keys.PHONE_NUMBER])
            # dct = json.loads(response.data)
            result = pbkdf2_sha256.verify(data[Keys.OLD_PASSWORD], iws[0].password)
            self.assertFalse(result)

    def test_old_password_is_not_verified_false_regex_new_password_1(self):
        data = {
            Keys.OLD_PASSWORD: "h5h4hhHH",
            Keys.NEW_PASSWORD: "h5h4hhhh",
            # 'phone_number': '09125200780',
            Keys.TYPE_USER: Keys.BUSINESS_OWNER
        }
        data1 = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = True
                sess[Keys.PHONE_NUMBER] = '09125200100'
            response = self.make_post_request(data1)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 400)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.BAD_SCHEMA)
            self.assertEqual(dct[Keys.PARAMS], {'invalid_params': ['password_is_not_strength']})
            self.assertEqual(session['user_id'], 1)

            _, iws = User.find(phone_number=session[Keys.PHONE_NUMBER])
            # dct = json.loads(response.data)
            result = pbkdf2_sha256.verify(data[Keys.NEW_PASSWORD], iws[0].password)
            self.assertFalse(result)

    def test_false_regex_new_password_and_old_password_2(self):
        data = {
            Keys.OLD_PASSWORD: "",
            # 'phone_number': '09125200780',
            Keys.TYPE_USER: Keys.BUSINESS_OWNER
        }
        data1 = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
                sess[Keys.PHONE_NUMBER] = '09125200100'
            response = self.make_post_request(data1)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 400)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.BAD_SCHEMA)
            self.assertEqual(dct[Keys.PARAMS], [Result.language.MISSING_PASSWORD_IN_JSON])
            self.assertEqual(session['user_id'], 1)

            _, iws = User.find(phone_number=session[Keys.PHONE_NUMBER])
            # dct = json.loads(response.data)
            result = pbkdf2_sha256.verify(data[Keys.OLD_PASSWORD], iws[0].password)
            self.assertFalse(result)

    def test_false_regex_new_password_and_old_password_3(self):
        data = {
            # 'phone_number': '09125200780',
            Keys.TYPE_USER: Keys.BUSINESS_OWNER
        }
        data1 = json.dumps(data)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = True
                sess[Keys.PHONE_NUMBER] = '09125200100'
            response = self.make_post_request(data1)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 400)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.BAD_SCHEMA)
            # self.assertEqual(dct[Keys.PARAMS], [Result.language.MISSING_PASSWORD_IN_JSON])
            self.assertEqual(session['user_id'], True)

            # _, iws = BusinessOwner.find(phone_number=data['phone_number'])
            # # dct = json.loads(response.data)
            # result = pbkdf2_sha256.verify(data['new_password'], iws[0].password)
            # self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
