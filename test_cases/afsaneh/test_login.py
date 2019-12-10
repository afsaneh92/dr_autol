#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
9 (9) As a car owner I want to choose a service(common, plus, premium) So that my car needs to fix
"""

import json
import unittest


from app import db, app
from persistence.database.entity.service_grade import ServiceGrade
from persistence.database.entity.service_type import ServiceType
from routers.admin import admin
from routers.authintication import authentication
from routers.car_owner import car_owner
from routers.choose_services import choose_service_grade
from routers.index import index_route

TEST_DB = 'test.db'


class ChooseServiceGradeTest(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config[
            'SQLALCHEMY_DATABASE_URI'] = r'sqlite:///D:\progs\drautol\car-history\test_cases\afsaneh\dr-autol-test.db?check_same_thread=False'
        app.register_blueprint(index_route)
        app.register_blueprint(car_owner)
        app.register_blueprint(authentication)
        app.register_blueprint(admin)
        app.register_blueprint(choose_service_grade)

        self.app = app.test_client()

        # db.drop_all()
        db.create_all()

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

    # def test_get_service_grade(self):
    #     list_returned = ServiceGrade.list_service_grades()
    #     list_returned1 = ServiceGrade.list_service_grades()
    #     self.assertEqual(list_returned[1], list_returned[1])
    #
    # def test_get_service_type_by_service_grade(self):
    #     list_returned = ServiceGrade.list_service_types(1)
    #     # list_returned[1][0][0].service_types[0].name
    #     self.assertEqual(list_returned[1], list_returned[1])
    #
    def test_return_service_grade_list(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['logged_in'] = True
            response = client.get('/services/service_grades', content_type='application/json')
            self.assertEqual(response.status_code, 200)

            response = client.post('/services/service_grades', content_type='application/json')
            self.assertEqual(response.status_code, 405)
    #
    # def test_add_new_service(self):
    #     grade = ServiceGrade(name="common")
    #     type_ = ServiceType(name="nothing")
    #     grade.service_types.append(type_)
    #     db.session.add(grade)
    #     db.session.commit()
    #     grades_list = ServiceGrade.list_service_grades()


    # def test_return_list_json(self):
    #     data = {
    #         "phone_number": "1",
    #         "password": "1",
    #         "name": "امیر",
    #         "user_type": "1"
    #     }
    #     json_obj = json.dumps(data)
    #     response = self.app.post('/car_owner/cars', data=json_obj, content_type='application/json')
    #     response = self.app.get('/car_owner/cars', follow_redirects=True)
    #     self.assertEqual(response.status_code, 405)
        # converter = JSONConverter()
        #
        # list_service_grades_controller = ListServiceGradesController(converter)
        # result = list_service_grades_controller.execute()
        # self.assertEqual(False, result)

if __name__ == '__main__':
    unittest.main()
