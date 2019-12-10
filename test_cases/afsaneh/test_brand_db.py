#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from flask import json

from app import app, db
from config import DataBaseConfig
from core.controller.business_owner.job_process_statuses.finish_request import FinishJobRequestController
from core.interfaces.Convertible import JSONConverter
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result import Result
# from persistence.database.entity import service_definition
from persistence.database.entity.brand import Brand
from persistence.database.entity.calendar import Calendar
from persistence.database.entity.car import Car
from persistence.database.entity.car_owner import CarOwners
from persistence.database.entity.job_.job import Job
from persistence.database.entity.service_definition import ServicesDefinition
from persistence.database.entity.service_definition_brand import ServicesDefinitionBrands
from persistence.database.entity.user.user import User
from routers.admin import admin
from routers.authintication import authentication
from routers.business_owner import business_owner
from routers.car_owner import car_owner
from routers.choose_services import choose_service_grade
from routers.endpoints import Endpoints
from routers.index import index_route
from test_cases.fill_db import init_db


class MyTestCase(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config[
            'SQLALCHEMY_DATABASE_URI'] = DataBaseConfig.DB_DIALECT + DataBaseConfig.USER_NAME + ':' + DataBaseConfig.PASSWORD + '@' + DataBaseConfig.SERVER_ADDRESS + ':' + DataBaseConfig.PORT + '/' + DataBaseConfig.DATABASE_NAME
        app.register_blueprint(authentication)
        app.register_blueprint(admin)

        app.register_blueprint(index_route)

        app.register_blueprint(business_owner)
        app.register_blueprint(authentication)
        app.register_blueprint(car_owner)
        app.register_blueprint(choose_service_grade)

        self.app = app.test_client()
        # init_db()
        # if self._testMethodName == "test_no_db":
        # db.drop_all()
        #
        db.drop_all()
        # # db.create_all()
        # else:
        #     # pass
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

    def make_post_request(self, data1):
        res = self.app.get(Endpoints.PAYABLE_LIST, data=data1, content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
        return res

    def test_add_brand(self):
        brand = Brand(brand_name='gtXX', product_name='10w40', price=66000)
        result = brand.add(db, brand)
        self.assertEqual(result[0], True)
        res = brand.load_brand(brand_name='gtXX')
        self.assertEqual(res[0], True)
        self.assertEqual(len(res[1]), 1)

    def test_add_service_definition_with_brand(self):
        brand = Brand(brand_name='gttXX', product_name='10w40', price=66)
        result = brand.add(db, brand)
        service_definition = ServicesDefinition(service_grade="PREMUM", service_type="change oil",
                                                service_category='AutoService', pay=1000)
        res = service_definition.add_with_brand(db, brand, service_definition)
        self.assertEqual(res[0], True)
        self.assertEqual(len(res[1]), 1)

    def test_add_service_definition_without_brand(self):
        service_definition = ServicesDefinition(service_grade="++", service_type="change oil",
                                                service_category='AutoService', pay=10000)
        res = service_definition.add_without_brand(db, service_definition)
        self.assertEqual(res[0], True)
        self.assertEqual(res[1].status, 200)

    def test_update_service_definition_true(self):
        # service_definition = ServicesDefinition(service_grade="+", service_type="change oil",
        #                                         service_category='AutoService', pay=1000, id=1)
        service_definition = ServicesDefinition.query.filter_by(id=1).first()
        # service_definition1 = service_definition.load_service(service_grade="+")
        # self.id = service_definition1[1][0].id
        data = {"service_grade": "معمولی"}
        response = service_definition.update(db, data)
        print response
        self.assertEqual(response[0], True)
        self.assertEqual(response[1].status, 200)
        self.assertEqual(response[1].message, MessagesKeys.SUCCESS_UPDATE)

    def test_update_sd_brande_id_append_true(self):
        service_definition = ServicesDefinition(service_grade="+", service_type="change oil",
                                                service_category='AutoService', pay=1000)
        # service_definition = ServicesDefinition.load_service(service_grade="+", service_type="change oil",
        #                                         service_category='AutoService', pay=1000)
        brand = Brand(brand_name='AtRoad', product_name='10w50', price=1000)
        data = {"brand_id": 3}
        print service_definition
        response = service_definition.append_brand(db, service_definition, brand)
        self.assertEqual(response[0], True)
        res = ServicesDefinitionBrands.load_brand(brand_id=3, service_definition_id=1)
        self.assertEqual(len(res[1]), 1)

    def test_update_sd_brande_id_remove_true(self):
        service_definition = ServicesDefinition(service_grade="+", service_type="change oil",
                                                service_category='AutoService', pay=1000)
        brand = Brand.load_brand(id=1)
        ServicesDefinitionBrands.add(brand, service_definition)
        data = {"brand_id": 1}
        service_definition.update(data)
        response = service_definition.update_brand_id_remove(data)
        self.assertEqual(response[0], True)
        res = ServicesDefinitionBrands.load_brand(brand_id=3, service_definition_id=1)
        self.assertEqual(len(res[1]), 0)

    # def test_update_sd_brande_id_append_false(self):
    #     service_definition = ServicesDefinition(service_grade="+", service_type="change oil",
    #                                             service_category='AutoService', pay=1000)
    #     data = {"brand_id": 4}
    #     service_definition.update(data)
    #     response = service_definition.update(data)
    #     self.assertEqual(response[0], True)
    #     dct = json.loads(response.data)
    #     self.assertEqual(dct[Keys.STATUS], 400)
    #     self.assertEqual(dct[Keys.MESSAGE], MessagesKeys.SUCCESS_UPDATE)

    # def test_update_sd_brande_id_remove_false(self):
    #     service_definition = ServicesDefinition(service_grade="+", service_type="change oil",
    #                                             service_category='AutoService', pay=1000)
    #     data = {"brand_id": "1"}
    #     service_definition.update(data)
    #     response = service_definition.update(data)
    #     self.assertEqual(response[0], True)
    #     dct = json.loads(response.data)
    #     self.assertEqual(dct[Keys.STATUS], 200)
    #     self.assertEqual(dct[Keys.MESSAGE], MessagesKeys.SUCCESS_UPDATE)

    def test_push_notification_poll(self):
        job = Job.query.filter(Job.id == 2).first()

        converter = JSONConverter()
        finish_job = FinishJobRequestController(job, converter)
        x = finish_job._push_notification_poll()

        self.assertEqual(x, 500)

    def test_give_payment_list(self):
        data = {
            "car_owner_id": 6,
            "car_id": 2
        }
        data1 = json.dumps(data)

        ccar = Car(vin_number="iRFC93R21SN497647", plate_number="77ط749-33", auto_type_id=1)
        User.query.filter(User.name == "MahD").first().cars.append(ccar)
        db.session.commit()

        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 6
            response = self.make_post_request(data1)
            dct = json.loads(response.data)
            self.assertEqual(dct[Keys.STATUS], 200)
            self.assertEqual(dct[Keys.MESSAGE], Result.language.SUCCESS_LIST)
            # self.assertEqual(dct[Keys.PARAMS], None)


if __name__ == '__main__':
    unittest.main()
