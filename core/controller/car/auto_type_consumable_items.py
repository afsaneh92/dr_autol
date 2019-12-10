import logging

from core.controller import BaseController
from core.messages.translator.messages_keys import MessagesKeys
from core.result.failure.faile_to_find_list import FailToFindList
from core.result.failure.list_is_empty import EmptyList
from core.result.success.success_auto_type_consumable_items import SuccessListAutoTypesConsumableItems
from persistence.database.entity.auto_types_products import AutoTypeProduct

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ListAutoTypeConsumableItemsController(BaseController):
    def __init__(self, req_info, converter):
        self.converter = converter
        self.auto_type_id = req_info.auto_type_id
        self.service_type_id = req_info.service_type_id

    def execute(self):
        error_free, result_find_all_proper_consumable_items = self._find_all_consumable_items()
        if not error_free:
            dct = result_find_all_proper_consumable_items.dictionary_creator()
            return self.serialize(dct, converter=self.converter)
        dct = result_find_all_proper_consumable_items.dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    def _find_all_consumable_items(self):
        needed_items = AutoTypeProduct.find_all_proper_consumable_items(self.auto_type_id, self.service_type_id)
        if needed_items[0]:
            consumable_items = set()
            if needed_items[1] != []:
                for result in needed_items[1]:
                    consumable_items.add(result)
                success = SuccessListAutoTypesConsumableItems(status=200, message=MessagesKeys.SUCCESS_LIST,
                                                              params=consumable_items)
                res = True, success

            else:
                fail = EmptyList(status=404, message=MessagesKeys.FAIL_LIST,
                                 params=None)
                res = False, fail
        else:
            fail = FailToFindList(status=500, message=MessagesKeys.FAIL_LIST,
                                  params=None)
            return False, fail

        return res
