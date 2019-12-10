from passlib.handlers.pbkdf2 import pbkdf2_sha256

from app import db
from core.controller import BaseController
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result import Result
from core.result.failure.registered_before import RegisteredBefore
from core.result.failure.wrong_pass_or_phone_number import WrongPassOrPhoneNumber
from core.result.success.success_send_code import SuccessForgetPass
from persistence.database.entity.user.user import User


class ChangePasswordController(BaseController):
    def __init__(self, request_info, phone_number, converter):
        self.new_password = request_info.new_password
        self.old_password = request_info.old_password
        self.converter = converter
        self.phone_number = phone_number
        self.type_user = request_info.type_user

    def execute(self):
        res = self._authentication()
        if not res[0]:
            dct = res[1].dictionary_creator()
            return self.serialize(dct, self.converter)
        result = self._update_password()
        return result

    def _update_password(self):
        result = None
        user = User(phone_number=self.phone_number, validate=True)
        if user.is_registered():
            if user.is_valid():
                hashed_password = user.generate_hash_password(self.new_password)
                dct = {Keys.PASSWORD: hashed_password}
                result = user.update(db, dct)

            elif user.is_invalid():
                pass
        else:
            not_registered_before = RegisteredBefore(status=404, message=MessagesKeys.NOT_REGISTERED_BEFORE,
                                                     params=None)
            return False, not_registered_before
        if result[0]:
            result = self.create_success_message(Result.language.PASSWORD_CHANGE_SUCCESSFULLY)
            dct = result.dictionary_creator()
            return self.serialize(dct, self.converter)

        dct = result.dictionary_creator()
        return self.serialize(dct, self.converter)

    def _authentication(self):
        find_result = User.find(phone_number=self.phone_number, validate=True)
        if not find_result[0]:
            return find_result
        if not len(find_result[1]):
            # in eygam ro chek kon
            not_registered_before = RegisteredBefore(status=404, message=MessagesKeys.NOT_REGISTERED_BEFORE,
                                                     params=None)
            return False, not_registered_before
        verified_pass = pbkdf2_sha256.verify(self.old_password, find_result[1][0].password)
        if not verified_pass:
            params = {Keys.PHONE_NUMBER: self.phone_number}
            fail = WrongPassOrPhoneNumber(status=404, message=MessagesKeys.OLD_PASSWORD_IS_NOT_VALID,
                                          params=params)
            return False, fail

        return find_result

    def create_success_message(self, message):
        return SuccessForgetPass(status=200, message=message, params=None)
