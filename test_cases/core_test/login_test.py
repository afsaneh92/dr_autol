#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from client.request_bases import HttpRequest
from core.business_logics.registration.registration import *


class UserRegistrationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # success scenario

    def test_send_user_login_request(self):
        user_request = HttpRequest()
        user_request.is_json = True
        self.assertEqual(send_login(user_request), True)
        user_request.is_json = False
        self.assertEqual(send_login(user_request), False)

    def test_login_user(self):
        pass

    def test_bad_request(self):
        pass

    def test_wrong_pass_and_phone_number(self):
        pass

    def test_internal_server_error(self):
        pass


if __name__ == '__main__':
    unittest.main()
