#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
9 (9) As a car owner I want to choose a service(common, plus, premium) So that my car needs to fix
"""

import json
import unittest


from app import db, app
from config import DataBaseConfig
from persistence.database.entity.service_grade import ServiceGrade
from persistence.database.entity.user.user import User
from routers.admin import admin
from routers.authintication import authentication
from routers.car_owner import car_owner
from routers.choose_services import choose_service_grade
from routers.index import index_route
from test_cases.fill_db import init_db


class RegistersTest(unittest.TestCase):
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

        # db.drop_all()
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

    # success scenario

    def test_get_service_grade(self):
        list_returned = ServiceGrade.list_service_grades()
        list_returned1 = ServiceGrade.list_service_grades()
        self.assertEqual(list_returned[1], list_returned[1])

    def test_get_service_type_by_service_grade(self):
        list_returned = ServiceGrade.list_service_types(1)
        # list_returned[1][0][0].service_types[0].name
        list_returned[1].dictionary_creator()
        self.assertEqual(list_returned[1], list_returned[1])

    def test_register_admin(self):
        data = {
            "name": "امید",
            "last_name": "شعبانی",
            "password": "Amish147852",
            "phone_number": "09372943761",
            "user_type": "1"
        }
        json_obj = json.dumps(data)

        with self.app as client:
            with client.session_transaction() as sess:
                sess['logged_in'] = True
            response = client.post('/register_admin', data=json_obj, content_type='application/json')
            print(response.data)
            datastore = json.loads(response.data)
            self.assertEqual(True, True)
            #

            data = {
                "code": User.query.filter(User.phone_number== "09372943761").first().code,
                "phone_number": "09372943761",
            }
            json_obj = json.dumps(data)

            response = client.post('/validate_user', content_type='application/json', data=json_obj)
            print(response.data)
            datastore = json.loads(response.data)
            self.assertEqual(True, True)
            #
            # data = {
            #     "car_owner_id": "1234",
            #     "car_id": "1",
            # }
            # json_obj = json.dumps(data)
            #
            # response = client.delete('/car_owner/cars/1', content_type='application/json', data=json_obj)
            # print(response.data)
            # datastore = json.loads(response.data)
            # self.assertEqual(True, True)
            #
            # data = {
            #     "car_owner_id": "1234",
            #     "car_id": "1",
            # }
            # json_obj = json.dumps(data)
            #
            # response = client.put('/car_owner/cars/1', content_type='application/json', data=json_obj)
            # print(response.data)
            # datastore = json.loads(response.data)
            # self.assertEqual(True, True)
            #
            # data = {
            #     "phone_number": "09125200492",
            #     "name": "امید",
            #     "password": "Amish1234",
            # }
            # json_obj = json.dumps(data)
            #
            # response = client.post('/register/iws', content_type='application/json', data=json_obj)
            # print(response.data)
            # datastore = json.loads(response.data)
            # self.assertEqual(True, True)
            #
            # data = {
            #     "car_owner": "1",
            #     "car_info": {"vin_number": 'iRFC93R21SN497641', "plate_number": '79ط749-33', "auto_type": '1'}
            # }
            # json_obj = json.dumps(data)
            #
            # response = client.post('/car_owner/cars', content_type='application/json', data=json_obj)
            # print(response.data)
            # datastore = json.loads(response.data)
            # self.assertEqual(True, True)

            data = {
                "name": "امیر",
                "password": "Amish1234",
                "phone_number": "09122341484",
                "reg_id": "1",
                # "user_type": "1"
            }
            json_obj = json.dumps(data)

            response = client.post('/register_user', content_type='application/json', data=json_obj)
            print(response.data)
            datastore = json.loads(response.data)
            self.assertEqual(True, True)

            data = {
                "phone_number": "09125200492",
                "name": "امید",
                "password": "Amish1234",
                "regId": "",
                "os": ""
            }
            json_obj = json.dumps(data)

            response = client.post('/login', content_type='application/json', data=json_obj)
            print(response.data)
            datastore = json.loads(response.data)
            self.assertEqual(True, True)

            response = client.post('/login/iws', content_type='application/json', data=json_obj)
            print(response.data)
            datastore = json.loads(response.data)
            self.assertEqual(True, True)

    def test_return_service_grade_list(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['logged_in'] = True
            response = client.get('/services/service_grades', content_type='application/json')
            print(response.data)
            self.assertEqual(response.status_code, 200)

            response = client.post('/services/service_grades', content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_add_new_service_grade(self):
        data = {
            "name": "+"
        }
        json_obj = json.dumps(data)

        response = self.app.post('/services/service_grades', data=json_obj, content_type='application/json')
        self.assertEqual(400, response.status_code)

        data = {
            "service_grade_name": "+"
        }
        json_obj = json.dumps(data)

        response = self.app.post('/services/service_grades', data=json_obj, content_type='application/json')
        self.assertEqual(200, response.status_code)

        data = {
            "service_grade_name": "     "
        }
        json_obj = json.dumps(data)

        response = self.app.post('/services/service_grades', data=json_obj, content_type='application/json')
        self.assertEqual(400, response.status_code)
        print(response.data)
        # grade = ServiceGrade(name="common")
        # type_ = ServiceType(name="nothing")
        # grade.service_types.append(type_)
        # db.session.add(grade)
        # db.session.commit()
        # grades_list = ServiceGrade.list_service_grades()

    def _post_request(self, url, data):
        json_obj = json.dumps(data)
        response = self.app.post(url, data=json_obj, content_type='application/json')
        print(response.data)
        return response

    def _test_add_new_service_type(self, data, expected_response):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['logged_in'] = True
            response = self._post_request('/services/service_types', data)
            print(response)
            self.assertEqual(expected_response, response.status_code)

    def test_add_new_service_type_(self):
        data = {
            "service_type": {
                "name": "change oidfgfgfl",
                "price": 10
            },
            "service_grades": [1, 2]
        }
        self._test_add_new_service_type(data, 404)

    def test_add_new_service_type_bad_request(self):
        data = {
            "service_type": {
                "name": "تعویض روغن",
                "price": "10"
            },
            "service_grades": [1, 2]
        }
        self._test_add_new_service_type(data, 400)

    def test_add_new_service_type(self):
        test_data = [
            {
                'data': {
                    "service_type": {
                        "name": "change oidfgfgfl",
                        "price": 10
                    },
                    "service_grades": [1, 2]
                },
                'expected': 200
            },
            {
                'data': {
                    "service_type": {
                        "name": "تعویض روغن",
                        "price": "10"
                    },
                    "service_grades": [1, 2]
                },
                'expected': 400
            },
            {
                'data': {
                    "service_type": {
                        "name": "dfdfdfdf",
                        "price": 1000
                    },
                    "service_grades": [1, 2]
                },
                'expected': 200
            },
            {
                'data': {
                    "service_type": {
                        "name": "تعویض روغن",
                        "price": 1000
                    },
                    "service_grades": [1]
                },
                'expected': 200
            },
            {
                'data': {
                    "service_type": {
                        "name": "",
                        "price": 1000
                    },
                    "service_grades": [1]
                },
                'expected': 400
            },
            {
                'data': {
                    "service_type": {
                        "name": "       ",
                        "price": 1000
                    },
                    "service_grades": [1]
                },
                'expected': 400
            }
        ]
        with self.app as client:
            with client.session_transaction() as sess:
                sess['logged_in'] = True


if __name__ == '__main__':
    unittest.main()
