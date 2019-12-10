from core.messages.keys import Keys
from core.result import Result


class SuccessListOfUnfinishedJob(Result):
    def dictionary_creator(self):
        params = []
        for param in self.params:
            dct = {Keys.ID: param.id, Keys.NAME: param.name, Keys.PHONE_NUMBER: param.phone_number,
                   Keys.CAR_INFO: param.plate_number

                   }
            params.append(dct)
        return {Keys.STATUS: 200, Keys.MESSAGE: Result.language.SUCCESS_LIST, Keys.PARAMS: params}