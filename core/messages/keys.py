#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Keys(object):
    GEOM = 'geom'
    TITLE = 'title'
    PAYMENT_JOB = 'payment_job'
    PLATE_NUMBER = 'plate_number'
    PAYMENT_AMOUNT = 'amount'
    TRANSACTION_NUMBER = 'transaction_number'
    STATUS_ACCEPTED_BY_BUSINESS_OWNER = u"تایید شده"
    STATUS_DENIED_BY_BUSINESS_OWNER = u"رد شده"
    STATUS_DONE = u"انجام شده"
    STATUS_PENDING = u"در انتظار تایید"
    STATUS_CANCELLED_BY_BUSINESS_OWNER = u"کنسل شده توسط صاحب بیزینس"
    STATUS_CANCELLED_BY_CAR_OWNER = u"کنسل شده توسط صاحب کار"
    STATUS_TIMEOUT = u"تایم اوت"
    STATUS_START = u"شروع به تعمیر"
    PENDING = 'pending'

    PAYMENT_PSP_TYPE = 'PSP'
    PAYMENT_POSE_TYPE = 'POSE'
    PAYMENT_CASH_TYPE = 'CASH'

    METHOD_GET = 'GET'
    METHOD_PUT = 'PUT'
    METHOD_DELETE = 'DELETE'
    METHOD_UPDATE = 'UPDATE'
    METHOD_POST = 'POST'

    PARAMS = 'params'
    MESSAGE = 'message'
    STATUS = 'status'
    ACTIVATION_STATUS = "activation_status"
    FLAGS = "flags"
    FLAG = "flag"
    REGEX_IS_VALID = 'regex is valid'

    COMPANY = 'company'
    JOB = 'job'
    CAR_ID = 'car_id'
    CAR_OWNER = 'car_owner'
    BUSINESS_OWNER = 'business_owner'
    CAR_PROBLEM = 'car_problem'
    SERVICE_TYPE = 'service_type'
    SERVICE_GRADE = 'service_grade'
    SERVICE_DEFINITIONS = 'service_definitions'
    JOB_ID = 'job_id'
    CALENDAR_ID = 'calendar_id'
    ID = 'id'
    USER_TYPE = 'type'
    TYPES = 'typeS'
    ACCEPT_JOB_REQUEST = 'accept'
    DENY_JOB_REQUEST = 'deny'
    START_JOB_REQUEST = 'start_a_job'
    FINISH_JOB_REQUEST = 'finish_a_job'
    FINISH_PAYMENT_JOB = 'finish_payment_job'
    CANCEL_JOB_BY_BUSINESS_OWNER_REQUEST = 'cancel_job_by_business_owner'
    SOME_MSG_COMES_HERE = 'some msg comes here'
    ACCEPT_ORDER_REQUEST = 'accept_order_request'
    DENY_ORDER_REQUEST = 'deny_order_request'
    PARTIAL_ORDER_REQUEST = 'partial_order_request'

    STATUS_ID = 'status_id'
    MODULE = 'module'
    KLASS = 'class'
    NAME = 'name'
    REG_ID = 'reg_id'
    NEW_JOB_REQUEST = 'new_job_request'
    CAR_INFO = 'car_info'
    ADDRESS = 'address'
    PROBLEM = 'problem'
    GRADE = 'grade'
    CANCEL_JOB = 'cancel_job'
    PHONE_NUMBER = "phone_number"
    PASSWORD = "password"
    OLD_PASSWORD = "old_password"
    NEW_PASSWORD = "new_password"
    BUSINESS_LICENSE = 'business_license'
    FORGET_PASS = 'forget_pass'
    STATE_ID = 'state_id'
    CODE = 'code'
    USER_ID = 'user_id'
    BUSINESS_OWNER_ID = "businessOwnerId"
    CAR_OWNER_ID = "car_owner_id"
    SERVICE_TYPES = 'service_types'
    AUTO_TYPE = 'auto_type'
    APPLICATION_CONTENT_TYPE_JSON = 'application/json'
    START_TIME = 'start_time'
    FINISH_TIME = 'finish_time'
    LAT = 'lat'
    LNG = 'lng'
    SRID = 'srid'
    SRID_VALUE = 4326
    TYPE_USER = 'type_user'
    BUSINESS_OWNER_TASK = "BusinessOwnerTask"
    LIMITED_TIME_TO_FOLLOW_UP_WORK = "43200"
    RANKING_QUESTION_ID = "ranking_question_id"
    QUESTION_AND_RATE = "question_and_rate"
    QUESTION = "question"
    RATE = "rate"
    PAYMENT_TYPE = 'payment_type'
    INVALID_PARAMS = 'invalid_params'
    FULL_PAYMENT_REQUEST = 'full_payment'
    INSTALLMENT_PAYMENT_REQUEST = 'installment_payment'
    AUTO_SERVICE_JOB_REQUEST = 'auto_service_job'
    INSURANCE_JOB_REQUEST = 'insurance_job'
    ACTIONS = 'actions'
    SERVICE_CATEGORY = 'service_category'
    PRODUCTABLE_ITEMS = 'productable_items'
    NON_PRODUCTABLE_ITEMS = 'non_productable_items'
    DELETED = "deleted"
    QUESTION_ID = 'question_id'
    QUESTION_SET_ID = 'question_set_id'
    QUESTION_MANNER = u"از رفتار پرسنل تعمیرگاه چقدر رضایت دارید؟"
    QUESTION_COST = u"از هزینه ی پرداختی (قطعه و اجرت) برای خدمات چقدر رضایت دارید؟",
    QUESTION_PLACE = u"از سهولت دسترسی به نمایندگی شرکت چقدر رضایت دارید؟ ",
    QUESTION_QUALITY = u"میزان رضایت شما از کیفیت خدمات ارایه شده چقدر است؟",
    QUESTION_EVERYTHING = u"به طور کلی چقدر از خدمات رضایت دارید؟"
    QUESTION_RANKING = u" لطفا به سولات پاسخ دهید"
    POINT = "point"
    CAR_OWNER = "﻿CarOwner"
    CAR_OWNER_USER = "﻿CarOwnerUser"
    START_SCHEDULE = 'start_schedule'
    FINISH_SCHEDULE = 'finish_schedule'
    RATE_TO_JOB = "rate_to_job"
    RESEND_CODE = 'resend_code'
    SEND_POLL = 'send_poll'
    EVENT_TYPE = 'event_type'
    QUESTION_TEXT = 'question_text'
    BUSINESS_OWNER_NAME = 'business_owner_name'
    TYPE_OF_SERVICE = 'type_of_service'
    CAR_PROBLEM_ID = "car_problem_id"
    AUTO_TYPE_ID = "auto_type_id"
    SERVICE_TYPE_ID = "service_type_id"
    LONGITUDE = 'LONGITUDE'
    LATITUDE = 'LATITUDE'
    PRICE = 'price'
    SERVICE_DEFINITION = 'service_definition'
    CAR_PROBLEMS = 'car_problems'
    PRODUCT_ID = 'productId'
    BRAND_NAME = 'brand_name'
    VIN_NUMBER = "vin_number"
    AUTO_MODEL = 'auto_model'
    CAR_COLOR = 'color'
    CURRENT_KILOMETER = 'current_kilometer'
    AUTO_MODEL_NAME = "auto_model_name"
    AUTO_MODEL_ID = "auto_model_id"
    OS = "os"
    SUPPLIER = 'supplier'
    LOGIN_SUCCESS = 'login_success'
    COMPANY_ID = 'company_id'
    BRAND_ID = 'brand_id'
    SUPPLIER_ID = 'supplier_id'
    DESCRIPTION = 'description'
    SUB_CATEGORY_ID = 'sub_category_id'
    SECOND_TYPE = "second_type"
    BUSINESS_OWNER_IMAGE = 'business_owner_image'
    KEY_QUESTION="key_question"
    POLL_QUESTIONS= 'poll_questions'
    WORK_SPACE_NAME= 'workSpaceName'
    WRONG_PHONE_NUMBER_OR_PASSWORD = 'wrong phone number or password'
    MINIMUM_ORDER = 'minimum_order'
    ORDER_ID = 'orderId'
    REQUESTED_NUMBER = 'requested_number'
    SUPPLIER_STATUS_NAME = 'supplier_status_name'
    ACCEPTED_NUMBER = 'accepted_number'
    SOLD_NUMBER = 'sold_number'
    TOTAL_SALES = 'total_sales'
    TOTAL_COST_ALL_THE_ORDERS = 'total_cost_all_the_orders'
    ORDER_ITEMS = 'order_items'
    ORDER_ITEMS_ID = 'order_items_id'
    TOTAL_NUM = 'total_num'
    TOTAL_COST_EACH_ORDER = 'total_cost_each_order'
    OPTIONS = 'options'
    SUPPLIER_STATUS_ID = 'supplier_status_id'
    MAX_PRICE = 'max_price'
    MIN_PRICE = 'min_price'
    COMPANY_NAME = 'company_name'
    SUB_CATEGORY_NAME = 'sub_category_name'
    BUY_DONE = 'done'
    ALLOWED_CREDIT = 'allowed_credit'
    USED_CREDIT = 'used_credit'
    EXCEL_PASS = '../../test_cases/fateme/financial_credit.xlsx'
    REST_OF_ALLOW_CREDIT = 'rest_of_allow_credit'
    PARAM = 'param'
    NUMBER = 'number'
    ACCEPT = 'accept'
    DENY = 'deny'