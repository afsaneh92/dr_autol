import random

from flask import session

from app import db
from core.controller import BaseController
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.request.forget_password import States
from core.result import Result
from core.result.failure.false_code_validation import FalseCodeValidation
from core.result.failure.registered_before import RegisteredBefore
from core.result.failure.wrong_pass_or_phone_number import WrongPassOrPhoneNumber
from core.result.success.success_send_code import SuccessForgetPass
from core.services.channel import SMSCodeValidation
from persistence.database.entity.user.user import User


class ForgetPasswordController(BaseController):

    def __init__(self, request_info, converter):
        self.state_id = request_info.state_id
        self.type_user = session[Keys.FORGET_PASS][Keys.TYPE_USER]

        if self.state_id == States.PHONE_NUMBER:
            self.phone_number = request_info.phone_number
        elif self.state_id == States.CODE:
            self.code = request_info.code
        elif self.state_id == States.PASSWORD:
            self.password = request_info.password

        self.converter = converter

    def execute(self):
        if self.state_id == States.PHONE_NUMBER:
            return self.handle_state_phone_number()
        elif self.state_id == States.RESEND_CODE:
            return self.handle_state_resend_code()
        elif self.state_id == States.CODE:
            return self.handle_state_code()

        elif self.state_id == States.PASSWORD:
            return self.handle_state_password()

        elif self.state_id == States.RESEND_CODE:
            return self.handle_state_resend_code()


    def handle_state_code(self):
        if self.code == session[Keys.FORGET_PASS][Keys.CODE]:
            user_id = session[Keys.FORGET_PASS][Keys.USER_ID]
            session.update(
                {Keys.FORGET_PASS: {
                    Keys.STATE_ID: States.PASSWORD,
                    Keys.USER_ID: user_id,
                    Keys.TYPE_USER: self.type_user
                }})
            result = self.create_success_message(Result.language.CODE_RECEIVE_SUCCESSFULLY)
            dct = result.dictionary_creator()
            return self.serialize(dct, self.converter)
        session.update(
            {Keys.FORGET_PASS: {
                Keys.STATE_ID: States.RESEND_CODE,
                Keys.USER_ID: session[Keys.FORGET_PASS][Keys.PHONE_NUMBER],
                Keys.TYPE_USER: self.type_user,
                Keys.NAME: session[Keys.FORGET_PASS][Keys.NAME]
            }})

        result = self.create_fail_message(Result.language.CODE_RECEIVE_FAILED)
        dct = result.dictionary_creator()
        return self.serialize(dct, self.converter)

    def handle_state_password(self):
        result = None
        user = User(phone_number=session[Keys.FORGET_PASS][Keys.USER_ID])
        if user.is_registered():
            hashed_password = user.generate_hash_password(self.password)
            dct = {Keys.PASSWORD: hashed_password}
            result = user.update(db, dct)
        else:
            not_registered_before = RegisteredBefore(status=404, message=MessagesKeys.NOT_REGISTERED_BEFORE,
                                                     params=None)

            dct = not_registered_before.dictionary_creator()
            return self.serialize(dct, self.converter)

        if not result[0]:
            dct = result.dictionary_creator()
            return self.serialize(dct, self.converter)
        session.clear()
        result = self.create_success_message(Result.language.PASSWORD_CHANGE_SUCCESSFULLY)
        dct = result.dictionary_creator()
        return self.serialize(dct, self.converter)

    def handle_state_phone_number(self):
        session[Keys.FORGET_PASS][Keys.USER_ID] = self.phone_number
        user = User.find(phone_number=session[Keys.FORGET_PASS][Keys.USER_ID])
        if not user[0]:
            dct = user[1].dictionary_creator()
            return self.serialize(dct, self.converter)

        if len(user[1]) == 0:
            return self.create_no_user_dct(Result.language.NOT_REGISTERED_BEFORE)

        sms = SMSCodeValidation(user[1][0].name, self.phone_number, SMSCodeValidation.create_random_code())
        _, code = sms.send_validation_code()

        result = self.create_success_message(Result.language.CODE_SEND_SUCCESSFULLY)
        dct = result.dictionary_creator()
        session.update(
            {Keys.FORGET_PASS: {
                Keys.STATE_ID: States.CODE,
                Keys.CODE: str(code),
                Keys.USER_ID: self.phone_number,
                Keys.TYPE_USER: self.type_user,
                Keys.NAME: user[1][0].name
            }})
        return self.serialize(dct, self.converter)

    def create_success_message(self, message):
        return SuccessForgetPass(status=200, message=message, params=None)

    def create_fail_message(self, message):
        return FalseCodeValidation(status=404, message=message)

    def create_no_user_dct(self, message):
        params = {Keys.PHONE_NUMBER: self.phone_number}
        res = WrongPassOrPhoneNumber(status=404, message=message, params=params)
        dct = res.dictionary_creator()
        return self.serialize(dct, self.converter)

    @staticmethod
    def create_random_code():
        return random.randint(1000, 10000)

    def handle_state_resend_code(self):
        sms = SMSCodeValidation(session[Keys.FORGET_PASS][Keys.NAME], session[Keys.FORGET_PASS][Keys.USER_ID], SMSCodeValidation.create_random_code())
        _, code = sms.send_validation_code()
        result = self.create_success_message(Result.language.CODE_SEND_SUCCESSFULLY)
        dct = result.dictionary_creator()
        user_id = session[Keys.FORGET_PASS][Keys.USER_ID]
        user_type = session[Keys.FORGET_PASS][Keys.TYPE_USER]
        session.update(
            {Keys.FORGET_PASS: {
                Keys.STATE_ID: States.CODE,
                Keys.CODE: str(code),
                Keys.USER_ID: user_id,
                Keys.TYPE_USER: user_type
            }})
        return self.serialize(dct, self.converter)
