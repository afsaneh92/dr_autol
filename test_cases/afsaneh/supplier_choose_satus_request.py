# !/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import random
import unittest

from app import app, db
from config import DataBaseConfig
from core.messages.keys import Keys
from core.result import Result
from persistence.database.entity.order_items import OrderItem
from routers.endpoints import Endpoints
from routers.index import index_route
from routers.supplier import suppliers
from test_cases.fill_db import init_db


class ChooseAcceptDenyByBO(unittest.TestCase):
    # executed prior to each test
    def setUp(self):

        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config[
            'SQLALCHEMY_DATABASE_URI'] = DataBaseConfig.DB_DIALECT + DataBaseConfig.USER_NAME + ':' + DataBaseConfig.PASSWORD + '@' + DataBaseConfig.SERVER_ADDRESS + ':' + DataBaseConfig.PORT + '/' + DataBaseConfig.DATABASE_NAME
        app.register_blueprint(index_route)
        app.register_blueprint(suppliers)

        self.app = app.test_client()

        # db.create_all()
        if self._testMethodName == "test_no_db":
            db.drop_all()
        else:
            init_db()

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

    def _put_accept_deny_request(self, url, data):
        json_obj = json.dumps(data)

        response = self.app.put(url, data=json_obj, content_type='application/json')
        print(response.data)
        return response

    def _test_choose_order_request(self, data, expected_response, expected_message, expected_status_id,
                                   expected_params=None):
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 11
            response = self._put_accept_deny_request(Endpoints.SUPPLIER_CHANGE_ORDER_STATUS, data)
            response_dict = json.loads(response.data)
            self.assertEqual(expected_response, response.status_code)
            self.assertEqual(expected_message, response_dict[Keys.MESSAGE])
            if expected_params is not None:
                self.assertEqual(expected_params, response_dict[Keys.PARAMS])
            if self._testMethodName != "test_no_db" and self._testMethodName != "test_no_order" and self._testMethodName != "test_bad_schema":
                actual_stat = OrderItem.query.filter(OrderItem.id == data[Keys.ORDER_ID]). \
                    with_entities(OrderItem.supplier_status_id).first()[0]
                self.assertEqual(expected_status_id, actual_stat)

    def test_accept_order_successfully(self):
        data = {
            Keys.USER_TYPE: Keys.ACCEPT_ORDER_REQUEST,
            Keys.ORDER_ID: 4
        }
        self._test_choose_order_request(data, 200, Result.language.SUCCESS_ACCEPT_ORDER, 1)

    def test_deny_order_successfully(self):
        data = {
            Keys.USER_TYPE: Keys.DENY_ORDER_REQUEST,
            Keys.ORDER_ID: 4
        }
        self._test_choose_order_request(data, 200, Result.language.SUCCESS_ACCEPT_ORDER, 2)

    def test_no_order(self):
        arr = [Keys.DENY_ORDER_REQUEST, Keys.ACCEPT_ORDER_REQUEST]
        rand = random.randint(0, 1)
        data = {
            Keys.USER_TYPE: arr[rand],
            Keys.ORDER_ID: 11
        }
        self._test_choose_order_request(data, 404, Result.language.NOT_FOUND_ORDER_ITEM, 6)

    def test_bad_schema(self):
        data = {
            Keys.USER_TYPE: 'bad',
            Keys.ORDER_ID: 1
        }
        self._test_choose_order_request(data, 400, u'فرمت اطلاعات وارد شده اشتباه می باشد.', 5)

    def test_no_db(self):
        arr = [Keys.DENY_ORDER_REQUEST, Keys.ACCEPT_ORDER_REQUEST]
        rand = random.randint(0, 1)
        data = {
            Keys.USER_TYPE: arr[rand],
            Keys.ORDER_ID: 1
        }
        self._test_choose_order_request(data, 500, Result.language.SOMETHING_WENT_WRONG, 6)


if __name__ == '__main__':
    unittest.main()
