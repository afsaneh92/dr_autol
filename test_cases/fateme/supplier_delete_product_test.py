#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import unittest

from app import db, app
from config import DataBaseConfig
from core.messages.keys import Keys
from routers import supplier
from routers.admin import admin
from routers.authintication import authentication
from routers.car_owner import car_owner
from routers.choose_services import choose_service_grade
from routers.endpoints import Endpoints
from routers.index import index_route
from routers.supplier import suppliers
from test_cases.fill_db import init_db

TEST_DB = 'test.db'


class DeleteProductTest(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config[
            'SQLALCHEMY_DATABASE_URI'] = DataBaseConfig.DB_DIALECT + DataBaseConfig.USER_NAME + ':' + DataBaseConfig.PASSWORD + '@' + DataBaseConfig.SERVER_ADDRESS + ':' + DataBaseConfig.PORT + '/' + DataBaseConfig.DATABASE_NAME
        app.register_blueprint(index_route)
        app.register_blueprint(car_owner)
        app.register_blueprint(authentication)
        app.register_blueprint(admin)
        app.register_blueprint(choose_service_grade)
        app.register_blueprint(suppliers)

        self.app = app.test_client()
        if self._testMethodName == "test_no_db":
            db.drop_all()
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

    def test_delete_product(self):
        update_date = {
            'product_id': 1,
        }
        json_obj = json.dumps(update_date)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 7
                sess[Keys.PHONE_NUMBER] = "09125200101"
                sess[Keys.TYPE_USER] = 'SupplierUser'
            response = client.delete(Endpoints.DELETE_PRODUCT_INFO + '/' + str(update_date['product_id']),
                                     data=json_obj,
                                     content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 200)

    def test_supplier_delete_own_product(self):
        update_date = {
            'product_id': 1,
        }
        json_obj = json.dumps(update_date)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 8
                sess[Keys.PHONE_NUMBER] = "09125200111"
                sess[Keys.TYPE_USER] = 'SupplierUser'
            response = client.delete(Endpoints.DELETE_PRODUCT_INFO + '/' + str(update_date['product_id']),
                                     data=json_obj,
                                     content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_product_is_exist(self):
        update_date = {
            'product_id': 12,
        }
        json_obj = json.dumps(update_date)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 8
                sess[Keys.PHONE_NUMBER] = "09125200111"
                sess[Keys.TYPE_USER] = 'SupplierUser'
            response = client.delete(Endpoints.DELETE_PRODUCT_INFO + '/' + str(update_date['product_id']),
                                     data=json_obj,
                                     content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_no_db(self):
        update_date = {
            'product_id': 1,
        }

        json_obj = json.dumps(update_date)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 7
                sess[Keys.PHONE_NUMBER] = "09125200101"
                sess[Keys.TYPE_USER] = 'SupplierUser'
            response = client.delete(Endpoints.DELETE_PRODUCT_INFO + '/' + str(update_date['product_id']),
                                     data=json_obj,
                                     content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 500)


if __name__ == '__main__':
    unittest.main()
