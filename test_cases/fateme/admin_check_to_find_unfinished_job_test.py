import json
from app import db, app
from config import DataBaseConfig
from core.messages.keys import Keys
from persistence.database.entity.car_problem import CarProblem
from persistence.database.entity.job_.job import Job
from persistence.database.entity.stauts import Status
from routers.admin import admin
from routers.authintication import authentication
from routers.business_owner import business_owner
from routers.car_owner import car_owner
from routers.choose_services import choose_service_grade
from routers.index import index_route
from test_cases.fill_db import init_db
import unittest
from routers.endpoints import Endpoints
from test_cases.test_keys import TestKeys


class TestCheckUnfinishedJobs(unittest.TestCase):
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
        app.register_blueprint(car_owner)
        app.register_blueprint(business_owner)
        app.register_blueprint(authentication)
        app.register_blueprint(admin)
        app.register_blueprint(choose_service_grade)

        self.app = app.test_client()

        if self._testMethodName == "test_no_db":
            db.drop_all()
        else:
            db.drop_all()
            init_db()
            # TestCheckUnfinishedJobs.insert_some_data()

    # executed after each test
    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    @classmethod
    def insert_some_data(cls):
        data = [
            {"service_type": 1, "service_grade": 1},
            {"service_type": 2, "service_grade": 1},
            {"service_type": 4, "service_grade": 1},
        ]
        car_problems = []
        for car_problem in data:
            c_p = CarProblem(consumable_item_id=1, services_definition_id=1)
            car_problems.append(c_p)
        status = Status.query.filter(Status.name == Keys.STATUS_START).first()
        status1 = Status.query.filter(Status.name == Keys.STATUS_DONE).first()
        status2 = Status.query.filter(Status.name == Keys.STATUS_ACCEPTED_BY_BUSINESS_OWNER).first()

        job1 = Job(business_owner_id=1, car_owner_id=2, car_id=1, status_=status1,
                    start_schedule="2018-04-3 07:30:00",
                    finish_schedule="2018-04-3 11:40:00", start_time="2018-04-3 07:33:00")
        job2 = Job(business_owner_id=2, car_owner_id=3, car_id=2, status_=status, start_schedule="2018-04-3 08:00:00",
                    finish_schedule="2018-04-3 08:13:00", start_time="2018-04-3 08:02:00")

        job3 = Job(business_owner_id=6, car_owner_id=5, car_id=5, status_=status1, start_schedule="2018-04-3 08:40:00",
                    finish_schedule="2018-04-3 08:41:00", start_time="2018-04-3 09:02:00")
        job4 = Job(business_owner_id=7, car_owner_id=4, car_id=4, status_=status1, start_schedule="2018-04-3 07:13:00",
                    finish_schedule="2018-04-3 07:15:00", start_time="2018-04-3 07:20:00",
                    finish_time="2018-04-3 08:15:00")
        job5 = Job(business_owner_id=5, car_owner_id=3, car_id=3, status_=status2,
                    start_schedule="2018-04-2 06:00:00",
                    finish_schedule="2018-04-2 11:11:00")

        job1.car_problems.extend(car_problems)
        db.session.add(job1)
        db.session.commit()

        job2.car_problems.extend(car_problems)
        db.session.add(job2)
        db.session.commit()

        job3.car_problems.extend(car_problems)
        db.session.add(job3)
        db.session.commit()

        job4.car_problems.extend(car_problems)
        db.session.add(job4)
        db.session.commit()

        job5.car_problems.extend(car_problems)
        db.session.add(job5)
        db.session.commit()

    def test_no_db(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self.app.get(Endpoints.LIST_UNFINISHED_JOB, content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)

            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 500)

    def test_find_all_not_finished_job(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = self.app.get(Endpoints.LIST_UNFINISHED_JOB, content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)
            data_store = json.loads(response.data)
            self.assertEqual(data_store[Keys.STATUS], 200)




if __name__ == '__main__':
    unittest.main()
