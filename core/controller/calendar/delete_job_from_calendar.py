from app import db
from core.controller import BaseController
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result.failure.not_found_job import JobNotFound

from persistence.database.entity.calendar import Calendar


class CalenderDeletionController(BaseController):

    def __init__(self, request_info, converter):
        self.calendar_id = request_info.id
        self.converter = converter

    def execute(self):
        result = Calendar.find(id=self.calendar_id)

        if not result[0]:
            dct = result[1].dictionary_creator()
            return self.serialize(dct, self.converter)

        if not result[1]:
            not_registered = JobNotFound(status=404, message=MessagesKeys.NOT_FOUND_JOB)
            dct = not_registered.dictionary_creator()
            return self.serialize(dct, self.converter)

        delete_res = self.delete_from_calendar()
        dct = delete_res[1].dictionary_creator()
        return self.serialize(dct, self.converter)

    def delete_from_calendar(self):
        calendar = Calendar(id=self.calendar_id)
        data = {Keys.FLAG: {Keys.DELETED: 1}}
        return calendar.update(db, data)


