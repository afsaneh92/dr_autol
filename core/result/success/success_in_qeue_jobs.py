from core.messages.keys import Keys
from core.result import Result


class SuccessInQueueJobs(Result):
    def dictionary_creator(self):
        desired_jobs = []
        sorted_list = sorted(self.params , key=lambda result: result.Job.start_schedule)
        for result in sorted_list:
            dictionary_item = {Keys.JOB_ID: result.Job.id, Keys.PRICE: str(result.Job.price), 'status': result.Job.status_.name,
                               Keys.START_SCHEDULE: result.Job.start_schedule,
                               Keys.SERVICE_DEFINITION: {
                                   Keys.GRADE: result.Job.car_problems[0].services_definition.service_grade,
                                   Keys.SERVICE_CATEGORY: result.Job.car_problems[
                                       0].services_definition.service_category},
                               Keys.CAR_INFO: {Keys.PLATE_NUMBER: result.Car.plate_number,
                                               Keys.AUTO_TYPE: result.Car.auto_type_.name}}

            car_problems = []
            for car_problem in result[0].car_problems:
                car_problems.append(car_problem.services_definition.service_type.name)

            dictionary_item[Keys.CAR_PROBLEMS] = car_problems
            desired_jobs.append(dictionary_item)
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.SUCCESS_IN_QUEUE_JOBS, Keys.PARAMS: desired_jobs}
