from app import global_logger
from core.validation.helpers import db_error_message


def update_record_from_dictionary(obj, data):
    result = True,
    try:
        for property, value in data.iteritems():
            setattr(obj, property, value)
        result = True, obj
    except AttributeError:
        result = False, db_error_message(global_logger)
    return result