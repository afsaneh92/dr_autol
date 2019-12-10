from app import db
from core.controller import BaseController
from core.result.failure.false_code_validation import FalseCodeValidation
from core.result.failure.validated_before import ValidatedBefore
from core.result.success.success_validtion import SuccessValidation
from persistence.database.entity.user.user import User


class CodeValidationController(BaseController):

    def __init__(self, code, converter):
        self.code = code
        self.converter = converter

    def execute(self):

        result = self._is_registered_before()
        if not result[0]:
            dct = result[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        is_validate_before = self._is_validated_before(result[1])
        if is_validate_before[0]:
            dct = is_validate_before[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        result = self._update_user(result[1])

        if not result[0]:
            dct = result[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        dct = result[1].dictionary_creator()

        return self.serialize(dct, converter=self.converter)

    def _is_registered_before(self):
        find_results = User.find(code=self.code.code, phone_number=self.code.phone_number)
        if not find_results[0]:
            return find_results

        if len(find_results[1]) == 0:
            false_code = FalseCodeValidation(status=404,
                                             message="karbari ba shomatreye" + self.code.phone_number + " va code " +
                                                     self.code.code + " not registered",
                                             params=None)
            return False, false_code

        return find_results

    def _is_validated_before(self, user):
        if user[0].validate:
            validated_before = ValidatedBefore(status=400, message="ghablan valid shodi jigar", params=None)
            return True, validated_before
        return False,

    def _update_user(self, user):
        data = {"validate": True}
        result = user[0].update(db, data)
        if result[0]:
            params = {'id': result[1].params["user_id"]}
            success = SuccessValidation(status=200, message="%s aziz, mamnon.s" % self.code.phone_number, params=params)
            return True, success
        return result
