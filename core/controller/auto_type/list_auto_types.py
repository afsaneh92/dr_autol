import logging
from core.controller import BaseController
from core.messages.translator.messages_keys import MessagesKeys
from core.result import Result
from core.result.failure.auto_id_dosnt_exist import AutoIdDoseNotExist
from core.result.failure.faile_to_find_list import FailToFindList
from core.result.success.success_list_auto_types import SuccessListAutoTypes
from persistence.database.entity.auto_type import AutoType

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ListAutoTypesController(BaseController):
    def __init__(self, converter):
        self.converter = converter

    def execute(self):
        result_find_all = self._find_all()
        if not result_find_all[0]:
            dct = result_find_all[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        dct = result_find_all[1].dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    def _find_all(self):
        models = AutoType.find_all_models_of_a_type()
        if models[0]:
            if models[1] == [] or models is None:
                return False, AutoIdDoseNotExist(
                    status=404, message=Result.language.AUTO_ID_DOES_NOT_EXIST, params=None)
            else:
                return True, SuccessListAutoTypes(status=200, message=MessagesKeys.SUCCESS_LIST, params=models[1])
        else:
            return False, FailToFindList(status=500, message=MessagesKeys.FAIL_LIST, params=None)
