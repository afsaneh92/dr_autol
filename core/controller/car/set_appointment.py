from app import db, global_logger
from core.controller import BaseController
from core.messages.keys import Keys
from core.services.push_notifications.iws_announcement import IWSAnnouncement
from persistence.database.entity.job_.job import Job
from persistence.database.entity.service_grade import ServiceGrade
from utilities import calculate_duration, calculate_finish_schedule

logger = global_logger


# class SetAppointmentController(BaseController):
#
#     def __init__(self, job, problem, converter):
#         self.problem = problem
#         self.job = job
#         self.converter = converter
#
#     def execute(self):
#         result_finish_schedule = self._calculate_finish_schedule()
#         if not result_finish_schedule[0]:
#             dct = result_finish_schedule[1].dictionary_creator()
#             return self.serialize(dct, converter=self.converter)
#
#         result_registration_status = self._register_car_problems()
#         if not result_registration_status[0]:
#             dct = result_registration_status[1].dictionary_creator()
#             return self.serialize(dct, converter=self.converter)
#         job_id = result_registration_status[1].params[Keys.ID]
#         self.send_notification(job_id)
#         dct = result_registration_status[1].dictionary_creator()
#         return self.serialize(dct, converter=self.converter)
#
#     def _register_car_problems(self):
#         return Job.register_problem(db, self.job, self.problem)
#
#     def send_notification(self, job_id):
#         types = []
#         for problem in self.problem:
#             types.append(problem.service_type)
#
#         grade = self.problem[0].service_grade
#         service_grade = SetAppointmentController.load_service_grade(grade)
#         IWSAnnouncement.request_notification(service_grade, types, self.job.business_owner_id, self.job.car_id, job_id)
#
#     def _calculate_finish_schedule(self):
#         service_types = []
#         for problem in self.problem:
#             service_types.append(problem.service_type)
#         result = calculate_duration(service_types)
#         if not result[0]:
#             return False, result[1]
#         self.job.finish_schedule = calculate_finish_schedule(self.job.start_schedule, result[1])
#         return True,
#
#     @staticmethod
#     def load_service_grade(grade):
#         return ServiceGrade.load_service_grade(grade)
