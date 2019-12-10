import logging
from core.controller import BaseController
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result.failure.faile_to_find_list import FailToFindList
from core.result.success.success_list_of_unfinished_job import SuccessListOfUnfinishedJob
from persistence.database.entity.job_.autoservice_job import AutoServiceJob
from persistence.database.entity.job_.job import Job
from persistence.database.entity.stauts import Status
import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ListUnfinishedJob(BaseController):
    def __init__(self, converter):
        self.converter = converter

    def execute(self):
        error_free, find_all_result = self._unfinished()
        if not error_free:
            dct = find_all_result.dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        dct = find_all_result.dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    @staticmethod
    def _unfinished():
        time_delta = datetime.timedelta(hours=12)
        late_to_finish_jobs = []
        late_to_start_jobs = []

        error_free_start_status, start_status = Status.find_status(Keys.STATUS_START)
        error_free_accepted_status, accepted_status = Status.find_status(Keys.STATUS_ACCEPTED_BY_BUSINESS_OWNER)
        if not error_free_start_status:
            return accepted_status

        list_started_jobs = Job.find(status_id=start_status.id)[1]
        list_accepted_jobs = Job.find(100000, status_id=accepted_status.id)[1]

        if list_started_jobs is not []:

            for unfinished_job in list_started_jobs:
                now_time = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                                      "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M:%S")
                if unfinished_job.start_time is not None:
                    real_start_time = unfinished_job.start_time.strftime("%Y-%m-%d %H:%M:%S")
                    start_time_schedule = unfinished_job.start_schedule.strftime("%Y-%m-%d %H:%M:%S")
                    finish_time_schedule = unfinished_job.finish_schedule.strftime("%Y-%m-%d %H:%M:%S")

                    time_length_to_finish_job = datetime.datetime.strptime(finish_time_schedule,
                                                                           '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(
                        start_time_schedule, '%Y-%m-%d %H:%M:%S')

                    expected_time_to_finish = datetime.datetime.strptime(real_start_time,
                                                                         '%Y-%m-%d %H:%M:%S') + time_length_to_finish_job

                    if now_time > expected_time_to_finish.strftime("%Y-%m-%d %H:%M:%S"):
                        late_to_finish_jobs.append(unfinished_job.id)
                else:
                    start_time_schedule = unfinished_job.start_schedule.strftime("%Y-%m-%d %H:%M:%S")
                    if start_time_schedule + str(time_delta) > now_time:
                        late_to_finish_jobs.append(unfinished_job.id)

        if list_accepted_jobs is not []:
            for accepted_job in list_accepted_jobs:

                job_limited_time = datetime.datetime.strptime(str(accepted_job.start_schedule + time_delta),
                                                              "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                now_time = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                                      "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M:%S")

                if now_time > job_limited_time:
                    late_to_start_jobs.append(accepted_job.id)

        wanted_list = late_to_start_jobs + late_to_finish_jobs

        error_free, unfinished_jobs = AutoServiceJob.unfinished(wanted_list)
        if not error_free:
            return unfinished_jobs
        return True, SuccessListOfUnfinishedJob(status=200, message=MessagesKeys.SUCCESS_LIST,
                                                params=unfinished_jobs)
