from core.messages.keys import Keys
from core.result import Result


class JobAndCarOwnerNotMatch(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.JOB_AND_CAR_OWNER_ARE_NOT_MATCH,
                Keys.PARAMS: None}
