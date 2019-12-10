from core.messages.keys import Keys
from core.result import Result


class SuccessAddNewProduct(Result):
    def dictionary_creator(self):
        # params = []
        # for param in self.params:
        #     dct = {Keys.PRODUCT_NAME: param[Keys.PRODUCT_NAME],
        #            Keys.CODE: param[Keys.CODE],
        #            Keys.BRAND_ID: param[Keys.BRAND_ID],
        #            Keys.COMPANY_ID: param[Keys.COMPANY_ID]
        #            }
        #     params.append(dct)
        return {"status": 200, "message": Result.language.SUCCESS_ADD_NEW_CAR, "params": self.params}
