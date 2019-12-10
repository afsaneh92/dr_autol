#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import unittest

from app import db, app
from config import DataBaseConfig
from core.messages.keys import Keys
from routers.authintication import authentication
from routers.endpoints import Endpoints
from routers.index import index_route
from routers.supplier import suppliers
from test_cases.fill_db import init_db

TEST_DB = 'test.db'


class TestSearchOnProductTest(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config[
            'SQLALCHEMY_DATABASE_URI'] = DataBaseConfig.DB_DIALECT + DataBaseConfig.USER_NAME + ':' + DataBaseConfig.PASSWORD + '@' + DataBaseConfig.SERVER_ADDRESS + ':' + DataBaseConfig.PORT + '/' + DataBaseConfig.DATABASE_NAME
        app.register_blueprint(index_route)
        app.register_blueprint(authentication)
        app.register_blueprint(suppliers)

        self.app = app.test_client()
        if self._testMethodName == "test_no_db":
            db.drop_all()
        else:
            db.drop_all()
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

    def test_get_list_of_selected_products1(self):
        update_date = {
            'options': {
                'min_price': 1000,
                'max_price': 20000
            }
        }
        json_obj = json.dumps(update_date)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 7
                sess[Keys.PHONE_NUMBER] = "09125200101"
                sess[Keys.TYPE_USER] = 'SupplierUser'
            response = client.get(Endpoints.SEARCH_FOR_PRODUCT,
                                  data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 200)

    def test_get_list_of_selected_products2(self):
        update_date = {
            'options': {
                'supplier_status_id': 4,
                'accepted_number': 0
            }
        }
        json_obj = json.dumps(update_date)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 7
                sess[Keys.PHONE_NUMBER] = "09125200101"
                sess[Keys.TYPE_USER] = 'SupplierUser'
            response = client.get(Endpoints.SEARCH_FOR_PRODUCT,
                                  data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 200)

    def test_get_list_of_selected_products3(self):
        update_date = {
            'options': {
                'accepted_number': 7,
            }
        }
        json_obj = json.dumps(update_date)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 8
                sess[Keys.PHONE_NUMBER] = "09125200111"
                sess[Keys.TYPE_USER] = 'SupplierUser'
            response = client.get(Endpoints.SEARCH_FOR_PRODUCT,
                                  data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 200)

    def test_there_is_not_such_product(self):
        update_date = {
            'options': {
                'brand_id': 8,
                'minimum_order': 120
            }
        }
        json_obj = json.dumps(update_date)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 8
                sess[Keys.PHONE_NUMBER] = "09125200111"
                sess[Keys.TYPE_USER] = 'SupplierUser'
            response = client.get(Endpoints.SEARCH_FOR_PRODUCT,
                                  data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_supplier_is_not_exist(self):
        update_date = {
            'options': {
                'brand_id': 8,
                'minimum_order': 3
            }
        }
        json_obj = json.dumps(update_date)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 1
                sess[Keys.PHONE_NUMBER] = "09145200114"
                sess[Keys.TYPE_USER] = 'SupplierUser'
            response = client.get(Endpoints.SEARCH_FOR_PRODUCT,
                                  data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_bad_schema(self):
        update_date = {

            'brand_id': 8,
            'minimum_order': 120

        }
        json_obj = json.dumps(update_date)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 8
                sess[Keys.PHONE_NUMBER] = "09125200111"
                sess[Keys.TYPE_USER] = 'SupplierUser'
            response = client.get(Endpoints.SEARCH_FOR_PRODUCT,
                                  data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 400)

    def test_no_db(self):
        update_date = {
            'options': {
                'brand_id': 2,
                'minimum_order': 120
            }
        }
        json_obj = json.dumps(update_date)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 8
                sess[Keys.PHONE_NUMBER] = "09125200111"
                sess[Keys.TYPE_USER] = 'SupplierUser'
            response = client.get(Endpoints.SEARCH_FOR_PRODUCT,
                                  data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 500)


if __name__ == '__main__':
    unittest.main()
