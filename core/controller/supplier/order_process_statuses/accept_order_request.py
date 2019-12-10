import datetime

from app import db
from core.controller import BaseController
import logging

from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result import Result
from core.result.failure.not_found_order_items import NotFoundOrderItem
from core.result.failure.time_out_of_validity import TimeOutOfValidity
from core.result.success.success_accept_order import SuccessAcceptOrder
from persistence.database.entity.order_items import OrderItem
from persistence.database.entity.supplier_status import SupplierStatus

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class AcceptOrderController(BaseController):

    def __init__(self, order, converter):
        self.order = order
        self.converter = converter

    def execute(self):
        is_valid = self.load_order()
        if not is_valid[0]:
            dct = is_valid[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)
        if not len(is_valid[1]):
            result = True, NotFoundOrderItem(status=404, message=Result.language.NOT_FOUND_ORDER_ITEM, params=None)
            dct = result[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        self.order = is_valid[1][0]
        validate = self._validate_time()
        if not validate[0]:
            dct = validate[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        update_result = self._update_order_item()
        if not update_result[0]:
            dct = update_result[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)
        if update_result[1].message == MessagesKeys.SUCCESS_UPDATE:
            result = True, SuccessAcceptOrder(status=200, message=MessagesKeys.SUCCESS_ACCEPT_ORDER, params=None)

            dct = result[1].dictionary_creator()
            return self.serialize(dct, converter=self.converter)

    def load_order(self):
        return OrderItem.find_by_id(self.order.id)

    def _validate_time(self):
        today = datetime.datetime.now()
        time_out = datetime.datetime(today.year, today.month, today.day, 13, 0, 0, 0)
        if self.order.date_created > time_out:
            return False,  TimeOutOfValidity(status=404, message=MessagesKeys.NOT_VAILID_TIME, params=None)
        return True, self.order.id

    def _update_order_item(self):
        status_id = SupplierStatus.find_status_id(Keys.ACCEPT)
        data = {Keys.SUPPLIER_STATUS_ID: status_id[1]}
        result = OrderItem.update_by_id(self.order.id, db, data)
        return result

