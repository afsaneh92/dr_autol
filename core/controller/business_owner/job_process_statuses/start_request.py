import datetime

from app import db, global_logger
from core.controller import BaseController
from core.controller.business_owner.job_process_statuses import BaseJobProcessStatusesController
from core.messages.keys import Keys
from core.result import Result
from core.result.failure.invalid_state_for_job import InvalidState
from persistence.database.entity.job_.autoservice_job import AutoServiceJob
from persistence.database.entity.job_.job import Job
from persistence.database.entity.stauts import Status

logger = global_logger


class StartJobRequestController(BaseController):

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

        overlap = self._has_overlap()
        if not overlap[0]:
            dct = overlap[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        update_result = self._update_job()
        if not update_result[0]:
            dct = update_result[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        dct = update_result[1].dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    def _validate_state(self):
        if self.job.status_.name == Keys.STATUS_ACCEPTED_BY_BUSINESS_OWNER:
            return True,
        return False, InvalidState(status=404, message=Result.language.INVALID_STATE, params=None)

    def _has_overlap(self):
        result = AutoServiceJob.has_overlap_jobs(self.job)
        if not result[0]:
            return result
        count = int(result[1])
        if int(count) == 0:
            result = True,
        else:
            result = False, InvalidState(status=404, message=Result.language.INVALID_STATE, params=None)
        return result

    def _load_job(self):
        return Job.load_job(self.job.id)

    def _update_job(self):
        status = Status.query.filter(Status.name == Keys.STATUS_START).first()
        data = {Keys.STATUS_ID: status.id, Keys.START_TIME: str(datetime.datetime.now()).split('.')[0]}
        return self.job.update_status(data, db)
