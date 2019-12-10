from core.messages.keys import Keys
from core.result import Result


class SuccessListAutoTypesConsumableItems(Result):
    def dictionary_creator(self):
        params = []
        for param in self.params:
            dct = {Keys.PRICE: str(param.price), Keys.PRODUCT_ID: param.product_name,
                   Keys.BRAND_NAME: param.brand_name}
            params.append(dct)
        return {Keys.STATUS: 200, Keys.MESSAGE: Result.language.SUCCESS_LIST, Keys.PARAMS: params}
