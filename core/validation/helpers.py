#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import xlrd
from flask import make_response, jsonify, session
from datetime import timedelta, datetime, date

from core.messages import fail_keys, HttpStatus
from core.messages import json_keys
from core.messages.keys import Keys
from core.result import Result
from core.result.failure.bad_input_format import BadInputFormat
from core.result.failure.internal_error import InternalError
from core.messages.translator.messages_keys import MessagesKeys
from core.result.failure.invalid_class import InvalidClass
from persistence.database.model.UsersClass import UsersQuery
import datetime
import time


def is_not_empty_phone_number(phone_number):
    if len(phone_number) == 0:
        return False
    else:
        return True


def is_not_empty_password(password):
    if len(password) == 0:
        return False
    else:
        return True


def is_not_empty_user_name(username):
    if len(username) == 0:
        return False
    else:
        return True


def is_request_json(request_http):
    return request_http.is_json


def is_http_request_valid(request_http):
    return is_request_json(request_http)


def is_contains_car_owner_register_json(request_http):
    if json_keys.CarOwnerJSONKeys.phone_number not in request_http.json:
        return False, fail_keys.FailKeysForJSON.missing_phone_number_in_json
    elif json_keys.CarOwnerJSONKeys.name not in request_http.json:
        return False, fail_keys.FailKeysForJSON.missing_name_in_json
    elif json_keys.CarOwnerJSONKeys.password not in request_http.json:
        return False, fail_keys.FailKeysForJSON.missing_password_in_json
    else:
        return True,


def password_regex_checker(password):
    # must be at least 6 chars
    if re.match(r'.{6,}', password):
        return True,
    else:
        return False, fail_keys.FailKeysForJSON.password_is_not_strength


def is_user_registered_before(request_http):
    phone = request_http.json[json_keys.UserJSONKeys.phone_number]
    if not UsersQuery.is_valid_user_by_phone_number(phone):
        return False, fail_keys.FailKeysForJSON.user_has_registered_before
    return True,


def plate_number_regex_checker(plate_number):
    if re.match(u'^[0-9]{2}[آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی]{1,3}[0-9]{3}\-[0-9]{2}$', plate_number):
        if plate_number[2:5].encode('utf-8') == u'الف'.encode('utf-8'):
            return True,
        elif is_string_int(plate_number[3:4]):
            return True,
        else:
            return False, fail_keys.FailKeysForJSON.plate_number_is_not_valid
    else:
        return False, fail_keys.FailKeysForJSON.plate_number_is_not_valid


def vin_number_regex_checker(vin_number):
    if re.match(
            r'^(([a-n,A-N,p-z,P-Z,0-9]{9})([a-h,A-H,j-n,J-N,p,P,r-t,R-T,v-z,V-Z,0-9])([a-h,A-H,j-n,J-N,p-z,P-Z,0-9])(\d{6}))$',
            vin_number):
        return True,
    else:
        return False, fail_keys.FailKeysForJSON.vin_number_is_not_valid


def phone_number_regex_checker(phone_number):
    if re.match(r'09(1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}', phone_number):
        return True,
    else:
        return False, fail_keys.FailKeysForJSON.phone_number_is_not_valid


def name_regex_checker(name):
    if re.match(u'^[آ-یءچ\s]{3,20}$', name):
        return True,
    else:
        return False, fail_keys.FailKeysForJSON.name_is_not_valid


def business_license_regex_checker(number):
    if re.match(r'^[0-9]{10}$', number):
        return True,
    else:
        return False, fail_keys.FailKeysForJSON.number_pattern_is_not_valid


def code_validation_regex_checker(code):
    if re.match(r'^[0-9]{4}$', code):
        return True,
    else:
        return False, fail_keys.FailKeysForJSON.code_pattern_is_not_valid


def check_regex(expression, matching_type):
    result = None
    if matching_type == "password":
        result = password_regex_checker(expression)
    elif matching_type == "phone_number":
        result = phone_number_regex_checker(expression)
    else:
        result = (False, "Bad matching_type")
    return result


def is_contains_validation_code_json(request_http):
    if json_keys.ValidationKeys.phone_number not in request_http.json:
        return False, fail_keys.FailKeysForJSON.missing_phone_number_in_json
    elif json_keys.ValidationKeys.code not in request_http.json:
        return False, fail_keys.FailKeysForJSON
    else:
        return True,


def unrecognized_request():
    dct = {"type": "failure", "message": "The request was not recognized.", "status": HttpStatus.BAD_REQUEST}
    return make_response(jsonify(dct), dct["status"])


def is_logged_in():
    if 'logged_in' not in session or not session['logged_in']:
        dct = {"type": "failure", "message": "you should login first", "status": HttpStatus.BAD_REQUEST}
        return False, make_response(jsonify(dct), dct["status"])
    return True,


def is_string_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def db_error_message(logger, message=Result.language.SOMETHING_WENT_WRONG):
    logger.error(message, exc_info=True)
    return False, InternalError(status=500, message=message, params=None)


def bad_schema_response(params):
    bad_input = BadInputFormat(status=HttpStatus.BAD_REQUEST, message=Result.language.BAD_SCHEMA, params=params)
    dct = bad_input.dictionary_creator()
    return make_response(jsonify(dct), dct["status"])


def convert_datetime_to_timestamp(date_time):
    year = date_time.year
    month = date_time.month
    day = date_time.day
    hour = date_time.hour
    minute = date_time.minute
    second = date_time.second
    string = str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(minute) + ":" + str(second)
    return time.mktime(datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S").timetuple())


def convert_str_to_datetime(string):
    return time.mktime(datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S").timetuple())


def create_class_dynamically(logger, module_path, class_name, request_type=None):
    class_string = module_path + '.' + class_name
    result = None
    try:
        parts = class_string.split('.')
        module = ".".join(parts[:-1])
        m = __import__(module)
        for comp in parts[1:]:
            m = getattr(m, comp)
        result = True, m
    except:
        logger.error(Result.language.NO_CLASS_PATH, exc_info=True)
        result = False, InvalidClass(status=400, message=Result.language.NO_CLASS_PATH,
                                     params={Keys.USER_TYPE: request_type})
    return result


def create_class_dynamic(module_path, class_name):
    module = __import__(module_path)
    return getattr(module, class_name)


def is_time_past(start_time, finish_time):
    if start_time >= finish_time:
        return False
    else:
        return True


def is_start_time_before_finish_time(start_time):
    input_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    current_date = datetime.datetime.now()
    if input_time <= current_date:
        return False
    return True


def time_regex_checker(time):
    if re.match(r'^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})$', time):
        return True,
    else:
        return False, fail_keys.FailKeysForJSON.input_pattern_is_not_valid


def region_checker(polygons):
    for polygon in polygons:
        points_size = len(polygon)
        if points_size < 3:
            return False, Result.language.MISSING_ENOUGH_POINTS
        first_point = polygon[0]
        last_point = polygon[points_size - 1]
        if first_point[Keys.LONGITUDE] != last_point[Keys.LONGITUDE] or first_point[Keys.LATITUDE] != last_point[
            Keys.LATITUDE]:
            return False, Result.language.MISSING_POINT_CONSISTENCY

        for point in polygon:
            lng = is_float(point[Keys.LONGITUDE])
            lat = is_float(point[Keys.LATITUDE])
            if not lng or not lat:
                return False, Result.language.MISSING_POINT_FORMAT

    return True,


def is_float(num):
    try:
        num = float(num) + float(0)
        return True
    except:
        return False


def is_int(num):
    try:
        num += 1
        return True
    except TypeError:
        return False


def is_boolean(item):
    if item == 1:
        return True
    elif item == 0:
        return False
    else:
        return None


def expected_time_for_each_job(start_schedule, finish_schedule):
    return finish_schedule - start_schedule


def calculate_real_time_to_finish_job(start_time, expected_time):
    return start_time + expected_time


def is_latitude(latitude):
    if re.match(r'^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$', str(latitude)):
        return True,
    else:
        return False, fail_keys.FailKeysForJSON.password_is_not_strength


def is_longitude(longitude):
    if re.match(r'^[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$', str(longitude)):
        return True,
    else:
        return False, fail_keys.FailKeysForJSON.password_is_not_strength


def read_data_from_excel_file(excel_file_path):
    open_file = xlrd.open_workbook(excel_file_path)
    sheet = open_file.sheet_by_index(0)

    return True, sheet


def special_time():
    today = datetime.datetime.today()
    rest_of_week = 7 - today.day
    day_till_saturday = 7 - rest_of_week
    saturday = timedelta(hours=(day_till_saturday - 1) * 24)
    friday = timedelta(hours=rest_of_week * 24)
    today = date.today()
    before = datetime.datetime.combine(today, datetime.datetime.min.time()) - saturday
    after = datetime.datetime.combine(today, datetime.datetime.min.time()) + friday
    return before, after
