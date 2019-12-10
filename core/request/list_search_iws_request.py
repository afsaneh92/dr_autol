from core.interfaces.serialization import Serializable
from core.messages.keys import Keys
from core.request.base_request import RequestBaseClass
from core.validation.helpers import region_checker
from persistence.database.entity.search_iws import IWSSearchParameters


class ListSearchIWSRequest(RequestBaseClass):

    def __init__(self, json_obj):
        self.service_grade = None
        self.service_category = None
        self.business_owner_type = None
        self.options = None
        self.json_obj = json_obj

    def validate_pattern(self):
        res = self._validate_options(self.options)
        if not res[0]:
            return res

        res = self._id_checker(self.service_grade, res[1])
        if not res[0]:
            return res

        return True, res[1]

    def _validate_options(self, options):
        search = IWSSearchParameters()
        if not options:
            return True, search
        if 'service_types' in options:
            if not isinstance(options['service_types'], list):
                return False, "service_types is not array"
            search.service_types = options['service_types']
        if 'region' in options:
            if not isinstance(options['region'], list):
                return False, "region is not array"
            result = self._region_checker(options['region'])
            if not result[0]:
                return False, result[1]
            search.region = options['region']
        if 'name' in options:
            if not isinstance(options['name'], unicode):
                return False, "name is not str"
            search.name = options['name']
        if Keys.START_SCHEDULE in options:
            search.start_schedule = options[Keys.START_SCHEDULE]
        search.service_category = self.service_category
        # search.business_owner_type = self.business_owner_type
        return True, search

    def _id_checker(self, id, search):
        if id is int:
            return False,
        search.service_grade = id
        return True, search

    @staticmethod
    def pre_deserialize(json_dict):
        """
        before deserializing, run this method. It help to check json and confirm it's schema.
        :param json_dict:
        :return:
        """
        missed_params = []
        # if 'business_owner_type' not in json_dict:
        #     missed_params.append("missing_business_owner_type_in_json")

        if 'service_category' not in json_dict:
            missed_params.append("missing_service_category_in_json")

        if 'service_grade' not in json_dict:
            missed_params.append("missing_service_grade_in_json")
        if 'options' not in json_dict:
            missed_params.append("missing_options_in_json")

        if len(missed_params) > 0:
            return False, missed_params

        return True,

    def post_deserialize(self):
        return self.validate_pattern()

    def deserialize(self):
        if not type(self.json_obj) is dict:
            json_dict = Serializable.convert_input_to_dict(self.json_obj)
        else:
            json_dict = self.json_obj
        result = ListSearchIWSRequest.pre_deserialize(json_dict)
        if result[0]:

            self.options = json_dict['options']
            self.service_grade = json_dict['service_grade']
            # self.business_owner_type = json_dict['business_owner_type']
            self.service_category = json_dict['service_category']
            result_pattern = self.post_deserialize()
            if not result_pattern[0]:
                return result_pattern
            return True, result_pattern[1]
        return result

    def _region_checker(self, regions):
        return region_checker(regions)
