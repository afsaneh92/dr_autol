import datetime

from app import db, global_logger
from core.controller import BaseController
from core.controller.business_owner.job_process_statuses import BaseJobProcessStatusesController
from core.messages.keys import Keys
from core.result import Result
from core.result.failure.invalid_state_for_job import InvalidState
from core.services.push_notifications.car_owner_announcement import CarOwnerAnnouncement
from persistence.database.entity.job_.job import Job
from persistence.database.entity.stauts import Status

logger = global_logger


class FinishJobRequestController(BaseController):

    def __init__(self, job, converter):
        self.job = job
        self.converter = converter

    def execute(self):
        is_valid = self._load_job()
        if not is_valid[0]:
            dct = is_valid[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)
        is_exist = BaseJobProcessStatusesController.is_exist(is_valid[1])
        if not is_exist[0]:
            dct = is_exist[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        self.job = is_valid[1]
        validate = self._validate_state()
        if not validate[0]:
            dct = validate[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        update_result = self._update_job()
        if not update_result[0]:
            dct = update_result[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        dct = update_result[1].dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    def _validate_state(self):
        if self.job.status_.name == Keys.STATUS_START:
            return True,
        return False, InvalidState(status=404, message=Result.language.INVALID_STATE, params=None)

    def _load_job(self):
        return Job.load_job(self.job.id)

    def _update_job(self):
        error_free, status = FinishJobRequestController.find_suitable_status_for_finish_a_job()
        if not error_free:
            return False, status

        data = {Keys.STATUS_ID: status.id, Keys.FINISH_TIME: str(datetime.datetime.now()).split('.')[0]}
        return self.job.update_status(data, db)

    @staticmethod
    def find_suitable_status_for_finish_a_job():
        error_free, status = Status.find_status(Keys.STATUS_DONE)
        if not error_free:
            return False, error_free
        if status is None:
            return False,
        return True, status
