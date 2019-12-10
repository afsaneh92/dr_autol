from sqlalchemy import Column, String
from sqlalchemy.ext.associationproxy import association_proxy

from app import db, global_logger
from core.messages.translator.messages_keys import MessagesKeys
from core.result.success.success_list_auto_types import SuccessListAutoTypes
from core.validation.helpers import db_error_message
from persistence.database.entity.auto_model import AutoModel
from persistence.database.entity.auto_types_products import AutoTypeProduct
from persistence.database.entity.base import BaseMixin

logger = global_logger


class AutoType(BaseMixin, db.Model):
    __tablename__ = 'auto_types'
    name = Column(String(20), nullable=False)
    engine_power = Column(String(20), nullable=False)
    cars = db.relationship("Car", backref="cars_list", lazy='dynamic', primaryjoin="AutoType.id == Car.auto_type_id")
    consumable_items = association_proxy('auto_type_consumable_items', 'consumable_item',
                                         creator=lambda consumable_item: AutoTypeProduct(
                                             consumable_item=consumable_item))
    auto_models = db.relationship(AutoModel)

    def __repr__(self):
        return '<AutoType %r>' % self.name

    @staticmethod
    def find_all():
        try:
            collection = AutoType.query.add_columns(AutoType.id, AutoType.name).all()

            success = SuccessListAutoTypes(status=200, message=MessagesKeys.SUCCESS_LIST, params=collection)
            res = True, success
        except:
            res = db_error_message(logger)
        return res

    @staticmethod
    def find_all_models_of_a_type():
        try:

            result = AutoType.query. \
                all()
            res = True, result
        except:
            res = False, db_error_message(logger)
        return res

    @staticmethod
    def are_auto_type_and_auto_model_matched(auto_type_id, auto_model_id):
        try:
            res = AutoModel.query.filter(AutoModel.id == auto_model_id). \
                filter(AutoModel.auto_types_id == auto_type_id).first()
            # res = AutoModel.query.filter(AutoModel.id == auto_type_id). \
            #     filter(AutoModel.auto_types_id == auto_model_id).first()
        except:
            res = db_error_message(logger)
        return res
