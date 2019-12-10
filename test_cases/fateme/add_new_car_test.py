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
from test_cases.fill_db import init_db

TEST_DB = 'test.db'


class AddCarTest(unittest.TestCase):
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

        self.app = app.test_client()
        if self._testMethodName == "test_no_db":
            db.drop_all()
        else:
            db.drop_all()
            db.create_all()

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

    def test_get_list_of_consumable_items_for_an_auto_type(self):
        update_data = {
            'car_owner': "4",
            'car_info': {

                'vin_number': 'iRFC93R21SN497648',
                'plate_number': '77ط749-33',
                'auto_type': '1',
                'color': '3',
                'auto_model': '1',
                'current_kilometer': '20000'}}

        json_obj = json.dumps(update_data)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 1
                sess[Keys.PHONE_NUMBER] = "09125200202"
                sess[Keys.TYPE_USER] = 'CarOwnerUser'
            response = client.post('/car_owner/cars', data=json_obj,
                                   content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 200)

    def test_bad_schema(self):
        update_data = {
            'car_owner': "4",
            'car_info': {

                'vin_number': 'iRFC93R21SN497648',
                'plate_number': '77ط749-33',
                'auto_type': '1',
                'current_kilometer': '20000'}}

        json_obj = json.dumps(update_data)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 1
                sess[Keys.PHONE_NUMBER] = "09125200202"
                sess[Keys.TYPE_USER] = 'CarOwnerUser'
            response = client.post('/car_owner/cars', data=json_obj,
                                   content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 400)

    def test_no_db(self):
        update_data = {
            'car_owner': "4",
            'car_info': {

                'vin_number': 'iRFC93R21SN497648',
                'plate_number': '77ط749-33',
                'auto_type': '1',
                'color': '3',
                'auto_model': '2',
                'current_kilometer': '20000'}}

        json_obj = json.dumps(update_data)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 1
                # sess[Keys.PHONE_NUMBER] = "09125200202"
                # sess[Keys.TYPE_USER] = 'CarOwnerUser'
            response = client.post('/car_owner/cars', data=json_obj,
                                   content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 500)

    def test_auto_type_and_auto_model_are_matched_false(self):
        update_data = {
            'car_owner': "4",
            'car_info': {

                'vin_number': 'iRFC93R21SN497648',
                'plate_number': '77ط749-33',
                'auto_type': '1',
                'color': '3',
                'auto_model': '2',
                'current_kilometer': '20000'}}

        json_obj = json.dumps(update_data)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 1
                sess[Keys.PHONE_NUMBER] = "09125200202"
                sess[Keys.TYPE_USER] = 'CarOwnerUser'
            response = client.post('/car_owner/cars', data=json_obj,
                                   content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_car_is_registered_false(self):
        update_data = {
            'car_owner': "4",
            'car_info': {
                'vin_number': 'iRFC93R21SN497640',
                'plate_number': '70ط749-33',
                'auto_type': '1',
                'color': '3',
                'auto_model': '2',
                'current_kilometer': '20000'}
        }

        json_obj = json.dumps(update_data)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 1
                sess[Keys.PHONE_NUMBER] = "09125200202"
                sess[Keys.TYPE_USER] = 'CarOwnerUser'
            response = client.post('/car_owner/cars', data=json_obj,
                                   content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)


if __name__ == '__main__':
    unittest.main()
