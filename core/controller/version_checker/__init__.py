#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import global_logger
from core.controller import BaseController
from core.messages.keys import Keys

logger = global_logger


class VersionCheckerController(BaseController):

    def __init__(self, app_name, version, converter):
        self.app_name = app_name
        self.version = version
        self.converter = converter

    def execute(self):
        need_update = True
        if self.app_name == u"Dr Autol":
            if self.version < '1':
                need_update = True
            else:
               need_update = False
        if self.app_name == u"همکاران دکتر اتول":
            if self.version < '1':
                need_update = True
            else:
                need_update = False
        dct = {Keys.STATUS: 200, Keys.PARAMS: need_update}
        return self.serialize(dct, converter=self.converter)
