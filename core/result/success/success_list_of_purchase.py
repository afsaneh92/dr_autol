from core.messages.keys import Keys
from core.result import Result
from persistence.database.entity.brand import Brand
from persistence.database.entity.sub_category import SubCategory


class SuccessSupplierDailyPurchaseList(Result):
    def dictionary_creator(self):
        purchase = []
        for list_item in self.params:
            dic = {}
            dic['productId'] = list_item.product_id
            dic['number'] = list_item.requested_number
            dic['price'] = str(list_item.product.price)
            dic['autoServiceId'] = list_item.auto_service_id
            dic['orderId'] = list_item.order_id
            dic['code'] = list_item.product.code
            name = Brand.query.filter(Brand.id == list_item.product.brand_id). \
                with_entities(Brand.name).first()
            dic['name'] = name

            result = SubCategory.category_id(list_item.product.sub_category_id)
            if len(result == 0):
                pass
            dic['name'] = result[1].name
            dic['company'] = result[1].company

            purchase.append(dic)

        return {Keys.STATUS: 200, Keys.MESSAGE: Result.language.SUCCESS_LIST, Keys.PARAMS: purchase}
