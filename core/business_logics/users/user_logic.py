from core.messages import json_keys
from core.messages.fail_keys import *
from core.validation import helpers
from persistence.database.model.UsersClass import UsersQuery
from core.services.validation_code import ValidationCodeSMS


def run_car_owner_registration_logic(http_request):
    if not helpers.is_request_json(http_request):
        return FailKeysForJSON.request_is_not_json

    contains_json_keys = helpers.is_contains_car_owner_register_json(http_request)
    print (contains_json_keys)
    if not contains_json_keys[0]:
        return contains_json_keys[1]

    is_password_strength = helpers.password_regex_checker(http_request.json[json_keys.UserJSONKeys.password])
    if not is_password_strength[0]:
        return is_password_strength[1]

    is_phone_number_valid = helpers.phone_number_regex_checker(http_request.json[json_keys.UserJSONKeys.phone_number])

    if not is_phone_number_valid[0]:
        return is_phone_number_valid[1]

    is_user_exists = helpers.is_user_registered_before(http_request)
    if not is_user_exists[0]:
        return is_user_exists[1]

    send_result = ValidationCodeSMS.send_message(http_request.json)
    if not send_result[0]:
        return send_result[1]

    insert_result = UsersQuery.add_user_to_db(http_request.json)
    if not insert_result[0]:
        return insert_result[1]

    return "success"
