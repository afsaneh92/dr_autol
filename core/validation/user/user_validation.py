from core.validation.validator import *
import json


class UserValidator(Validator):
    registration_fields = ['name', 'password', 'phone_number', 'user_type']
    code_validation_fields = ['code', 'phone_number']
    request_type = ""
    fields = None

    def get_fields_for_request_type(self, request_type):
        self.request_type = request_type
        if self.request_type == 'registration':
            self.fields = self.registration_fields
        elif self.request_type == 'code_validation':
            self.fields = self.code_validation_fields
        else:
            return False, 'not valid request type: ' + self.request_type
        return True,

    def validate_schema(self, obj, format_type):
        if not format_type == 'json':
            return False, "Bad format_type. We only accept json: " + format_type

        if 'request_type' not in obj:
            return False, 'no request type'
        res = self.get_request_type(obj['request_type'])
        if res[0] is False:
            return res

        for field in self.fields:
            if field in obj:
                res = self.validate_pattern(obj[field], field)
                if not res[0]:
                    return res
            else:
                return False, "missing_field_" + field
        return True,

    def validate_pattern(self, expression, field_type):
        return self.__check_regex(expression, field_type)

    def __check_regex(self, expression, matching_type):
        result = None
        if matching_type == 'name' or matching_type == 'user_type':
            return True,
        if matching_type == "password":
            result = self.__password_checker(expression)
        elif matching_type == "phone_number":
            result = self.__phone_number_cheker(expression)
        elif matching_type == "code":
            result = self.__code_checker(expression)
        else:
            result = (False, "Bad matching_type")
        return result

    def __password_checker(self, password):
        # must be at least 8 chars, and contains lowercase, uppercase and number
        if re.match(r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,})', password):
            return True,
        else:
            return False, fail_keys.FailKeysForJSON.password_is_not_strength

    def __phone_number_cheker(self, phone_number):
        if re.match(r'09(1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}', phone_number):
            return True,
        else:
            return False, fail_keys.FailKeysForJSON.phone_number_is_not_valid

    def __code_checker(self, code):
        if re.match(r'^[0-9]{4}$', code):
            return True,
        else:
            return False, fail_keys.FailKeysForJSON.code_pattern_is_not_valid


class CarOwner(UserValidator):
    car_registration_fields = ['car_type', 'shasi_number']

    def get_request_type(self, request_type):
        if request_type == "registration" or request_type == "code_validation":
            return UserValidator.get_request_type(self, request_type)
        self.request_type = request_type
        if self.request_type == 'add_new_car':
            self.fields = self.car_registration_fields
        else:
            return False, 'not valid request type: ' + self.request_type
        return True,
