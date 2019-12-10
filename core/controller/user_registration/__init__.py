from app import db, global_logger
from core.controller import BaseController
from core.messages.translator.messages_keys import MessagesKeys
from core.result.failure.registered_before import RegisteredBefore
from core.services.channel import CodeValidationChannel, SMSCodeValidation
from persistence.database.entity.user.car_owner import CarOwner

logger = global_logger


class UserRegistrationController(BaseController):

    def __init__(self, user, converter):
        self.user = user
        self._random_code = CodeValidationChannel.create_random_code()
        self.converter = converter

    def execute(self):
        result = self._add_new_user_record()
        if not result[0]:
            dct = result[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        code_valid_result = self._send_validation_code()
        if not code_valid_result[0]:
            logger.warning('code has not been send to user:' + self.user.phone_number, exc_info=True)

        dct = result[1].dictionary_creator()

        return self.serialize(dct, converter=self.converter)

    def _add_new_user_record(self):
        result = True,
        user = CarOwner(name=self.user.name, phone_number=self.user.phone_number, password=self.user.password, reg_id=self.user.reg_id)

        if user.is_registered():
            if user.is_valid():
                params = {"name": self.user.name}
                registered_before = RegisteredBefore(status=404, message=MessagesKeys.REGISTERED_BEFORE, params=params)
                return False, registered_before
            elif user.is_invalid():
                dct = {"code": str(self._random_code)}
                result = user.update(db, dct)
        else:
            user.code = str(self._random_code)
            result = user.add(db)

        db.session.close()
        return result

    def _send_validation_code(self):
        sms = SMSCodeValidation(self.user.name, self.user.phone_number, self._random_code)
        result = sms.send_validation_code()
        return result
