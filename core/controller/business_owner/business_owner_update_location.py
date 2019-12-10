#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.exc import InvalidRequestError

from app import db, global_logger
from core.controller import BaseController
from core.messages.translator.messages_keys import MessagesKeys
from core.result.failure.not_found_user import UserNotFound
from core.result.success.success_update import SuccessUpdate
from core.validation.helpers import db_error_message
from persistence.database.entity.user.business_owner import BusinessOwner

logger = global_logger


class BusinessOwnerUpdateLocationController(BaseController):
    def __init__(self, business_owner, converter):
        self.business_owner = business_owner
        self.converter = converter

    def execute(self):
        existence_result = self._is_existence()
        if not existence_result[0]:
            dct = existence_result[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)
        result_update = self._update_location()
        dct = result_update[1].dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    def _is_existence(self):
        ok, result = BusinessOwner.find(id=self.business_owner.id)
        if not ok:
            return False, result

        if len(result) == 0:
            return False, UserNotFound(status=404, message=MessagesKeys.ID_IS_NOT_IN_DB, params=None)

        return True, result[0]

    def _update_location(self):

        try:
            BusinessOwner.update_lng_lat(self.business_owner.id, self.business_owner.lng, self.business_owner.lat, db)
            success = SuccessUpdate(status=200, message=MessagesKeys.SUCCESS_UPDATE)
            result = True, success
        except InvalidRequestError as error:
            result = db_error_message(logger)
            db.session.rollback()

        except:
            result = db_error_message(logger)
            db.session.rollback()
        return result
