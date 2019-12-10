import logging

from core.controller import BaseController
from core.messages.translator.messages_keys import MessagesKeys
from core.result.failure.not_found_job import JobNotFound
from persistence.database.entity.job_.job import Job

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ListPayableJob(BaseController):
    def __init__(self, car_owner_id, converter):
        self.converter = converter
        self.car_owner_id = car_owner_id
        # self.car_id = car_id

    def execute(self):
        error_free, result = Job.find(car_owner_id=self.car_owner_id)
        if not error_free:
            dct = result.dictionary_creator()
            return self.serialize(dct, self.converter)
        if result:
            error_free, payable_job = self._payable_job()
            if not error_free:
                dct = payable_job.dictionary_creator()
                return self.serialize(dct, converter=self.converter)

            #    if payable_job ro check konam?

            dct = payable_job.dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        else:
            is_busy = JobNotFound(status=404, message=MessagesKeys.NOT_FOUND_JOB, params=None)
            dct = is_busy.dictionary_creator()
            return self.serialize(dct, self.converter)

        # return False,

    def _payable_job(self):
        return Job.find_all_payable_job(car_owner_id=self.car_owner_id)
