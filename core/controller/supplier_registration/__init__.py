from app import db, global_logger
from core.controller import BaseController
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result.failure.registered_before import RegisteredBefore
from core.services.channel import CodeValidationChannel, SMSCodeValidation
from persistence.database.entity.user.auto_service import AutoServiceBusinessOwner
from persistence.database.entity.user.supplier import Supplier

logger = global_logger


class SupplierRegistrationController(BaseController):

    def __init__(self, result, converter):
        self.supplier = result.supplier
        self._random_code = CodeValidationChannel.create_random_code()
        self.converter = converter

    def execute(self):
        result = self._add_new_supplier_record()
        if not result[0]:
            return result[1]

        code_valid_result = self._send_validation_code()
        if not code_valid_result[0]:
            logger.warning('code has not been send to supplier:' + self.supplier.phone_number, exc_info=True)
        dct = result[1].dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    def _add_new_supplier_record(self):
        result = True,
        user = self.supplier
        self.phone_number = user.phone_number
        if user.is_registered():
            if user.is_valid():
                params = {Keys.NAME: user.name}
                print params
                registered_before = RegisteredBefore(status=404, message=MessagesKeys.REGISTERED_BEFORE, params=params)
                dct = registered_before.dictionary_creator()
                return False, self.serialize(dct, converter=self.converter)

            elif user.is_invalid():
                dct = {Keys.CODE: str(self._random_code)}
                result = user.update(db, dct)
        else:
            user.code = str(self._random_code)
            result = user.add(db)

        db.session.close()
        return result

    def _send_validation_code(self):
        sms = SMSCodeValidation(self.supplier.name, self.supplier.phone_number, self._random_code)
        result = sms.send_validation_code()
        return result
