from core.messages.keys import Keys
from core.result import Result


class SuccessProductSearchListDetails(Result):
    def dictionary_creator(self):
        params = []
        total_price = 0
        total_num = 0

        for product in self.params:
            for order_item in product.order_items:
                dct = {
                    Keys.SUPPLIER_ID: order_item.product.supplier_id,
                    Keys.CODE: order_item.product.code,
                    Keys.SUB_CATEGORY_NAME: order_item.product.sub_categories.name,
                    Keys.COMPANY_NAME: order_item.product.company.name,
                    Keys.BRAND_NAME: order_item.product.brands.name,
                    Keys.ORDER_ITEMS_ID: order_item.id,
                    Keys.ACCEPTED_NUMBER: order_item.accepted_number,
                    Keys.PRICE: float(order_item.product.price),
                    Keys.TOTAL_COST_EACH_ORDER: float(order_item.accepted_number * order_item.product.price)
                }
                params.append(dct)
        for info in params:
            total_price = total_price + info[Keys.TOTAL_COST_EACH_ORDER]
            total_num = total_num + info[Keys.ACCEPTED_NUMBER]
        params.append({Keys.TOTAL_SALES: float(total_price),
                       Keys.SUPPLIER_ID: info[Keys.SUPPLIER_ID],
                       Keys.TOTAL_NUM: total_num

                       })

        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.FOUND_LIST, Keys.PARAMS: params}
