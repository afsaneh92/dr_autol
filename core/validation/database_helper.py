from persistence.database.entity.car_problem import CarProblem
from persistence.database.entity.services import ServiceGradeType


def calculate_job_payment_price(job, off_percent=0):
    return  job.price - ((job.price * off_percent) / 100)
    # error_cause = None
    # result = None
    # try:
    #     error_free, car_problems = CarProblem.find_job_problems(job)
    #     if not error_free:
    #         error_cause = car_problems
    #         raise Exception()
    #     for car_problem in car_problems:
    #         error_free, service_price = ServiceGradeType.load_service_price(car_problem.service_grade,
    #                                                                         car_problem.service_type)
    #         if not error_free:
    #             error_cause = service_price
    #             raise Exception()
    #         job_price = job_price + service_price
    #     job_price = job_price - ((job_price * off_percent) / 100)
    #     result = True, job_price
    # except:
    #     result = False, error_cause
    #
    # return result
