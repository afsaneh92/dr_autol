#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from app import db
from core.controller import BaseController
from core.messages.translator.messages_keys import MessagesKeys
from core.result.failure.bad_input_format import BadInputFormat
from core.result.failure.business_owner_is_busy import BusinessOwnerIsBusy
from core.result.failure.not_register_before import NotRegisteredBefore
from core.validation.helpers import is_time_past, is_start_time_before_finish_time
from persistence.database.entity.calendar import Calendar
from persistence.database.entity.user.user import User

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class CalenderInsertionController(BaseController):

    def __init__(self, request_info, converter):
        self.start_time = request_info.start_time
        self.finish_time = request_info.finish_time
        self.business_owner_id = request_info.business_owners_id
        self.converter = converter
        self.business_owner = None

    def execute(self):

        if not is_time_past(self.start_time, self.finish_time):
            # TODO make these lines like a decorators
            # needs refactor... create a decorator function for handling all of serialization. Something like below
            # class Name:
            #     name = "Amish"
            #
            # def create(cls, *args):
            #     return cls(status= status)
            # name = create(Name, status=404)
            # name.name
            # 'Amish'
            not_valid_time = BadInputFormat(status=400, message=MessagesKeys.TIME_IS_NOT_CORRECT, params=None)
            dct = not_valid_time.dictionary_creator()
            return self.serialize(dct, self.converter)
        if not is_start_time_before_finish_time(self.start_time):
            not_valid_time = BadInputFormat(status=400, message=MessagesKeys.TIME_IS_NOT_CORRECT, params=None)
            dct = not_valid_time.dictionary_creator()
            return self.serialize(dct, self.converter)

        error_free, result = User.find(id=self.business_owner_id)
        if not error_free:
            dct = result.dictionary_creator()
            return self.serialize(dct, self.converter)

        if not result:
            not_registered = NotRegisteredBefore(status=404, message=MessagesKeys.NOT_REGISTERED_BEFORE)
            dct = not_registered.dictionary_creator()
            return self.serialize(dct, self.converter)

        res = self.is_free_business_owner()
        if not res[0]:
            return res[1]
        self.business_owner = result[0]
        insert_res = self.insert_in_db()
        dct = insert_res[1].dictionary_creator()
        return self.serialize(dct, self.converter)

    def is_free_business_owner(self):
        error_free, count = Calendar.count_conflict(self.start_time, self.finish_time, self.business_owner_id)
        if not error_free:
            dct = count.dictionary_creator()
            return False, self.serialize(dct, self.converter)
        if count != 0:
            is_busy = BusinessOwnerIsBusy(status=404, message=MessagesKeys.BUSINESS_OWNER_IS_BUSY, params=None)
            dct = is_busy.dictionary_creator()
            return False, self.serialize(dct, self.converter)
        return True,

    def insert_in_db(self):
        calendar = Calendar(start_time=self.start_time, finish_time=self.finish_time,
                            business_owner_id=self.business_owner_id)
        result = calendar.add(db, calendar)
        return result

