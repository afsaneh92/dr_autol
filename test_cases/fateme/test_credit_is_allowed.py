#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest

from app import db, app
from config import DataBaseConfig
from core.messages.keys import Keys
from persistence.database.entity.user.auto_service import AutoServiceBusinessOwner
from routers.admin import admin
from routers.authintication import authentication
from routers.car_owner import car_owner
from routers.choose_services import choose_service_grade
from routers.endpoints import Endpoints
from routers.index import index_route
from test_cases.fill_db import init_db

TEST_DB = 'test.db'


class ChooseServiceGradeTest(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config[
            'SQLALCHEMY_DATABASE_URI'] = DataBaseConfig.generate_database_uri()
        app.register_blueprint(index_route)
        app.register_blueprint(car_owner)
        app.register_blueprint(authentication)
        app.register_blueprint(admin)
        app.register_blueprint(choose_service_grade)

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

    def test_buy_more_than_allowed_credit(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 1
                sess[Keys.PHONE_NUMBER] = "09125200100"
                sess[Keys.TYPE_USER] = 'AutoServiceBusinessOwnerUser'
            response = client.get(Endpoints.GET_BUSINESS_OWNER_REST_OF_ALLOWED_CREDIT,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_allowed_credit(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 2
                sess[Keys.PHONE_NUMBER] = "09125200102"
                sess[Keys.TYPE_USER] = 'AutoServiceBusinessOwnerUser'
            response = client.get(Endpoints.GET_BUSINESS_OWNER_REST_OF_ALLOWED_CREDIT,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 200)

    def test_no_such_a_data_in_excel_file(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 1
                sess[Keys.PHONE_NUMBER] = "09125200104"
                sess[Keys.TYPE_USER] = 'AutoServiceBusinessOwnerUser'
            response = client.get(Endpoints.GET_BUSINESS_OWNER_REST_OF_ALLOWED_CREDIT,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_not_exist_user(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 12
                sess[Keys.PHONE_NUMBER] = "09125200112"
                sess[Keys.TYPE_USER] = 'AutoServiceBusinessOwnerUser'
            response = client.get(Endpoints.GET_BUSINESS_OWNER_REST_OF_ALLOWED_CREDIT,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_order_list_is_empty(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 3
                sess[Keys.PHONE_NUMBER] = "09125200103"
                sess[Keys.TYPE_USER] = 'AutoServiceBusinessOwnerUser'
            response = client.get(Endpoints.GET_BUSINESS_OWNER_REST_OF_ALLOWED_CREDIT,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_no_db(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 3
                sess[Keys.PHONE_NUMBER] = "09125200102"
                sess[Keys.TYPE_USER] = 'AutoServiceBusinessOwnerUser'
            response = client.get(Endpoints.GET_BUSINESS_OWNER_REST_OF_ALLOWED_CREDIT,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 500)


if __name__ == '__main__':
    unittest.main()
