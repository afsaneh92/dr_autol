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


class UpdateProductTest(unittest.TestCase):
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
            db.drop_all()
            init_db()

        # db.drop_all()
        # init_db()

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

    def test_update_product_information_with_description(self):
        update_date = {
            'id': 1,
            'sub_category_id': 1,
            'company_id': 1,
            'brand_id': 1,
            'code': '45555',
            'price': 30000,
            'description': "سایران هر روز بهتر از دیروز دینگ دینگ. ",
            'minimum_order': 80000
        }
        json_obj = json.dumps(update_date)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 7
                sess[Keys.PHONE_NUMBER] = "09125200101"
                sess[Keys.TYPE_USER] = 'SupplierUser'
            response = client.put(Endpoints.EDIT_PRODUCT_INFO + '/' + str(update_date['id']), data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 200)

    def test_update_product_information_without_description(self):
        update_date = {
            'id': 1,
            'sub_category_id': 1,
            'company_id': 1,
            'brand_id': 1,
            'code': '45555',
            'price': 30000,
            'minimum_order': 80000
        }
        json_obj = json.dumps(update_date)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 7
                sess[Keys.PHONE_NUMBER] = "09125200101"
                sess[Keys.TYPE_USER] = 'SupplierUser'
            response = client.put(Endpoints.EDIT_PRODUCT_INFO + '/' + str(update_date['id']), data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 200)

    def test_supplier_update_own_product(self):
        update_date = {
            'id': 1,
            'sub_category_id': 1,
            'company_id': 1,
            'brand_id': 1,
            'code': '45555',
            'price': 30000,
            'description': "سایران هر روز بهتر از دیروز دینگ دینگ. ",
            'minimum_order': 80000
        }
        json_obj = json.dumps(update_date)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 8
                sess[Keys.PHONE_NUMBER] = "09125200111"
                sess[Keys.TYPE_USER] = 'SupplierUser'
            response = client.put(Endpoints.EDIT_PRODUCT_INFO + '/' + str(update_date['id']), data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_bad_schema(self):
        update_date = {
            'id': 1,
            'sub_category_id': 1,
            'brand_id': 1,
            'code': '985555',
            'price': 10000,
            'minimum_order': 80000
        }
        json_obj = json.dumps(update_date)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 7
                sess[Keys.PHONE_NUMBER] = "09125200101"
                sess[Keys.TYPE_USER] = 'SupplierUser'

            response = client.put(Endpoints.EDIT_PRODUCT_INFO + '/' + str(update_date['id']), data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 400)

    def test_no_db(self):

        update_date = {
            'id': 1,
            'sub_category_id': 1,
            'company_id': 1,
            'brand_id': 1,
            'code': '45555',
            'price': 30000,
            'description': "سایران هر روز بهتر از دیروز دینگ دینگ. ",
            'minimum_order': 80000
        }

        json_obj = json.dumps(update_date)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 7
                sess[Keys.PHONE_NUMBER] = "09125200101"
                sess[Keys.TYPE_USER] = 'SupplierUser'
            response = client.put(Endpoints.EDIT_PRODUCT_INFO + '/' + str(update_date['id']), data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 500)


if __name__ == '__main__':
    unittest.main()
