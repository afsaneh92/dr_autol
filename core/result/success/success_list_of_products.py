from core.messages.keys import Keys
from core.result import Result


class ListOfSupplierProducts(Result):
    def dictionary_creator(self):
        params = []
        total_price = 0
        total_num = 0

        for product in self.params:
            for order_item in product.order_items:
                dct = {
                    Keys.SUPPLIER_ID: order_item.product.supplier_id,
                    Keys.CODE: order_item.product.code,
                    Keys.SUB_CATEGORY_ID: order_item.product.sub_category_id,
                    Keys.COMPANY_ID: order_item.product.company_id,
                    Keys.BRAND_ID: order_item.product.brand_id,
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

# params = []
# cost = []
# number_of_a_product = []
# product_accepted = 0
#
# for product in self.params:
#     cost.append(product.price)
#
# for item in self.params:
#     for items in item.order_items:
#         if isinstance(items.accepted_number, int):
#             number_of_a_product.append(items.accepted_number)
#         else:
#             number_of_a_product.append(0)
#
# for products in number_of_a_product:
#     product_accepted = product_accepted + products
#
# price = cost[0] * product_accepted
#
# for item in self.params:
#     dct = {
#         Keys.SUPPLIER_ID: item.supplier_id,
#         Keys.CODE: item.code,
#         Keys.SUB_CATEGORY_ID: item.sub_category_id,
#         Keys.COMPANY_ID: item.company_id,
#         Keys.BRAND_ID: item.brand_id,
#         Keys.PRICE: item.pric
#
#     }
#     params.append(dct)
#     params.append({Keys.TOTAL_COST: float(price)})
#     params.append({Keys.TOTAL_SALES: product_accepted})
#
#     return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.FOUND_LIST, Keys.PARAMS: params}

#
# params = []
# cost = []
# number_of_a_product = []
# product_accepted = 0
# order = []
#
# for product in self.params:
#     for order_item in product.order_items:
#         dct2 = {
#             Keys.ORDER_ITEMS_ID: order_item.id,
#             Keys.ACCEPTED_NUMBER: order_item.accepted_number,
#             Keys.PRICE: order_item.product.price,
#
#         }
#         order.append(dct2)
#         dct1 = {
#             Keys.SUPPLIER_ID: product.supplier_id,
#             Keys.CODE: product.code,
#             Keys.SUB_CATEGORY_ID: product.sub_category_id,
#             Keys.COMPANY_ID: product.company_id,
#
#             Keys.BRAND_ID: product.brand_id,
#             Keys.ORDER_ITEMS: order}
#
#         params.append(dct1)
#
# info = set()
# for result in params:
#     info.add(result)
#
# return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.FOUND_LIST, Keys.PARAMS: info}
