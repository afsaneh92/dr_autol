from core.messages.keys import Keys
from core.request.base_request import RequestBaseClass
from core.interfaces.serialization import Serializable
from core.result import Result
from persistence.database.entity.job_.autoservice_job import AutoServiceJob


class AutoServiceRequest(RequestBaseClass):
    def __init__(self, json_obj):
        self.job = None
        self.car_problems = None
        self.service_definition = None
        self.json_obj = json_obj

    def validate_pattern(self):
        res = self._validate_job()
        if not res[0]:
            return res
        res = self.validate_problem()
        if not res[0]:
            return res

        return True,

    def validate_problem(self):
        if not isinstance(self.car_problems, dict):
            return False, Result.language.POST_VALIDATION_SERVICE_GRADE
        if not isinstance(self.service_definition, dict):
            return False, Result.language.POST_VALIDATION_SERVICE_GRADE

        # for problem in self.car_problems:
        #     # if not isinstance(problem.services_definition_id, int):
        #     #     return False, Result.language.POST_VALIDATION_SERVICE_GRADE
        #     if not isinstance(problem.services_definition_id, dict):
        #         return False, Result.language.POST_VALIDATION_SERVICE_GRADE
            # if not isinstance(problem.service_definition, int):
            #     return False, Result.language.POST_VALIDATION_SERVICE_GRADE
            # if not isinstance(problem.service_type, int):
            #     return False, Result.language.POST_VALIDATION_SERVICE_TYPE
        return True,

    def _validate_job(self):
        if not isinstance(self.job.car_id, int):
            return False, Result.language.POST_VALIDATION_CAR_ID
        if not isinstance(self.job.business_owner_id, int):
            return False, Result.language.POST_VALIDATION_BUSINESS_OWNER_ID
        if not isinstance(self.job.car_owner_id, int):
            return False, Result.language.POST_VALIDATION_CAR_OWNER_ID
        return True,

    @staticmethod
    def pre_deserialize(json_dict):
        """
        before deserializing, run this method. It help to check json and confirm it's schema.
        :param json_dict:
        :return:
        """
        missed_params = []
        if Keys.SECOND_TYPE not in json_dict:
            missed_params.append(Result.language.MISSING_SECOND_TYPE)

        if Keys.JOB not in json_dict:
            missed_params.append(Result.language.MISSING_JOB_IN_JSON)
        else:
            job = json_dict[Keys.JOB]
            if Keys.CAR_OWNER not in job:
                missed_params.append(Result.language.MISSING_CAR_OWNER_IN_JSON)
            if Keys.BUSINESS_OWNER not in job:
                missed_params.append(Result.language.MISSING_BUSINESS_OWNER_IN_JSON)
            if Keys.CAR_ID not in job:
                missed_params.append(Result.language.MISSING_CAR_ID_IN_JSON)
            if Keys.CAR_PROBLEM not in job:
                missed_params.append(Result.language.MISSING_CAR_PROBLEM_IN_JSON)
            if Keys.START_SCHEDULE not in job:
                missed_params.append(Result.language.MISSING_START_SCHEDULE)


            else:
                car_problem = job[Keys.CAR_PROBLEM]
                if Keys.SERVICE_GRADE not in car_problem:
                    missed_params.append(Result.language.MISSING_SERVICE_GRADE_IN_JSON)
                if Keys.SERVICE_DEFINITIONS not in car_problem:
                    missed_params.append(Result.language.MISSING_SERVICE_TYPE_IN_JSON)

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
        result = AutoServiceRequest.pre_deserialize(json_dict)
        if result[0]:
            job = AutoServiceRequest.extract_job(json_dict)
            car_problem = AutoServiceRequest.extract_problem(json_dict)
            service_definition = AutoServiceRequest.extract_service_definition(json_dict)
            # self.car_problem = car_problem
            self.job = job
            self.car_problems = car_problem
            self.service_definition = service_definition
            # self.job.car_problems.extend(car_problem)
            result_pattern = self.post_deserialize()
            if not result_pattern[0]:
                return result_pattern
            return True, self
        return result

    @staticmethod
    def extract_job(json_dict):
        return AutoServiceJob(car_id=json_dict[Keys.JOB][Keys.CAR_ID], car_owner_id=json_dict[Keys.JOB][Keys.CAR_OWNER],
                              business_owner_id=json_dict[Keys.JOB][Keys.BUSINESS_OWNER],
                              start_schedule=json_dict[Keys.JOB][Keys.START_SCHEDULE], second_type= json_dict['second_type'])

    @staticmethod
    def extract_problem(json_dict):
        problems = json_dict[Keys.JOB][Keys.CAR_PROBLEM][Keys.SERVICE_DEFINITIONS]

        # for service_id in json_dict[Keys.JOB][Keys.CAR_PROBLEM][Keys.SERVICE_DEFINITION]:
        #
        #     problems.append(CarProblem(services_definition_id=service_id))


        # for type_ in json_dict[Keys.JOB][Keys.CAR_PROBLEM][Keys.SERVICE_TYPE]:
        #     problems.append(
        #         CarProblem(service_grade=json_dict[Keys.JOB][Keys.CAR_PROBLEM][Keys.SERVICE_GRADE], service_type=type_,
        #                    service_definition=json_dict[Keys.JOB][Keys.CAR_PROBLEM][Keys.SERVICE_DEFINITION]))
        return problems

    @staticmethod
    def extract_service_definition(json_dict):
        service_grade = json_dict[Keys.JOB][Keys.CAR_PROBLEM][Keys.SERVICE_GRADE]
        service_category = json_dict[Keys.JOB][Keys.CAR_PROBLEM][Keys.SERVICE_CATEGORY]
        return {Keys.SERVICE_GRADE: service_grade, Keys.SERVICE_CATEGORY: service_category}
