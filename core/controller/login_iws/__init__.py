from passlib.hash import pbkdf2_sha256

from app import db, global_logger
from core.controller import BaseController
from core.messages.keys import Keys
from core.result.failure.wrong_pass_or_phone_number import WrongPassOrPhoneNumber
from core.result.success.success_login import SuccessLogin
from persistence.database.entity.user.user import User

logger = global_logger


class IwsLoginController(BaseController):
    def __init__(self, login, converter):
        self.login = login
        self.converter = converter

    def execute(self):
        authentication_result = self._authentication()
        if not authentication_result[0]:
            dct_result = authentication_result[1].dictionary_creator()
            return self.serialize(dct_result, converter=self.converter)

        update_reg_id_result = self._update_reg_id()
        if not update_reg_id_result[0]:
            dct_result = update_reg_id_result[1].dictionary_creator()
            return self.serialize(dct_result, converter=self.converter)

        authentication_iws = authentication_result[1]
        self.add_new_key_to_session(Keys.PHONE_NUMBER, self.login.phone_number)
        self.add_new_key_to_session(Keys.USER_ID, authentication_iws.id)
        params = dict(name=authentication_iws.name, id=authentication_iws.id)
        success_login = SuccessLogin(status=200, message="Successed", params=params)
        dct_result = success_login.dictionary_creator()
        return self.serialize(dct_result, converter=self.converter)

    def _authentication(self):
        find_result = User.find(phone_number=self.login.phone_number, validate=True)
        if not find_result[0]:
            return find_result

        if len(find_result[1]) == 0:
            params = {"phone_number": self.login.phone_number}
            fail = WrongPassOrPhoneNumber(status=404, message="wrong", params=params)
            return False, fail

        verified_pass = pbkdf2_sha256.verify(self.login.password, find_result[1][0].password)
        if not verified_pass:
            params = {"phone_number": self.login.phone_number}
            fail = WrongPassOrPhoneNumber(status=404, message="wrong", params=params)
            return False, fail

        return True, find_result[1][0]

    def _update_reg_id(self):
        return User.update_reg_id(self.login.phone_number, self.login.reg_id, db)
