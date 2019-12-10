#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import db, app
from config import DataBaseConfig
from core.messages.keys import Keys
from core.result import Result
from core.validation.helpers import expected_time_for_each_job
from persistence.database.entity.auto_model import AutoModel
from persistence.database.entity.auto_type import AutoType
from persistence.database.entity.car_color import CarColor

from persistence.database.entity.consumable_item import ConsumableItem
from persistence.database.entity.order import Order
from persistence.database.entity.order_items import OrderItem
from persistence.database.entity.payment_.full import FullPayment
from persistence.database.entity.product import Product
from persistence.database.entity.category import Category
from persistence.database.entity.sub_category import SubCategory
from persistence.database.entity.supplier_product import SupplierToProduct
from persistence.database.entity.user.car_owner import CarOwner
from persistence.database.entity.user.supplier import Supplier
from persistence.database.entity.user.user import User
from persistence.database.entity.business_owner_task import BusinessOwnerTask
from persistence.database.entity.car import Car
# from persistence.database.entity.car_owner import CarOwner
from persistence.database.entity.car_problem import CarProblem
from persistence.database.entity.question import Question
from persistence.database.entity.question_set import QuestionSet
from persistence.database.entity.question_to_question_set import QuestionToQuestionSet
from persistence.database.entity.service_definition import ServicesDefinition
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
from persistence.database.entity.user.auto_service import AutoServiceBusinessOwner
from persistence.database.entity.user.insurance import InsuranceBusinessOwner
from persistence.database.entity.user.car_wash import CarWashBusinessOwner

app.config[
    'SQLALCHEMY_DATABASE_URI'] = DataBaseConfig.generate_database_uri()


def _init_consumable_item(brand_name, product_name, price):
    consumable_item = ConsumableItem(brand_name=brand_name, product_name=product_name, price=price)
    db.session.add(consumable_item)
    db.session.commit()
    return consumable_item


def init_service_definitions():
    change_motor_oil = _init_service_type(name="روغن موتور", duration=10,
                                          consumable_items=None)
    _init_service_definition(service_grade=ServiceGradeEnum.Common, service_type=change_motor_oil,
                             service_category=ServiceCategoryEnum.AutoService, pay=10000, question_set_id=1)

    change_brake_oil = _init_service_type(name="روغن ترمز", duration=10,
                                          consumable_items=None)
    _init_service_definition(service_grade=ServiceGradeEnum.Common, service_type=change_brake_oil,
                             service_category=ServiceCategoryEnum.AutoService, pay=10000, question_set_id=1)

    change_motor_oil = _init_service_type(name="فیلتر هوا", duration=10,
                                          consumable_items=None)
    _init_service_definition(service_grade=ServiceGradeEnum.Common, service_type=change_motor_oil,
                             service_category=ServiceCategoryEnum.AutoService, pay=10000, question_set_id=1)

    change_bin_filter = _init_service_type(name="فیلتر بنزین", duration=10,
                                           consumable_items=None)
    _init_service_definition(service_grade=ServiceGradeEnum.Common, service_type=change_bin_filter,
                             service_category=ServiceCategoryEnum.AutoService, pay=10000, question_set_id=1)

    change_oil_filter = _init_service_type(name="فیلتر روغن", duration=10,
                                           consumable_items=None)
    _init_service_definition(service_grade=ServiceGradeEnum.Common, service_type=change_oil_filter,
                             service_category=ServiceCategoryEnum.AutoService, pay=10000, question_set_id=1)

    change_brake_pad = _init_service_type(name="لنت ترمز", duration=10,
                                          consumable_items=None)
    _init_service_definition(service_grade=ServiceGradeEnum.Common, service_type=change_brake_pad,
                             service_category=ServiceCategoryEnum.AutoService, pay=10000, question_set_id=1)

    change_candle = _init_service_type(name="شمع", duration=10,
                                       consumable_items=None)
    _init_service_definition(service_grade=ServiceGradeEnum.Common, service_type=change_candle,
                             service_category=ServiceCategoryEnum.AutoService, pay=10000, question_set_id=1)

    change_wire = _init_service_type(name="وایر", duration=10,
                                     consumable_items=None)
    _init_service_definition(service_grade=ServiceGradeEnum.Common, service_type=change_wire,
                             service_category=ServiceCategoryEnum.AutoService, pay=10000, question_set_id=1)

    change_battery = _init_service_type(name="باتری", duration=10,
                                        consumable_items=None)
    _init_service_definition(service_grade=ServiceGradeEnum.Common, service_type=change_battery,
                             service_category=ServiceCategoryEnum.AutoService, pay=10000, question_set_id=1)

    change_tire = _init_service_type(name="تایر", duration=10,
                                     consumable_items=None)
    _init_service_definition(service_grade=ServiceGradeEnum.Common, service_type=change_tire,
                             service_category=ServiceCategoryEnum.AutoService, pay=10000, question_set_id=1)

    balance_the_wheel = _init_service_type(name="بالانس کردن چرخ", duration=10,
                                           consumable_items=None)
    _init_service_definition(service_grade=ServiceGradeEnum.Common, service_type=balance_the_wheel,
                             service_category=ServiceCategoryEnum.AutoService, pay=10000, question_set_id=1)

    set_the_lights = _init_service_type(name="تنظیم چراغ", duration=10,
                                        consumable_items=None)
    _init_service_definition(service_grade=ServiceGradeEnum.Common, service_type=set_the_lights,
                             service_category=ServiceCategoryEnum.AutoService, pay=10000, question_set_id=1)

    set_the_command = _init_service_type(name="تنظیم فرمان", duration=10,
                                         consumable_items=None)
    _init_service_definition(service_grade=ServiceGradeEnum.Common, service_type=set_the_command,
                             service_category=ServiceCategoryEnum.AutoService, pay=10000, question_set_id=1)

    in_car_wash = _init_service_type(name="شست و شوی داخل خودرو", duration=10,
                                     consumable_items=None)
    _init_service_definition(service_grade=ServiceGradeEnum.InCarWash, service_type=in_car_wash,
                             service_category=ServiceCategoryEnum.CarWash, pay=10000, question_set_id=1)

    in_place_wash = _init_service_type(name="شست و شوی خارج خودرو", duration=10,
                                       consumable_items=None)
    _init_service_definition(service_grade=ServiceGradeEnum.InPlaceWash, service_type=in_place_wash,
                             service_category=ServiceCategoryEnum.CarWash, pay=10000, question_set_id=1)

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


def init_color():
    color1 = CarColor(name="سفید")
    color2 = CarColor(name="مشکی")
    color3 = CarColor(name="نوک مدادی")
    color4 = CarColor(name="نقره ای")
    color5 = CarColor(name="بژ")
    color6 = CarColor(name="آبی")
    color7 = CarColor(name="سبز")
    color8 = CarColor(name="قرمز")
    color9 = CarColor(name="زرد")
    db.session.add(color1)
    db.session.add(color2)
    db.session.add(color3)
    db.session.add(color4)
    db.session.add(color5)
    db.session.add(color6)
    db.session.add(color7)
    db.session.add(color8)
    db.session.add(color9)
    db.session.commit()


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

    ranking11 = QuestionSet(label="AutoServiceCommon")
    # ranking12 = QuestionSet(label="+")
    # ranking13 = QuestionSet(label="Pre")
    db.session.add(ranking11)
    db.session.commit()

    a = QuestionToQuestionSet(question=question1, question_set=ranking11)
    b = QuestionToQuestionSet(question=question2, question_set=ranking11)
    c = QuestionToQuestionSet(question=question3, question_set=ranking11)
    d = QuestionToQuestionSet(question=question4, question_set=ranking11)
    e = QuestionToQuestionSet(question=question5, question_set=ranking11, is_key=True)

    db.session.add(a)
    db.session.add(b)
    db.session.add(d)
    db.session.add(e)
    db.session.commit()


def init_auto_model():
    # pride
    pride = AutoType(name="پراید", engine_power="10000K")
    se111 = AutoModel(name="SE 111")
    se131 = AutoModel(name="SE 131")
    se132 = AutoModel(name="SE 132")
    sx = AutoModel(name="SX")
    pride.auto_models.extend([se111, se131, se132, sx])
    db.session.add(pride)

    # sayna
    sayna = AutoType(name="ساینا", engine_power="10000K")
    ex = AutoModel(name="EX")
    sayna_automatic = AutoModel(name="اتوماتیک")
    sayna.auto_models.extend([ex, sayna_automatic])
    db.session.add(sayna)

    # ariyo
    ariyo = AutoType(name="آریو", engine_power="10000K")
    gear1600 = AutoModel(name="1600 دنده ای")
    automatic1600 = AutoModel(name="1600 اتوماتیک")
    ariyo.auto_models.extend([gear1600, automatic1600])
    db.session.add(ariyo)

    # changan
    changan = AutoType(name="چانگان", engine_power="10000K")
    CS35 = AutoModel(name="CS35")
    changan.auto_models.extend([CS35])
    db.session.add(changan)

    # kia
    kia = AutoType(name="کیا", engine_power="10000K")
    serato_automatic = AutoModel(name="سراتو اتوماتیک")
    gear1600serato = AutoModel(name="1600 دنده ای")
    optional1600 = AutoModel(name="سراتو 1600 آپشنال دنده ای")
    serato2000 = AutoModel(name="سراتو 2000 اتوماتیک")
    serato2000automatic = AutoModel(name="سراتو 2000 آپشنال اتوماتیک")
    kia.auto_models.extend([serato_automatic, gear1600serato, optional1600, serato2000, serato2000automatic])
    db.session.add(kia)

    # samand
    samand = AutoType(name="سمند", engine_power="10000K")
    lx = AutoModel(name="LX")
    lx_ef7 = AutoModel(name="LX EF7")
    samand.auto_models.extend([lx, lx_ef7])
    db.session.add(samand)

    # soren
    soren = AutoType(name="سورن", engine_power="10000K")
    elx = AutoModel(name="ELX ")
    elx_turbo = AutoModel(name="ELX توربو")
    soren.auto_models.extend([elx, elx_turbo])
    db.session.add(soren)

    # dena
    dena = AutoType(name="دنا", engine_power="10000K")
    common = AutoModel(name="معمولی")
    plus = AutoModel(name="پلاس")
    plus_turbo = AutoModel(name="پلاس توربو")
    dena.auto_models.extend([common, plus, plus_turbo])
    db.session.add(dena)

    # dena
    # dena = AutoType(name="دنا", engine_power="10000K")
    # common = AutoModel(name="معمولی")
    # plus = AutoModel(name="پلاس")
    # plus_turbo = AutoModel(name="پلاس توربو")
    # dena.auto_models.extend([common, plus, plus_turbo])
    # db.session.add(dena)

    bmw_korok = AutoType(name="BMW سری 6 کروک", engine_power="10000K")
    bmw_korok_630i = AutoModel(name="630i")
    bmw_korok_1600650i = AutoModel(name="1600650i")
    bmw_korok_M6 = AutoModel(name="M6")
    bmw_korok.auto_models.extend([bmw_korok_630i, bmw_korok_1600650i, bmw_korok_M6])
    db.session.add(bmw_korok)

    bmw_kope = AutoType(name="BMW سری 6 کوپه", engine_power="10000K")
    bmw_kope_630i = AutoModel(name="630i")
    bmw_kope_640i = AutoModel(name="640i")
    bmw_kope.auto_models.extend([bmw_kope_630i, bmw_kope_640i])
    db.session.add(bmw_kope)

    bmw_7 = AutoType(name="BMW سری 7", engine_power="10000K")
    bmw_7_730i = AutoModel(name="730i")
    bmw_7_730li = AutoModel(name="730li")
    bmw_7_735li = AutoModel(name="735li")
    bmw_7_740i = AutoModel(name="740i")
    bmw_7_740li = AutoModel(name="740li")
    bmw_7_750li = AutoModel(name="750li")
    bmw_7.auto_models.extend([bmw_7_730i, bmw_7_730li, bmw_7_735li, bmw_7_740i, bmw_7_740li, bmw_7_750li])
    db.session.add(bmw_7)

    bmw_i = AutoType(name="BMW سری i", engine_power="10000K")
    bmw_i_i8 = AutoModel(name="i8")
    bmw_i.auto_models.extend([bmw_i_i8])
    db.session.add(bmw_i)

    bmw_cassic = AutoType(name="BMW کلاسیک", engine_power="10000K")
    bmw_i_i8 = AutoModel(name="i8")
    bmw_cassic.auto_models.extend([bmw_i_i8])
    db.session.add(bmw_cassic)

    bike = AutoType(name="بایک", engine_power="10000K")
    bmw_hachback = AutoModel(name="سابرینا هاچبک")
    bmw_sabrina_hachback = AutoModel(name="سابرینا هاچبک (مونتاژ)")
    bmw_senova = AutoModel(name="سنوا")
    bike.auto_models.extend([bmw_hachback, bmw_sabrina_hachback, bmw_senova])
    db.session.add(bike)


def _init_auto_service_business_owner(name, phone, address, phone_number_workspace, workspace_name, code, password,
                                      lat=-77.0364, lng=38.8951,
                                      uuid='75106e9e-a9eb-11e8-a66e-34f39aa7f24b'):
    hash = User.generate_hash_password(password=password)
    auto = AutoServiceBusinessOwner(phone_number=phone, password=hash, code=code, name=name, lat=lat, lng=lng,
                                    validate=True, address=address, workspace_name=workspace_name, uuid=uuid,
                                    phone_number_workspace=phone_number_workspace,
                                    geom='SRID=' + str(Keys.SRID_VALUE) + ';POINT(' + str(lng) + " " + str(lat) + ')',
                                    reg_id="ehbEUO0lt4Q:APA91bEgR2GHHbysOvq_oUgXj6jKxcllzOLO7ehvOGCNWB1nTIIRA559NVWEvN7LcJymImNsxiQoufix92DXLCEidytNgClXKE_CwWXXIpxyZncO1BMPNhINNvBh_EUQxYZkkp36L9Nr")
    db.session.add(auto)
    db.session.commit()
    return auto


def init_business_owner_task():
    phones = ['09121771676', '09122219547', '09125200100']

    for phone in range(len(phones)):
        b_o = User.query.filter(User.phone_number == phones[phone]).first()

        tasks = []
        for i in range(1, 13):
            tasks.append(BusinessOwnerTask(service_definition_id=i))
        b_o.task.extend(tasks)

    db.session.commit()


def init_users():
    _init_auto_service_business_owner(name="سعید کیانیان", workspace_name='اسپرت تایر تهرانپارس',
                                      address='فلکه دوم تهرانپارس، خیابان جشنواره، چهارراه سجده ای، پلاک 149',
                                      phone_number_workspace='77889055',
                                      phone="09121771676", password="Amish1234", code="1234")
    _init_auto_service_business_owner(name="حسین محمدی", uuid='7753e0e1-a9e9-11e8-8add-34f39aa7f24b',
                                      address='پیروزی، خیابان افراسیابی شمالی، نرسیده به میدان سیزده آبان، پلاک 225',
                                      workspace_name='اتو سرویس تک شعبه 1', phone_number_workspace='33178678',
                                      phone="09122219547", password="Amish1234",
                                      code="1234")
    _init_auto_service_business_owner(name="حمید حسینی", uuid='4a58fc5e-a9e9-11e8-9eb4-34f39aa7f24b',
                                      phone_number_workspace='33023569',
                                      address='17 شهریور جنوبی، ابتدای خیابان رضایی (منصور) شرقی، رو به روی مدرسه مختار، پلاک 690',
                                      workspace_name='اتو سرویس تک شعبه 2',
                                      phone="09125200100", password="Amish1234", code="1234")  # TODO give Hamid number

    _init_auto_service_business_owner(name="علیرضا ملک جانی",
                                      phone_number_workspace='',
                                      address='تهرانپارس، سه راه آزمایش، پلاک 4/1',
                                      workspace_name='تعمیرگاه شرق',
                                      phone="0935327387", password="Amish1234", code="1234")  # TODO safkari

    _init_car_owner(name="امیش", phone="09125200200", password="Amish1234", code="4321")


def _init_car_owner(name, phone, code, password, validate=True):
    hash = User.generate_hash_password(password=password)
    car_owner = CarOwner(phone_number=phone, password=hash, code=code, name=name, validate=validate,
                         reg_id='ehbEUO0lt4Q:APA91bEgR2GHHbysOvq_oUgXj6jKxcllzOLO7ehvOGCNWB1nTIIRA559NVWEvN7LcJymImNsxiQoufix92DXLCEidytNgClXKE_CwWXXIpxyZncO1BMPNhINNvBh_EUQxYZkkp36L9Nr')
    db.session.add(car_owner)
    db.session.commit()
    return car_owner


def init_db():
    # pass
    db.drop_all()
    db.create_all()
    init_question_set()
    init_service_definitions()
    init_status()
    init_auto_model()
    init_color()
    init_users()
    init_business_owner_task()


# https://www.sakhtafzarmag.com/%D9%84%DB%8C%D8%B3%D8%AA-%D9%82%DB%8C%D9%85%D8%AA/%D9%84%DB%8C%D8%B3%D8%AA-%D9%82%DB%8C%D9%85%D8%AA-%D8%AE%D9%88%D8%AF%D8%B1%D9%88#saipa

if __name__ == "__main__":
    init_db()
