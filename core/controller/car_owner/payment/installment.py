from app import db, global_logger
from core.controller import BaseController
from core.controller.business_owner.job_process_statuses import BaseJobProcessStatusesController
from core.messages.keys import Keys
from core.services.push_notifications.car_owner_announcement import CarOwnerAnnouncement
from persistence.database.entity.jobs import Jobs
from persistence.database.entity.job_.autoservice_job import AutoServiceJob
from persistence.database.entity.stauts import Status

logger = global_logger


class InstallmentPaymentRequestController(BaseController):

    def __init__(self, job, payment, converter):
        self.job = job
        self.payment = payment
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
        update_result = self._update_job()
        if not update_result[0]:
            dct = update_result[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        self.push_notification_to_car_owner()

        dct = update_result[1].dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    def _load_job(self):
        return Jobs.load_job(self.job.id)

    def _update_job(self):
        status = Status.query.filter(Status.name == Keys.STATUS_ACCEPTED_BY_BUSINESS_OWNER).first()
        data = {Keys.STATUS_ID: status.id}
        return AutoServiceJob.accept_deny_job(self.job, data, db)

    def push_notification_to_car_owner(self):
        CarOwnerAnnouncement.accept_job(self.job)
