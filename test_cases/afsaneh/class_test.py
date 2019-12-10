from core.interfaces.serialization import Serializable
from core.messages.keys import Keys
from core.request.rate_to_job_request import RateJobRequest
from routers.endpoints import Endpoints


class send_array_items():
    def __init__(self, array):
        self.array = array

    def send_dict_to_endpoint(self):
        for item in self.array:
                item_dict = Serializable.convert_input_to_dict(item)
                res = self.app.post(Endpoints.RATE_BUSINESS_OWNER_BY_CAR_OWNER, data=item_dict,
                                    content_type=Keys.APPLICATION_CONTENT_TYPE_JSON)

    # def get_dict_from_array(self):
    #     if isinstance(self.array, list):
    #         for item in self.array:
    #             if not type(item) is dict:
    #                 item_dict = Serializable.convert_input_to_dict(item)
    #             else:
    #                 item_dict = item
    #             RateJobRequest(item)