from core.result import Result


class IWSSearchResult(Result):
    def dictionary_creator(self):

        return {"status": self.status, "message": Result.language.IWS_SEARCH_LIST, "params": self.params}
