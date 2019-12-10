#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy.exc import InvalidRequestError

from app import db, global_logger
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result.success.success_update import SuccessUpdate
from core.validation.helpers import db_error_message
from persistence.database.entity.base import BaseMixin
from persistence.database.entity.order import Order
from persistence.database.entity.product import Product
from persistence.database.entity.supplier_status import SupplierStatus

logger = global_logger


class OrderItem(BaseMixin, db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship("Product", backref="order_items")
    requested_number = db.Column(db.Integer, default=0)
    accepted_number = db.Column(db.Integer, default=0)
    supplier_status_id = db.Column(db.Integer, db.ForeignKey(SupplierStatus.id), default=4)
    supplier_statuses = db.relationship("SupplierStatus")

    business_owner_id = db.Column(db.Integer, db.ForeignKey('business_owners.id'), nullable=False)
    auto_service_business_owners = db.relationship('AutoServiceBusinessOwner')

    order_id = db.Column(db.Integer, db.ForeignKey(Order.id))
    orders = db.relationship("Order")

    def __repr__(self):
        return '<OrderItem %r>' % self.id

    @staticmethod
    def get_daily_purchase_list_of_supplier(supplier_id):
        try:
            import datetime
            product_id = Product.query.filter(Product.supplier_id == supplier_id). \
                with_entities(Product.id)

            pending_id = SupplierStatus.query.filter(SupplierStatus.name == Keys.PENDING). \
                with_entities(SupplierStatus.id).first()

            today = datetime.datetime.now()
            beginning = datetime.datetime(today.year, today.month, today.day, 0, 0, 0, 0)

            list = OrderItem.query.filter(OrderItem.supplier_status_id.in_(pending_id)). \
                filter(OrderItem.date_created < datetime.datetime.now()). \
                filter(beginning < OrderItem.date_created). \
                filter(OrderItem.product_id.in_(product_id)).all()

            return True, list
        except:
            db_error_message(logger)

    @staticmethod
    def check_business_owner_order_list(business_owner_id):
        try:
            return OrderItem.query.filter(OrderItem.business_owner_id == business_owner_id). \
                filter(OrderItem.accepted_number > 0). \
                all()
        except:
            return db_error_message(logger)

    @staticmethod
    def find_by_id(order_id):
        try:
            return True, OrderItem.query.filter(OrderItem.id == order_id).all()
        except:
            return db_error_message(logger)

    @staticmethod
    def update_by_id(id, db_connection, data):
        result = None
        try:
            OrderItem.query.filter(OrderItem.id == id).update(data)
            db_connection.session.commit()
            logger.info('update question_sets. ID: %s' % id)
            params = {Keys.ID: id}
            success = SuccessUpdate(status=200, message=MessagesKeys.SUCCESS_UPDATE, params=params)
            result = True, success
        except InvalidRequestError as error:
            result = db_error_message(logger)
            db_connection.session.rollback()
        except:
            result = db_error_message(logger)
            db_connection.session.rollback()
        return result