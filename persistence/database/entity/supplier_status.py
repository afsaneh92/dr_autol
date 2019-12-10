from sqlalchemy.exc import InvalidRequestError

from app import db
from core.controller.admin_registration import logger
from core.messages.keys import Keys
from core.validation.helpers import db_error_message
from persistence.database.entity.base import BaseMixin


class SupplierStatus(db.Model, BaseMixin):
    __tablename__ = 'supplier_statuses'
    name = db.Column(db.String(300), nullable=False)
    order_items = db.relationship("OrderItem", back_populates="supplier_statuses")

    @staticmethod
    def find_status_id(status_name):
        try:
            return True, SupplierStatus.query.filter(SupplierStatus.name == status_name).\
                with_entities(SupplierStatus.id).first()
        except:
            return db_error_message(logger)

