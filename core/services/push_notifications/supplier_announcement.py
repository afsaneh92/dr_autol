from core.messages.keys import Keys
from core.result import Result
from core.services.push_notifications.new_request import PushNotification
from persistence.database.entity.user.supplier import Supplier
from persistence.database.entity.user.user import User


class SupplierAnnouncement(object):

    @staticmethod
    def accept_order(supplier):
        supplier = User.find(id=supplier.id)
        info = {
            Keys.USER_TYPE: Keys.ACCEPT_ORDER_REQUEST,
            Keys.SUPPLIER: {Keys.NAME: User.name, Keys.REG_ID: User.reg_id},
            Keys.MESSAGE: Result.language.ACCEPT_ORDER_BY_SUPPLIER,
        }

        response = PushNotification.push(info[Keys.SUPPLIER][Keys.REG_ID], info)
        return response

    @staticmethod
    def deny_order(supplier):
        supplier = User.find(id=supplier.id)
        info = {
            Keys.USER_TYPE: Keys.DENY_ORDER_REQUEST,
            Keys.SUPPLIER: {Keys.NAME: User.name, Keys.REG_ID: User.reg_id},
            Keys.MESSAGE: Result.language.DENY_ORDER_BY_SUPPLIER,
        }
        response = PushNotification.push(info[Keys.SUPPLIER][Keys.REG_ID], info)
        return response

