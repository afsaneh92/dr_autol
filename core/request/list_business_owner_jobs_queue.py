import logging

from core.result import Result
from persistence.database.entity.business_owner import BusinessOwners

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class JobsQueueListRequest:

    def __init__(self, business_owner_id):
        self.business_owner = BusinessOwners(id=business_owner_id)

    def validate_pattern(self):
        res = self._id_checker(self.business_owner.id)
        if not res[0]:
            return res

        return True,

    def _id_checker(self, id):
        try:
            int(id)
            return True,
        except:
            return False, Result.language.SHOULD_BE_INT

    @staticmethod
    def pre_deserialize(json_dict):
        pass

    def post_deserialize(self):
        return self.validate_pattern()

    def deserialize(self):
        result_pattern = self.post_deserialize()
        if not result_pattern[0]:
            return result_pattern
        return True, self.business_owner
