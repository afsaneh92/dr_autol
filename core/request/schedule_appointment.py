from core.interfaces.serialization import Serializable
from core.messages.keys import Keys
from core.request.base_request import RequestBaseClass
from core.result import Result
from persistence.database.entity.car_problem import CarProblem
from persistence.database.entity.jobs import Jobs


class ScheduleAppointmentRequest(RequestBaseClass):

    def __init__(self, json_obj):
        self.job = None
        self.car_problem = None
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
        for problem in self.car_problem:
            if not isinstance(problem.service_grade, int):
                return False, Result.language.POST_VALIDATION_SERVICE_GRADE
            if not isinstance(problem.service_type, int):
                return False, Result.language.POST_VALIDATION_SERVICE_TYPE
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
            else:
                car_problem = job[Keys.CAR_PROBLEM]
                if Keys.SERVICE_GRADE not in car_problem:
                    missed_params.append(Result.language.MISSING_SERVICE_GRADE_IN_JSON)
                if Keys.SERVICE_TYPE not in car_problem:
                    missed_params.append(Result.language.MISSING_SERVICE_TYPE_IN_JSON)
            if Keys.START_SCHEDULE not in job:
                missed_params.append(Result.language.MISSING_START_SCHEDULE)

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
        result = ScheduleAppointmentRequest.pre_deserialize(json_dict)
        if result[0]:
            job = ScheduleAppointmentRequest.extract_job(json_dict)
            car_problem = ScheduleAppointmentRequest.extract_problem(json_dict)
            self.car_problem = car_problem
            self.job = job
            result_pattern = self.post_deserialize()
            if not result_pattern[0]:
                return result_pattern
            return True, self
        return result

    @staticmethod
    def extract_job(json_dict):
        return Jobs(car_id=json_dict[Keys.JOB][Keys.CAR_ID], car_owner_id=json_dict[Keys.JOB][Keys.CAR_OWNER],
                    business_owner_id=json_dict[Keys.JOB][Keys.BUSINESS_OWNER], start_schedule=json_dict[Keys.JOB][Keys.START_SCHEDULE])

    @staticmethod
    def extract_problem(json_dict):
        problems = []
        for type_ in json_dict[Keys.JOB][Keys.CAR_PROBLEM][Keys.SERVICE_TYPE]:
            problems.append(
                CarProblem(service_grade=json_dict[Keys.JOB][Keys.CAR_PROBLEM][Keys.SERVICE_GRADE], service_type=type_))
        return problems
