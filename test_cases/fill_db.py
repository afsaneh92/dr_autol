#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

from passlib.handlers.pbkdf2 import pbkdf2_sha256

from app import db, app
from config import DataBaseConfig
from core.messages.keys import Keys
from core.result import Result
from core.validation.helpers import expected_time_for_each_job
from persistence.database.entity.auto_model import AutoModel
from persistence.database.entity.auto_type import AutoType
from persistence.database.entity.brand import Brand
from persistence.database.entity.car_color import CarColor
from persistence.database.entity.company_to_brand import CompanyToBrand

from persistence.database.entity.consumable_item import ConsumableItem
# from persistence.database.entity.business_owner import BusinessOwners
# from persistence.database.entity.jobs import Jobs
from persistence.database.entity.user.auto_service import AutoServiceBusinessOwner
from persistence.database.entity.order import Order
from persistence.database.entity.order_items import OrderItem
from persistence.database.entity.payment_.full import FullPayment
from persistence.database.entity.product import Product
from persistence.database.entity.category import Category
from persistence.database.entity.services import ServiceGradeType
from persistence.database.entity.sub_category import SubCategory
from persistence.database.entity.supplier_product import SupplierToProduct
from persistence.database.entity.supplier_status import SupplierStatus
from persistence.database.entity.user.car_owner import CarOwner
from persistence.database.entity.user.supplier import Supplier
from persistence.database.entity.user.car_wash import CarWashBusinessOwner
from persistence.database.entity.user.user import User
from persistence.database.entity.business_owner_task import BusinessOwnerTask, BusinessOwnerTaskCarWash
from persistence.database.entity.car import Car
# from persistence.database.entity.car_owner import CarOwner
from persistence.database.entity.car_problem import CarProblem
from persistence.database.entity.question import Question
from persistence.database.entity.question_set import QuestionSet
from persistence.database.entity.question_to_question_set import QuestionToQuestionSet
from persistence.database.entity.comany.insurance_company import Company, InsuranceCompany
from persistence.database.entity.job_.job import Job
from persistence.database.entity.job_.autoservice_job import AutoServiceJob
from persistence.database.entity.job_.third_party import ThirdPart
from persistence.database.entity.payment_.installment import InstallPayment
from persistence.database.entity.payment_.installments import Installment
from persistence.database.entity.service_definition import ServicesDefinition, ServiceCategoryEnum, ServiceGradeEnum
from persistence.database.entity.service_grade import ServiceGrade
from persistence.database.entity.service_type import ServiceType
from persistence.database.entity.stauts import Status
from persistence.database.entity.payment_type import PaymentType
from persistence.database.entity.user.insurance import InsuranceBusinessOwner

app.config[
    'SQLALCHEMY_DATABASE_URI'] = DataBaseConfig.generate_database_uri()


##########
# new fill db
def init_auto_model():
    auto1 = AutoModel(name="bilibilak1.1", auto_types_id=1)
    auto2 = AutoModel(name='bilbilak1.2', auto_types_id=1)
    db.session.add(auto1)
    db.session.add(auto2)
    db.session.commit()


def init_color():
    auto1 = CarColor(name="red")
    auto2 = CarColor(name="green")
    auto3 = CarColor(name="blue")
    db.session.add(auto1)
    db.session.add(auto2)
    db.session.add(auto3)
    db.session.commit()


def init_auto_type_with_consumable_items():
    autos = [
        {
            "name": "FJ",
            "power": "1500"
        },
        {
            "name": "H2",
            "power": "1500"
        },
        {
            "name": "Volester",
            "power": "1500"
        },
        {
            "name": u"پراید",
            "power": "1500"
        },
        {
            "name": u"مزدا",
            "power": "1500"
        },
        {
            "name": u"مرسدس",
            "power": "1500"
        },
    ]
    auto1 = AutoType(name="FJ", engine_power="10000K")
    auto2 = AutoType(name='bilbilak', engine_power="20000K")
    item = ConsumableItem.query.filter(ConsumableItem.id == 1).first()
    item2 = ConsumableItem.query.filter(ConsumableItem.id == 2).first()
    item3 = ConsumableItem.query.filter(ConsumableItem.id == 3).first()
    auto1.consumable_items.extend([item])
    db.session.add(auto1)

    auto1.consumable_items.extend([item2])
    db.session.add(auto1)

    auto1.consumable_items.extend([item3])
    db.session.add(auto1)
    db.session.commit()
    auto2.consumable_items.extend([item2])
    db.session.add(auto1)

    auto2.consumable_items.extend([item3])
    db.session.add(auto1)
    db.session.commit()


def init_status():
    data = [
        Keys.STATUS_DONE,
        Keys.STATUS_PENDING,
        Keys.STATUS_CANCELLED_BY_CAR_OWNER,
        Keys.STATUS_CANCELLED_BY_BUSINESS_OWNER,
        Keys.STATUS_ACCEPTED_BY_BUSINESS_OWNER,
        Keys.STATUS_DENIED_BY_BUSINESS_OWNER,
        Keys.STATUS_TIMEOUT,
        Keys.STATUS_START
    ]

    for datum in data:
        status = Status(name=datum)
        db.session.add(status)
    db.session.commit()


def init_payment_types():
    type_ = PaymentType(name="PSP")
    db.session.add(type_)
    db.session.commit()

    type_ = PaymentType(name="POSE")
    db.session.add(type_)
    db.session.commit()

    type_ = PaymentType(name="CASH")
    db.session.add(type_)


def init_companies():
    pasargad = InsuranceCompany(name="Pasargad", branches_count=3)

    insurance_owner = InsuranceBusinessOwner(phone_number="09125200104",
                                             password=User.generate_hash_password("Amish1234"),
                                             code="7412",
                                             name="Arash Shokrzadeh",
                                             branch_code=1244, company=pasargad)
    # db.session.add(insurance_owner)
    # db.session.commit()


def init_question_set():
    question1 = Question(question=Keys.QUESTION_MANNER)
    question2 = Question(question=Keys.QUESTION_COST)
    question3 = Question(question=Keys.QUESTION_PLACE)
    question4 = Question(question=Keys.QUESTION_QUALITY)
    question5 = Question(question=Keys.QUESTION_EVERYTHING)

    db.session.add(question1)
    db.session.add(question2)
    db.session.add(question3)
    db.session.add(question4)
    db.session.add(question5)
    db.session.commit()

    ranking11 = QuestionSet(label="+++")
    ranking12 = QuestionSet(label="+")
    ranking13 = QuestionSet(label="Pre")
    db.session.add(ranking11)
    db.session.add(ranking12)
    db.session.add(ranking13)
    db.session.commit()

    a = QuestionToQuestionSet(question=question1, question_set=ranking11, is_key=True)
    b = QuestionToQuestionSet(question=question2, question_set=ranking11)
    d = QuestionToQuestionSet(question=question1, question_set=ranking12, is_key=True)
    e = QuestionToQuestionSet(question=question2, question_set=ranking12)
    f = QuestionToQuestionSet(question=question3, question_set=ranking12)
    g = QuestionToQuestionSet(question=question5, question_set=ranking13, is_key=True)

    db.session.add(a)
    db.session.add(b)
    db.session.add(d)
    db.session.add(e)
    db.session.add(f)
    db.session.add(g)
    db.session.commit()


def _init_auto_service_business_owner(name, phone, code, password, lat=-77.0364, lng=38.8951):
    hash = User.generate_hash_password(password=password)
    auto = AutoServiceBusinessOwner(phone_number=phone, password=hash, code=code, name=name, lat=lat, lng=lng,
                                    validate=True,
                                    geom='SRID=' + str(Keys.SRID_VALUE) + ';POINT(' + str(lng) + " " + str(lat) + ')')
    db.session.add(auto)
    db.session.commit()
    return auto


def _init_car_wash_business_owner(name, phone, code, password, lat=-77.0364, lng=38.8951):
    hash = User.generate_hash_password(password=password)
    auto = CarWashBusinessOwner(phone_number=phone, password=hash, code=code, name=name, lat=lat, lng=lng,
                                phone_number_workspace='33805486',
                                geom='SRID=' + str(Keys.SRID_VALUE) + ';POINT(' + str(lng) + " " + str(lat) + ')')
    db.session.add(auto)
    db.session.commit()
    return auto


def _init_car_owner(name, phone, code, password, validate=False):
    hash = User.generate_hash_password(password=password)
    car_owner = CarOwner(phone_number=phone, password=hash, code=code, name=name, validate=validate,
                         reg_id='ehbEUO0lt4Q:APA91bEgR2GHHbysOvq_oUgXj6jKxcllzOLO7ehvOGCNWB1nTIIRA559NVWEvN7LcJymImNsxiQoufix92DXLCEidytNgClXKE_CwWXXIpxyZncO1BMPNhINNvBh_EUQxYZkkp36L9Nr')
    db.session.add(car_owner)
    db.session.commit()
    return car_owner


def init_users():
    _init_auto_service_business_owner(name="Mostafa", phone="09125200100", password="Amish1234", code="1234")
    # _init_auto_service_business_owner(name="Changizi", phone="09125200101", password="Amish1234", code="1234")
    _init_auto_service_business_owner(name="Shirazi", phone="09125200102", password="Amish1234", code="1234")
    _init_auto_service_business_owner(name="Ahmadi", phone="09125200103", password="Amish1234", code="1234")
    _init_auto_service_business_owner(name="Asghari", phone="09125200104", password="Amish1234", code="1234")

    _init_car_wash_business_owner(name="Navid", phone="09125500101", password="Amish1234", code="1234")
    _init_car_wash_business_owner(name="Arash", phone="09125500102", password="Amish1234", code="1234")
    _init_car_wash_business_owner(name="Momo", phone="09125500103", password="Amish1234", code="1234")

    _init_car_owner(name="Amish", phone="09125200200", password="Amish1234", code="4321", validate=True)
    _init_car_owner(name="HaD", phone="09125200201", password="Amish1234", code="4321")
    _init_car_owner(name="MahD", phone="09125200202", password="Amish1234", code="4321")


def _init_service_definition(service_grade, service_type, service_category, pay, question_set_id):
    service_definition = ServicesDefinition(service_grade=service_grade, service_type=service_type, pay=pay,
                                            service_category=service_category, question_set_id=question_set_id)
    db.session.add(service_definition)
    db.session.commit()
    return service_definition


def _init_service_type(name, duration, consumable_items=None):
    service_type = ServiceType(name=name, duration=duration)
    if not consumable_items is None:
        service_type.consumable_items.extend(consumable_items)
    db.session.add(service_type)
    db.session.commit()
    return service_type


def _init_consumable_item(brand_name, product_name, price):
    consumable_item = ConsumableItem(brand_name=brand_name, product_name=product_name, price=price)
    db.session.add(consumable_item)
    db.session.commit()
    return consumable_item


def init_service_definitions():
    item_behran = _init_consumable_item(brand_name="Behran", product_name="10w40", price=30000)
    item_at_road = _init_consumable_item(brand_name="AtRoad", product_name="10w40", price=30000)
    item_shahab = _init_consumable_item(brand_name="Shahab", product_name="GTX", price=30000)
    item_tehran = _init_consumable_item(brand_name="Tehran", product_name="30 50", price=30000)

    change_oil_service_type = _init_service_type(name="Change Oil", duration=10,
                                                 consumable_items=[item_behran, item_at_road])

    change_air_filter_service_type = _init_service_type(name="change air filter", duration=10,
                                                        consumable_items=[item_shahab, item_tehran])

    _init_service_definition(service_grade=ServiceGradeEnum.Common, service_type=change_oil_service_type,
                             service_category=ServiceCategoryEnum.AutoService, pay=10000, question_set_id=2)
    _init_service_definition(service_grade=ServiceGradeEnum.Plus, service_type=change_oil_service_type,
                             service_category=ServiceCategoryEnum.AutoService, pay=15000, question_set_id=2)

    _init_service_definition(service_grade=ServiceGradeEnum.Plus, service_type=change_air_filter_service_type,
                             service_category=ServiceCategoryEnum.AutoService, pay=15000, question_set_id=2)

    diag_service_type = _init_service_type(name="Diag", duration=5)
    _init_service_definition(service_grade=ServiceGradeEnum.Common, service_type=diag_service_type,
                             service_category=ServiceCategoryEnum.AutoService, pay=5000, question_set_id=2)

    car_wash_inner = _init_service_type(name=u"داخل خودرو", duration=10)
    _init_service_definition(service_grade=ServiceGradeEnum.InCarWash, service_type=car_wash_inner,
                             service_category=ServiceCategoryEnum.CarWash, pay=8000, question_set_id=2)
    car_wash_motor = _init_service_type(name=u"موتور خودرو", duration=10)
    _init_service_definition(service_grade=ServiceGradeEnum.InCarWash, service_type=car_wash_motor,
                             service_category=ServiceCategoryEnum.CarWash, pay=6000, question_set_id=2)
    car_wash_outer = _init_service_type(name=u"خارج خودور", duration=10)
    _init_service_definition(service_grade=ServiceGradeEnum.InCarWash, service_type=car_wash_outer,
                             service_category=ServiceCategoryEnum.CarWash, pay=12000, question_set_id=2)

    _init_service_definition(service_grade=ServiceGradeEnum.InPlaceWash, service_type=car_wash_inner,
                             service_category=ServiceCategoryEnum.CarWash, pay=8000, question_set_id=2)
    _init_service_definition(service_grade=ServiceGradeEnum.InPlaceWash, service_type=car_wash_motor,
                             service_category=ServiceCategoryEnum.CarWash, pay=6000, question_set_id=2)
    _init_service_definition(service_grade=ServiceGradeEnum.InPlaceWash, service_type=car_wash_outer,
                             service_category=ServiceCategoryEnum.CarWash, pay=12000, question_set_id=2)

    db.session.commit()

    # service_grade1 = ServiceGrade(name=ServiceGradeEnum.Plus)
    # service_grade2 = ServiceGrade(name=ServiceGradeEnum.Common)
    # db.session.add(service_grade1)
    # db.session.add(service_grade2)
    # db.session.commit()
    #
    # service_grade_type1 = ServiceGradeType(service_grade=2, service_type=1, question_set_id=1)
    # service_grade_type2 = ServiceGradeType(service_grade=1, service_type=2, question_set_id=2)
    # service_grade_type3 = ServiceGradeType(service_grade=1, service_type=1, question_set_id=1)
    # db.session.add(service_grade_type1)
    # db.session.add(service_grade_type2)
    # db.session.add(service_grade_type3)
    # db.session.commit()


def init_accepted_jobs():
    car_problems = {
        'has_product': {1: 1},
        'not_product': [3]
    }
    finish_status = Status.query.filter(Status.name == Keys.STATUS_DONE).first()

    status = Status.query.filter(Status.name == Keys.STATUS_ACCEPTED_BY_BUSINESS_OWNER).first()
    start_status = Status.query.filter(Status.name == Keys.STATUS_START).first()

    _init_auto_service_jobs(business_owner=1, car_owner=6, car_problems=car_problems, car=5, status_id=finish_status.id,
                            start="2018-5-3 08:40:00",
                            finish="2018-5-3 08:41:00", rate=[], price=10000,
                            question_set_id=2, start_time=None, finish_time=None)

    _init_auto_service_jobs(business_owner=1, car_owner=6, car_problems=car_problems, car=5, status_id=status.id,
                            start="2018-4-3 09:40:00",
                            finish="2018-4-3 08:41:00", rate=[], price=10000,
                            question_set_id=2, start_time=None, finish_time=None)
    _init_auto_service_jobs(business_owner=1, car_owner=6, car_problems=car_problems, car=5, status_id=start_status.id,
                            start="2018-10-3 09:40:00",
                            finish="2018-11-3 08:41:00", rate=[], price=10000,
                            question_set_id=2, start_time=None, finish_time=None)
    _init_auto_service_jobs(business_owner=1, car_owner=6, car_problems=car_problems, car=5, status_id=start_status.id,
                            start="2018-10-3 09:40:00",
                            finish="2018-11-3 08:41:00", rate=[], price=10000,
                            question_set_id=2, start_time=None, finish_time=None)


def init_jobs():
    init_accepted_jobs()
    car_problems = {
        'has_product': {1: 1, 3: 3},
        # 'not_product': [2]
    }
    pending_status = Status.query.filter(Status.name == Keys.STATUS_PENDING).first()
    accepted_status = Status.query.filter(Status.name == Keys.STATUS_ACCEPTED_BY_BUSINESS_OWNER).first()
    start_status = Status.query.filter(Status.name == Keys.STATUS_START).first()
    # _init_auto_service_jobs(car_owner=4, car=1, business_owner=1, status_id=1, car_problems=car_problems, rate=[],
    #                         question_set_id=2, price=1000,
    #                         start="2018-7-05 10:30", finish="2018-07-05 11:00", start_time="2018-7-05 10:30",
    #                         finish_time="2018-07-05 11:00")
    #
    # _init_auto_service_jobs(car_owner=4, car=1, business_owner=1, status_id=1, car_problems=car_problems, price=1000,
    #                         start="2018-7-05 10:30", finish="2018-07-05 11:00", rate=[], question_set_id=2,
    #                         start_time="2018-7-05 10:30",
    #                         finish_time="2018-07-05 11:00")
    #
    # _init_auto_service_jobs(car_owner=5, car=5, business_owner=6, car_problems=car_problems, status_id=status1.id,
    #                         start="2018-04-3 08:40:00",
    #                         finish="2018-04-3 08:41:00", rate=[1, 2, 0], price=1000,
    #                         question_set_id=2, start_time="2018-04-3 08:40:00",
    #                         finish_time="2018-04-3 08:41:00")

    _init_auto_service_jobs(business_owner=1, car_owner=7, car_problems=car_problems, car=5,
                            status_id=pending_status.id,
                            start="2018-04-3 08:40:00",
                            finish="2018-04-3 08:41:00", rate=[], price=10000,
                            question_set_id=2, start_time="2018-04-3 08:40:00", finish_time=None)

    _init_auto_service_jobs(business_owner=3, car_owner=6, car_problems=car_problems, car=2,
                            status_id=pending_status.id,
                            start="2018-05-12 08:40:00",
                            finish="2018-05-12 08:50:00", rate=[], question_set_id=2, price=1000,
                            start_time="2018-04-3 10:40:00", finish_time=None
                            )
    _init_auto_service_jobs(car_owner=5, car=1, business_owner=2, status_id=pending_status.id,
                            car_problems=car_problems,
                            price=1000,
                            start="2018-04-05 10:30", finish="2018-04-05 11:00", rate=[1, 0, 2],
                            question_set_id=2,
                            start_time=None, finish_time=None)


def _init_auto_service_jobs(car_owner, car, business_owner, status_id, car_problems, price, start, finish, rate=[],
                            question_set_id=None, start_time=None, finish_time=None):
    problems = []
    for key, values in car_problems.iteritems():
        if key == 'not_product':
            for value in values:
                problem = CarProblem(services_definition_id=value)
                problems.append(problem)
        else:
            for service, item in values.iteritems():
                problem = CarProblem(services_definition_id=service, consumable_item_id=item)
                problems.append(problem)

    job = AutoServiceJob(car_owner_id=car_owner, car_id=car,
                         business_owner_id=business_owner, status_id=status_id,
                         start_schedule=start, finish_schedule=finish, price=price, rate=rate,
                         question_set_id=question_set_id, start_time=start_time, finish_time=finish_time)
    job.car_problems.extend(problems)
    db.session.add(job)
    db.session.commit()
    return job


def init_business_owner_task():
    b_o = AutoServiceBusinessOwner.query.filter(AutoServiceBusinessOwner.id == 1).first()

    task1 = BusinessOwnerTask(service_definition_id=1)
    task2 = BusinessOwnerTask(service_definition_id=2)
    b_o.task.append(task1)
    b_o.task.append(task2)

    task1 = BusinessOwnerTaskCarWash(service_definition_id=5)
    # task2 = BusinessOwnerTaskCarWash(service_definition_id=11)
    b_o = CarWashBusinessOwner.query.filter().first()
    b_o.task.append(task1)
    # b_o.task.append(task2)

    task1 = BusinessOwnerTaskCarWash(service_definition_id=5)
    # task1 = BusinessOwnerTaskCarWash(service_definition_id=5)
    # task2 = BusinessOwnerTaskCarWash(service_definition_id=11)
    b_o = CarWashBusinessOwner.query.filter(CarWashBusinessOwner.name == "Momo").first()
    b_o.task.append(task1)

    db.session.commit()


def init_cars():
    cars = [
        {
            "vin_number": "iRFC93R21SN497640",
            "plate_number": "70ط749-33"
        },
        {
            "vin_number": "iRFC93R21SN497641",
            "plate_number": "71ط749-33"
        },
        {
            "vin_number": "iRFC93R21SN497643",
            "plate_number": "72ط749-33"
        },
        {
            "vin_number": "iRFC93R21SN497644",
            "plate_number": "73ط749-33"
        },
        {
            "vin_number": "iRFC93R21SN497645",
            "plate_number": "74ط749-33"
        }
    ]

    car_for_car_owner = []
    for car in cars:
        ccar = Car(vin_number=car['vin_number'], plate_number=car['plate_number'], color_id=1, current_kilometer=10000,
                   auto_type_id=1, auto_model_id=1)
        car_for_car_owner.append(ccar)

    CarOwner.query.filter(CarOwner.name == "Amish").first().cars.extend(car_for_car_owner)

    db.session.commit()


def _init_full_payment_job(job, payment_name):
    payment_type = PaymentType.query.filter(PaymentType.name == payment_name).first()
    payment = FullPayment(amount=1000, currency='IRR', payment_type_id=payment_type.id)
    job.payment = payment
    db.session.merge(job)
    db.session.commit()


def init_jobs_with_payment():
    car_problems = {
        'has_product': {1: 1},
        'not_product': [2]
    }
    status1 = Status.query.filter(Status.name == Keys.STATUS_DONE).first()

    job = _init_auto_service_jobs(car_owner=5, car=1, business_owner=1, status_id=status1.id, car_problems=car_problems,
                                  price=1000,
                                  start="2018-04-05 10:30", finish="2018-04-05 11:00", rate=[1, 1, 1],
                                  question_set_id=2,
                                  start_time=None, finish_time=None)
    _init_full_payment_job(job, "PSP")


def _init_supplier(name, phone, code, password, business_license, address, validate=False):
    hash = User.generate_hash_password(password=password)
    supplier = Supplier(phone_number=phone, password=hash, business_license=business_license, address=address,
                        code=code, name=name,
                        validate=validate,
                        reg_id='ehbEUO0lt4Q:APA91bEgR2GHHbysOvq_oUgXj6jKxcllzOLO7ehvOGCNWB1nTIIRA559NVWEvN7LcJymImNsxiQoufix92DXLCEidytNgClXKE_CwWXXIpxyZncO1BMPNhINNvBh_EUQxYZkkp36L9Nr')
    db.session.add(supplier)
    db.session.commit()
    return supplier


def init_product():
    sup1 = _init_supplier(name="alavi", phone="09125200101", password="Amish1234", code="7890",
                          business_license="11111", address="tehran- beheshti"
                          )
    sup2 = _init_supplier(name="naghavi", phone="09125200111", password="Amish1234", code="7890",
                          business_license="22222", address="tehran- beheshti"
                          )
    sup3 = _init_supplier(name="taghavi", phone="09125200112", password="Amish1234", code="7890",
                          business_license="33333", address="tehran- beheshti"
                          , validate=True)
    db.session.add(sup1)
    db.session.add(sup2)
    db.session.add(sup3)
    db.session.commit()

    category1 = Category(name="badane")
    category2 = Category(name="motori")
    category3 = Category(name=u"دوره ای")
    db.session.add(category1)
    db.session.add(category2)
    db.session.add(category3)
    db.session.commit()

    sub_category1 = SubCategory(name=u"آینه", category_id=1)
    sub_category2 = SubCategory(name=u"شمع", category_id=2)
    sub_category3 = SubCategory(name=u"روغن ترمز", category_id=3)
    db.session.add(sub_category1)
    db.session.add(sub_category2)
    db.session.add(sub_category3)
    db.session.commit()

    brand1 = Brand(name='10w40')
    brand2 = Brand(name='GTX')
    brand3 = Brand(name='30 50')
    db.session.add(brand1)
    db.session.add(brand2)
    db.session.add(brand3)
    db.session.commit()

    company1 = Company(id=1, name='BEHRAN')
    company2 = Company(id=2, name='AtRoad')
    company3 = Company(id=3, name='Shahab')
    db.session.add(company1)
    db.session.add(company2)
    db.session.add(company3)
    db.session.commit()

    q = CompanyToBrand(company=company1, brand=brand1)
    e = CompanyToBrand(company=company2, brand=brand1)
    p = CompanyToBrand(company=company2, brand=brand2)
    db.session.add(q)
    db.session.add(e)
    db.session.add(p)
    db.session.commit()

    product1 = Product(minimum_order=100, code="45555", price="10000", sub_category_id=1, brand_id=1,
                       company_id=1, supplier_id=11)
    product2 = Product(minimum_order=100, code="45556", price="20000", sub_category_id=2, brand_id=1,
                       company_id=2, supplier_id=12)
    product3 = Product(minimum_order=100, code="45557", price="30000", sub_category_id=3, brand_id=2,
                       company_id=2, supplier_id=13)
    db.session.add(product1)
    db.session.add(product2)
    db.session.add(product3)
    db.session.commit()

    # a = SupplierToProduct(supplier=sup1, product=product1)
    # b = SupplierToProduct(supplier=sup2, product=product1)
    # c = SupplierToProduct(supplier=sup1, product=product3)
    # db.session.add(a)
    # db.session.add(b)
    # db.session.add(c)
    # db.session.commit()

    order1 = Order(id=1, pre_invoice_id=1, invoice_id=2)
    order2 = Order(id=2, pre_invoice_id=2)
    order3 = Order(id=3, pre_invoice_id=3, invoice_id=3)
    db.session.add(order1)
    db.session.add(order2)
    db.session.add(order3)
    db.session.commit()

    supplier_status1 = SupplierStatus(name='accept')
    supplier_status2 = SupplierStatus(name='deny')
    supplier_status3 = SupplierStatus(name='partial')
    supplier_status4 = SupplierStatus(name='pending')
    supplier_status5 = SupplierStatus(name='done')
    db.session.add(supplier_status1)
    db.session.add(supplier_status2)
    db.session.add(supplier_status3)
    db.session.add(supplier_status4)
    db.session.add(supplier_status5)
    db.session.commit()

    order_items1 = OrderItem(product_id=1, order_id=1, requested_number=1000, supplier_status_id=5,
                             accepted_number=12, business_owner_id=1)
    order_items5 = OrderItem(product_id=1, order_id=1, requested_number=1000, supplier_status_id=5,
                             accepted_number=1, business_owner_id=1)
    order_items6 = OrderItem(product_id=1, order_id=1, requested_number=1000, supplier_status_id=5,
                             accepted_number=1000, business_owner_id=1)
    order_items7 = OrderItem(product_id=1, order_id=1, requested_number=1000, supplier_status_id=5,
                             accepted_number=14, business_owner_id=1)

    order_items2 = OrderItem(product_id=2, order_id=1, requested_number=2000, supplier_status_id=5,
                             accepted_number=5, business_owner_id=2)
    order_items3 = OrderItem(product_id=3, order_id=2, requested_number=100, supplier_status_id=3,
                             accepted_number=7, business_owner_id=1)
    order_items4 = OrderItem(product_id=1, order_id=2, supplier_status_id=4, business_owner_id=3)
    db.session.add(order_items1)
    db.session.add(order_items2)
    db.session.add(order_items3)
    db.session.add(order_items4)
    db.session.add(order_items5)
    db.session.add(order_items6)
    db.session.add(order_items7)
    db.session.commit()


def init_db():
    # pass
    db.drop_all()
    db.create_all()
    init_question_set()
    init_service_definitions()
    init_users()
    init_status()
    init_auto_type_with_consumable_items()
    init_auto_model()
    init_jobs()
    init_payment_types()
    init_jobs_with_payment()
    init_companies()
    init_business_owner_task()
    init_color()
    init_cars()
    init_product()
    # init_product initialize : order, order_items, product, supplier, category, sub_category tables
    # init_product()


if __name__ == "__main__":
    init_db()
