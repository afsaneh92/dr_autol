#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import unittest

from app import db, app
from config import DataBaseConfig
from core.messages.keys import Keys
from routers.admin import admin
from routers.authintication import authentication
from routers.car_owner import car_owner
from routers.choose_services import choose_service_grade
from routers.endpoints import Endpoints
from routers.index import index_route
from routers.supplier import suppliers
from test_cases.fill_db import init_db

TEST_DB = 'test.db'


class AddProductTest(unittest.TestCase):
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

        # db.drop_all()
        # init_db()

        # Disable sending emails during unit testing
        # self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_add_new_product_with_description(self):
        update_date = {
            'sub_category_id': 1,
            'company_id': 2,
            'brand_id': 1,
            'code': '45666',
            'price': 10000,
            'description': "سایران هر روز بهتر از دیروز دینگ دینگ. ",
            'minimum_order': 200
        }
        json_obj = json.dumps(update_date)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 7
                sess[Keys.PHONE_NUMBER] = "09125200101"
                sess[Keys.TYPE_USER] = 'SupplierUser'
            response = client.post(Endpoints.ADD_NEW_PRODUCT, data=json_obj,
                                   content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 200)

    def test_add_new_product_without_description(self):
        update_date = {
            'sub_category_id': 2,
            'company_id': 2,
            'brand_id': 1,
            'code': '456678',
            'price': 10000,
            'minimum_order': 200

        }
        json_obj = json.dumps(update_date)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 7
                sess[Keys.PHONE_NUMBER] = "09125200101"
                sess[Keys.TYPE_USER] = 'SupplierUser'
            response = client.post(Endpoints.ADD_NEW_PRODUCT, data=json_obj,
                                   content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 200)

    def test_supplier_add_one_product_twice(self):
        update_date = {
            'sub_category_id': 1,
            'company_id': 2,
            'brand_id': 1,
            'code': '45555',
            'price': 10000,
            'minimum_order': 200

        }
        json_obj = json.dumps(update_date)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 7
                sess[Keys.PHONE_NUMBER] = "09125200101"
                sess[Keys.TYPE_USER] = 'SupplierUser'
            response = client.post(Endpoints.ADD_NEW_PRODUCT, data=json_obj,
                                   content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_supplier_is_exist(self):
        update_date = {
            'sub_category_id': 1,
            'company_id': 2,
            'brand_id': 1,
            'code': '45555',
            'price': 10000,
            'minimum_order': 200
        }
        json_obj = json.dumps(update_date)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 7
                sess[Keys.PHONE_NUMBER] = "09195200101"
                sess[Keys.TYPE_USER] = 'SupplierUser'
            response = client.post(Endpoints.ADD_NEW_PRODUCT, data=json_obj,
                                   content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_user_is_not_supplier(self):
        update_date = {
            'sub_category_id': 1,
            'company_id': 2,
            'brand_id': 1,
            'code': '45555',
            'price': 10000,
            'minimum_order': 200

        }
        json_obj = json.dumps(update_date)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 1
                sess[Keys.PHONE_NUMBER] = "09125200100"
                sess[Keys.TYPE_USER] = 'SupplierUser'
            response = client.post(Endpoints.ADD_NEW_PRODUCT, data=json_obj,
                                   content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_company_is_exist(self):
        update_date = {
            'sub_category_id': 1,
            'company_id': 12,
            'brand_id': 1,
            'code': '45555',
            'price': 10000,
            'minimum_order': 200

        }
        json_obj = json.dumps(update_date)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 7
                sess[Keys.PHONE_NUMBER] = "09125200101"
                sess[Keys.TYPE_USER] = 'SupplierUser'
            response = client.post(Endpoints.ADD_NEW_PRODUCT, data=json_obj,
                                   content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_brand_is_exist(self):
        update_date = {
            'sub_category_id': 1,
            'company_id': 1,
            'brand_id': 12,
            'code': '45555',
            'price': 10000,
            'minimum_order': 200

        }
        json_obj = json.dumps(update_date)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 7
                sess[Keys.PHONE_NUMBER] = "09125200101"
                sess[Keys.TYPE_USER] = 'SupplierUser'
            response = client.post(Endpoints.ADD_NEW_PRODUCT, data=json_obj,
                                   content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_are_company_and_brand_match(self):
        update_date = {
            'sub_category_id': 1,
            'company_id': 1,
            'brand_id': 2,
            'code': '45555',
            'price': 10000,
            'minimum_order': 200

        }
        json_obj = json.dumps(update_date)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 7
                sess[Keys.PHONE_NUMBER] = "09125200101"
                sess[Keys.TYPE_USER] = 'SupplierUser'
            response = client.post(Endpoints.ADD_NEW_PRODUCT, data=json_obj,
                                   content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_bad_schema(self):
        update_date = {
            'sub_category_id': 1,
            'brand_id': 1,
            'code': '985555',
            'price': 10000,
            'minimum_order': 200

        }
        json_obj = json.dumps(update_date)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 7
                sess[Keys.PHONE_NUMBER] = "09125200101"
                sess[Keys.TYPE_USER] = 'SupplierUser'

            response = client.post(Endpoints.ADD_NEW_PRODUCT, data=json_obj,
                                   content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 400)

    def test_no_db(self):

        update_date = {
            'sub_category_id': 1,
            'company_id': 2,
            'brand_id': 1,
            'code': '45666',
            'price': 10000,
            'description': "سایران هر روز بهتر از دیروز دینگ دینگ. ",
            'minimum_order': 200

        }

        json_obj = json.dumps(update_date)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 7
                sess[Keys.PHONE_NUMBER] = "09125200101"
                sess[Keys.TYPE_USER] = 'SupplierUser'
            response = client.post(Endpoints.ADD_NEW_PRODUCT, data=json_obj,
                                   content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 500)


if __name__ == '__main__':
    unittest.main()
