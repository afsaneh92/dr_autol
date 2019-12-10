import time

import datetime

from persistence.database.entity.service_definition import ServicesDefinition
from persistence.database.entity.service_type import ServiceType


def calculate_duration(services_definitions):
    duration = 0
    for services_definition in services_definitions:
        # result = ServiceType.load_service_by_id(service_type)
        # result = ServicesDefinition.load_service_by_id(services_definition)
        # if not services_definition[0]:
        #     return services_definition
        duration += services_definition.service_type.duration

    return  True, duration

def calculate_finish_schedule(start_schedule, duration):
    string = start_schedule
    timestamp = time.mktime(datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S").timetuple()) + (duration * 60)
    return convert_timestamp_to_string(timestamp)

def convert_timestamp_to_string(timestamp):
    t = datetime.datetime.fromtimestamp(timestamp)
    return t.strftime('%Y-%m-%d %H:%M:%S')
