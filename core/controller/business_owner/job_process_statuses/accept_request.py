import logging

from app import db
from core.controller import BaseController
from core.controller.business_owner.job_process_statuses import BaseJobProcessStatusesController
from core.messages.keys import Keys
from core.result import Result
from core.result.failure.invalid_state_for_job import InvalidState
from core.services.push_notifications.car_owner_announcement import CarOwnerAnnouncement
# from persistence.database.entity.jobs import Jobs
from persistence.database.entity.job_.autoservice_job import AutoServiceJob
from persistence.database.entity.job_.job import Job
from persistence.database.entity.stauts import Status

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class AcceptController(BaseController):

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

        self.push_notification_to_car_owner()

        dct = update_result[1].dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    def _load_job(self):
        return Job.load_job(self.job.id)

    def _update_job(self):
        status = Status.query.filter().first()
        data = {Keys.STATUS_ID: status.id}
        return AutoServiceJob.accept_deny_job(self.job, data, db, where_clause={'status_': Keys.STATUS_PENDING})

    def _validate_state(self):
        if self.job.status_.name != Keys.STATUS_PENDING:
            return False, InvalidState(status=404, message=Result.language.INVALID_STATE, params=None)
        return True,

    def push_notification_to_car_owner(self):
        CarOwnerAnnouncement.accept_job(self.job)
