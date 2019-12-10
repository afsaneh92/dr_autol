import logging

from app import db
from core.controller import BaseController
from core.messages.keys import Keys
from core.result.failure.registered_before import RegisteredBefore
from core.messages.translator.messages_keys import MessagesKeys
from core.services.channel import CodeValidationChannel, SMSCodeValidation
from persistence.database.entity.user.admin import Admin

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class AdminRegistrationController(BaseController):

    def __init__(self, admin, converter):
        self.admin = admin
        self._random_code = CodeValidationChannel.create_random_code()
        self.converter = converter

    def execute(self):
        result = self._add_new_admin_record()
        if not result[0]:
            dct = result[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        code_valid_result = self._send_validation_code()
        if not code_valid_result[0]:
            logger.warning('code has not been send to user:' + self.admin.phone_number, exc_info=True)

        dct = result[1].dictionary_creator()

        return self.serialize(dct, converter=self.converter)

    def _add_new_admin_record(self):
        result = True,
        admin = Admin(name=self.admin.name, last_name=self.admin.last_name,
                              phone_number=self.admin.phone_number, password=self.admin.password)

        if admin.is_registered():
            if admin.is_valid():
                params = {Keys.NAME: self.admin.name}
                registered_before = RegisteredBefore(status=404, message=MessagesKeys.REGISTERED_BEFORE, params=params)
                return False, registered_before
            elif admin.is_invalid():
                dct = {"code": str(self._random_code)}
                result = admin.update(db, dct)
        else:
            admin.code = str(self._random_code)
            result = admin.add(db)

        db.session.close()
        return result

    def _send_validation_code(self):
        sms = SMSCodeValidation(self.admin.name, self.admin.phone_number, self._random_code)
        result = sms.send_validation_code()
        return result
