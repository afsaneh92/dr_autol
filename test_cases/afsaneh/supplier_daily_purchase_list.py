#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from flask import json, session

from app import db, app
from config import DataBaseConfig
from core.messages import HttpStatus
from core.messages.keys import Keys
from core.result import Result
from persistence.database.entity.user.supplier import Supplier
from routers.endpoints import Endpoints
from routers.supplier import suppliers
from test_cases.fill_db import init_db


class MyTestCase(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config[
            'SQLALCHEMY_DATABASE_URI'] = DataBaseConfig.DB_DIALECT + DataBaseConfig.USER_NAME + ':' + DataBaseConfig.PASSWORD + '@' + DataBaseConfig.SERVER_ADDRESS + ':' + DataBaseConfig.PORT + '/' + DataBaseConfig.DATABASE_NAME
        # app.register_blueprint(authentication)
        app.register_blueprint(suppliers)
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

    def make_get_request(self):
        res = self.app.get(Endpoints.SUPPLIER_DAILY_PURCHASE_LIST,
                           content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
        return res

    def test_return_daily_list_true(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 11
                sess[Keys.PHONE_NUMBER] = '09125200101'
            response = self.make_get_request()
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], HttpStatus.OK)
            # self.assertEqual(dct[Keys.PARAMS],  )
            self.assertEqual(dct[Keys.MESSAGE], Result.language.SUCCESS_LIST)
            self.assertItemsEqual(dct[Keys.PARAMS], [{
                Keys.PRODUCT_ID: 1,
                Keys.NUMBER: 0,
                Keys.PRICE: u'10000',
                Keys.BUSINESS_OWNER_ID: 3,
                Keys.ORDER_ID: 2,
                Keys.CODE: u'45555',
                Keys.COMPANY: u'10w40',
                Keys.NAME: u'آینه'
            }])

    def test_daily_list_false_regex_session(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = "10"
                sess[Keys.PHONE_NUMBER] = '09125200113'
            response = self.make_get_request()
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], HttpStatus.BAD_REQUEST)
            self.assertEqual(dct[Keys.PARAMS], Result.language.ID_IS_NOT_INTEGER)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.BAD_SCHEMA)

    def test_daily_list_not_registered_supplier(self):
        supplier = Supplier(phone_number="09125200113", password="Amish1234", name='Afsane',
                            business_license='0987654321',
                            address='تهران خیابان شهید بهشتی', validate=True)
        result = supplier.add(db)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 14
                sess[Keys.PHONE_NUMBER] = '09125200114'
            response = self.make_get_request()
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], HttpStatus.NOT_FOUND)
            self.assertEqual(dct[Keys.PARAMS], None)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.ID_IS_NOT_IN_DB)

    def test_daily_list_not_found_order_item(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 12
                sess[Keys.PHONE_NUMBER] = '09125200111'
            response = self.make_get_request()
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], HttpStatus.NOT_FOUND)
            self.assertEqual(dct[Keys.PARAMS], None)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.NOT_FOUND_ORDER_ITEM)


if __name__ == '__main__':
    unittest.main()
