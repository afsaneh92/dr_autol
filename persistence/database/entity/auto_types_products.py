from sqlalchemy.orm import relationship
from app import db, global_logger
# from persistence.database.entity.auto_type import AutoType
from core.validation.helpers import db_error_message
from persistence.database.entity.base import BaseMixin
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, UniqueConstraint, Numeric

from persistence.database.entity.consumable_item import ConsumableItem

logger = global_logger


class AutoTypeProduct(BaseMixin, db.Model):
    __tablename__ = 'auto_types_products'
    auto_type_id = db.Column(db.Integer, db.ForeignKey('auto_types.id'))
    consumable_item_id = db.Column(db.Integer, db.ForeignKey('consumable_items.id'))
    auto_type = db.relationship("AutoType", backref="auto_type_consumable_items")
    consumable_item = db.relationship("ConsumableItem")

    def __init__(self, consumable_item=None, auto_type=None):
        self.consumable_item = consumable_item
        self.auto_type = auto_type

    @staticmethod
    def find_all_proper_consumable_items(auto_type_id, service_type_id):
        try:
            consumable_item_id = AutoTypeProduct.query.filter(AutoTypeProduct.auto_type_id == auto_type_id). \
                with_entities(AutoTypeProduct.consumable_item_id).all()

            needed_items = ConsumableItem.query.filter(ConsumableItem.id.in_(consumable_item_id)). \
                filter(ConsumableItem.service_type_id == service_type_id).all()

            return True, needed_items

        except:
            return db_error_message(logger)
