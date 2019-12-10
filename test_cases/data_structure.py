# end pints

"""/register_user"""
# input json

registration_request = {
    "phone_number": "09372943761",
    "name": "amir@iws.com",
    "password": "123Amish3",
    "user_type": 'car_owner'
}

# output json
output = {
    "message": "Internal database error",
    "status": 400,
    "type": "failure"
}

"""/validate_user"""

validation_code = {
    "phone_number": "09372943761",
    "code": "1234"
}

fail_json = {
    "message": "Internal database error",
    "status": 400,
    "type": "failure"
}

"""/car_owner/cars/<car_id>"""  # PUT

input = {
    "car_id": 1,  # car's id
    "new_info": {
        "vin_number": "123654",
        "plate_number": "79t749-33",
        "name": "206 type 6",
        "auto_type": 1  # auto type id
    }
}

"""/register_admin"""

input = {
    "name": "امیر",
    "last_name": "شعبانی",
    "password": "Amish1234",
    "phone_number": "09125200000",
    "user_type": "admin"
}



# ########

iws_registration = {
    "name": "فارسی",
    "password": "123Amish3",
    "phone_number": "09125200780",
}
