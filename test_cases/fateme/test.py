import xlrd


def read_data_from_excel_file():
    wanted_values = []
    open_file = xlrd.open_workbook('./financial_credit.xlsx')
    sheet = open_file.sheet_by_index(0)
    if sheet.ncols != 0 or sheet.nrows != 0 :
        number_of_rows = sheet.ncols
        for value in range(number_of_rows):
            row_value = sheet.row_values(value)
            if '09125200100' in row_value:
                wanted_values.append(row_value)

        return wanted_values
    return None


if __name__ == '__main__':
    print read_data_from_excel_file()

# @staticmethod
# def how_much_a_business_owner_buy_product_in_special_time(business_owner_id, special_time):
#     try:
#         business_owner_order_price_list = []
#         fail_list = []
#         sum_prices = 0
#         time_delta = timedelta(hours=special_time)
#         done_status_id = SupplierStatus.query.filter(SupplierStatus.name == Keys.BUY_DONE). \
#             with_entities(SupplierStatus.id).first()
#         done_order_items = OrderItem.query.filter(OrderItem.supplier_status_id.in_(done_status_id)). \
#             filter(OrderItem.business_owner_id == business_owner_id).all()
#
#
#         for order_item in done_order_items:
#             if order_item.orders.date_modified + time_delta >= datetime.now():
#                 business_owner_order_price_list. \
# append(float(order_item.accepted_number * order_item.product.price))
#             else:
#                 fail_list.append(order_item)
#         if len(fail_list) == len(done_order_items):
#             return False, EmptyList(status=404, message=MessagesKeys.FAIL_LIST, params=None)
#
#         for price in business_owner_order_price_list:
#             sum_prices = sum_prices + price
#
#         res = True, sum_prices
#
#     except:
#         res = db_error_message(logger)
#
#     return res
