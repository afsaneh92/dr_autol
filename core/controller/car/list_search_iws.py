from app import global_logger
from core.controller import BaseController
from core.messages.translator.messages_keys import MessagesKeys
from core.result.success.success_list_search_iws import IWSSearchResult
from persistence.database.query.search_business_owner import SearchBusinessOwner

logger = global_logger


class ListSearchIWSController(BaseController):

    def __init__(self, iws_search_parameter, converter):
        self.search_parameter = iws_search_parameter
        self.converter = converter

    def execute(self):
        result_find_all = self._find_all()
        if not result_find_all[0]:
            dct = result_find_all[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        sorted_result = self.sort_iws(result_find_all[1])
        dct = sorted_result.dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    def _find_all(self):
        find_result = SearchBusinessOwner.query_iws(self.search_parameter)
        if not find_result[0]:
            return find_result

        list_result = find_result[1]
        params = []
        for result in list_result:
            dct = {"id": result.id, "name": result.name, "address": result.address,
                   'workplaceName': result.workspace_name, 'imageAddress': result.uuid + "/profile-pic",
                   'phone': result.phone_number_workspace}
            params.append(dct)

        return True, IWSSearchResult(status=200, message=MessagesKeys.IWS_SEARCH_LIST, params=params)

    def sort_iws(self, iws):
        # TODO, we need a sorted method.
        return iws
