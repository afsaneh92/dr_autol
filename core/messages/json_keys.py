from abc import ABCMeta, abstractmethod


class JSONKeys:
    request_type = "__request_type__"
    __metaclass__ = ABCMeta


class UserJSONKeys(JSONKeys):
    id = 'id'
    phone_number = 'phone_number'
    name = 'name'
    password = 'password'
    user_type = "user_type"
    pass

    def __init__(self):
        pass


class CarOwnerJSONKeys(UserJSONKeys):
    def __init__(self):
        pass


class ValidationKeys(JSONKeys):
    phone_number = 'phone_number'
    code = 'code'

