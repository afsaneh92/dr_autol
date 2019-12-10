#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class HttpStatus(Enum):
    """
    https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
    """
    INTERNAL_ERROR = 500  # done
    BAD_REQUEST = 400  # done
    ACCESS_FORBIDDEN = 403
    NOT_FOUND = 404  # done
    OK = 200


class RequestSuccess(Enum):
    ADD_NEW_USER = "ADD_NEW_USER"
    UPDATE_USER = "UPDATE_USER"
    VALIDATE_USER = "VALIDATE_USER"
    USER_HAS_VALIDATED = "USER_HAS_VALIDATED"  # done
    SUCCESS_LOGIN = "SUCCESS_LOGIN"  # done


class RequestFailure(Enum):
    REGISTERED_BEFORE = "REGISTERED_BEFORE" # done
    FAILED_UPDATE_USER = "FAILED_UPDATE_USER"
    CODE_IS_NOT_VALID = "CODE_IS_NOT_VALID"  # done
    VALIDATED_BEFORE = "VALIDATED_BEFORE"  # done
    WRONG_PASSWORD_OR_PHONE_NUMBER = "WRONG_PASSWORD_OR_PHONE_NUMBER"  # done


class SuccessMessage:
    ADD_NEW_USER = "ثبت کاربر موفقیت آمیز بود."
    UPDATE_USER = "اطلاعات ویرایش شد"


class FailureMessage:
    FAILED_ADD_NEW_USER = "ای بابا"


class DatabaseStatus(Enum):
    INTERNAL_ERROR = "INTERNAL_ERROR"
    SUCCESS_CREATE = "SUCCESS_CREATE"
    SUCCESS_UPDATE = "SUCCESS_UPDATE"
    SUCCESS_DELETE = "SUCCESS_DELETE"
    SUCCESS_READ = "SUCCESS_READ"

    FAIL_CREATE = "FAIL_CREATE"
    FAIL_UPDATE = "FAIL_UPDATE"
    FAIL_DELETE = "FAIL_DELETE"
    FAIL_READ = "FAIL_READ"
