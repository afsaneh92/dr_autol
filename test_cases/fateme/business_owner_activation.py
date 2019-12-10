import json
from app import db, app
from config import DataBaseConfig
from core.messages.keys import Keys
from persistence.database.entity.user.business_owner import BusinessOwner
from routers.admin import admin
from routers.authintication import authentication
from routers.business_owner import business_owner
from routers.choose_services import choose_service_grade
from routers.index import index_route
from test_cases.fill_db import init_db
import unittest
from routers.endpoints import Endpoints
from test_cases.test_keys import TestKeys


class TestActivateBusinessOwner(unittest.TestCase):
    # executed prior to each test

    def setUp(self):
        app.config[TestKeys.TESTING] = True
        app.config[TestKeys.WTF_CSRF_ENABLED] = False
        app.config[TestKeys.DEBUG] = False
        app.config[
            TestKeys.SQLALCHEMY_DATABASE_URI] = DataBaseConfig. \
                                                    DB_DIALECT + DataBaseConfig. \
                                                    USER_NAME + ':' + DataBaseConfig. \
                                                    PASSWORD + '@' + DataBaseConfig. \
                                                    SERVER_ADDRESS + ':' + DataBaseConfig. \
                                                    PORT + '/' + DataBaseConfig. \
                                                    DATABASE_NAME
        app.register_blueprint(index_route)
        app.register_blueprint(business_owner)
        app.register_blueprint(authentication)
        app.register_blueprint(admin)
        app.register_blueprint(choose_service_grade)

        self.app = app.test_client()

        if self._testMethodName == TestKeys.TEST_NO_DB:
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

    def test_bad_schema(self):
        data = {
            TestKeys.BUSINESS_OWNER_ID_WRONG_FORMAT: 10,
        }

        json_obj = json.dumps(data)

        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 1
            response = client.put(Endpoints.ACTIVATE_BUSINESS_OWNER, data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            print response.data
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 400)

    def test_is_not_job_in_business_owner_todo_list(self):
        data_found = {
            'business_owner_id': 3
        }
        json_obj_found = json.dumps(data_found)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 1
            response = client.put(Endpoints.ACTIVATE_BUSINESS_OWNER, data=json_obj_found,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 200)

    def test_is_job_in_business_owner_todo_list(self):
        data_found = {
            Keys.BUSINESS_OWNER_ID: 6
        }
        json_obj_found = json.dumps(data_found)
        with self.app as client:
            with client.session_transaction() as sess:
                sess[Keys.USER_ID] = 1
            response = client.put(Endpoints.ACTIVATE_BUSINESS_OWNER, data=json_obj_found,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_change_status(self):
        data_found = {
            Keys.BUSINESS_OWNER_ID: 1,
        }

        json_obj_found = json.dumps(data_found)
        find_status_by_id = BusinessOwner.query.filter_by(id=1).first()
        first_status_found = find_status_by_id.flags[Keys.ACTIVATION_STATUS]

        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = client.put(Endpoints.ACTIVATE_BUSINESS_OWNER, data=json_obj_found,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)

            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 200)
            new_status_query = BusinessOwner.query.filter_by(id=data_found[Keys.BUSINESS_OWNER_ID]).first()
            new_status = new_status_query.flags[Keys.ACTIVATION_STATUS]
            self.assertEqual(not first_status_found, new_status)

    def test_change_status_wrong_format(self):
        data_not_found = {
            Keys.BUSINESS_OWNER_ID: 11111,
        }
        json_obj_not_found = json.dumps(data_not_found)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = client.put(Endpoints.ACTIVATE_BUSINESS_OWNER, data=json_obj_not_found,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 404)

    def test_no_db(self):
        data = {
            Keys.BUSINESS_OWNER_ID: 1,
        }
        json_obj = json.dumps(data)

        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = client.put(Endpoints.ACTIVATE_BUSINESS_OWNER, data=json_obj,
                                  content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            print(response.data)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 500)


if __name__ == '__main__':
    unittest.main()
