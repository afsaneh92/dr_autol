import logging

from core.controller import BaseController
from core.messages.keys import Keys
from core.validation.session_helper.session_manager import SessionManager
from persistence.database.entity.job_.job import Job
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ListFinishedJob(BaseController):
    def __init__(self, converter):
        self.converter = converter

    def execute(self):
        find_all_result = self._finished_job()
        if not find_all_result[0]:
            dct = find_all_result[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        dct = find_all_result[1].dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    def _finished_job(self):
        car_owner_id = SessionManager.retrieve_session_value_by_key(Keys.USER_ID)
        return Job.find_all_finished_job(car_owner_id=car_owner_id)
