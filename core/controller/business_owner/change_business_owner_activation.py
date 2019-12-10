#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from app import global_logger
from core.controller import BaseController
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result.failure.not_found_user import UserNotFound
from persistence.database.entity.user.auto_service import AutoServiceBusinessOwner
from persistence.database.entity.user.business_owner import BusinessOwner
from persistence.database.entity.user.user import User

logger = global_logger


class ActivationStateController(BaseController):
    def __init__(self, business_owner, converter):
        self.business_owner = business_owner
        self.converter = converter
        self.status = None

    def execute(self):
        existence_result = self._is_existence()
        if not existence_result[0]:
            dct = existence_result[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)
        self.status = existence_result[1].flags[Keys.ACTIVATION_STATUS]
        result_update = self._update_status()
        dct = result_update[1].dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    def _is_existence(self):
        ok, result = User.find(id=self.business_owner.business_owner_id)
        if not ok:
            return False, result

        if len(result) == 0 or not isinstance(result[0], BusinessOwner):
            return False, UserNotFound(status=404, message=MessagesKeys.ID_IS_NOT_IN_DB, params=None)

        return True, result[0]

    def _update_status(self):
        data = {Keys.FLAGS: {Keys.ACTIVATION_STATUS: not self.status}}
        return AutoServiceBusinessOwner.update_by_id(self.business_owner.business_owner_id, db, data)
