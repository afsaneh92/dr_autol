#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import abstractmethod

from sqlalchemy.exc import InvalidRequestError

from app import db, global_logger
from core.messages.translator.messages_keys import MessagesKeys
from core.result.success.success_list_of_payable_job import SuccessListOfPayableJob
from core.result.success.success_list_of_purchase import SuccessSupplierDailyPurchaseList
from core.result.success.success_update import SuccessUpdate
from core.validation.helpers import db_error_message
from persistence.database.entity.brand import Brand
from persistence.database.entity.comany.comapny import Company
from persistence.database.entity.order_items import OrderItem
from persistence.database.entity.product import Product
from persistence.database.entity.sub_category import SubCategory
from persistence.database.entity.order_items import OrderItem
from persistence.database.entity.user.user import User

logger = global_logger


class Supplier(User):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    business_license = db.Column(db.String(300), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    products = db.relationship('Product')

    # product = association_proxy('supplier', 'product')
    __mapper_args__ = {
        'polymorphic_identity': 'Supplier',
    }

    def __repr__(self):
        return '<Supplier %r>' % self.id

    @staticmethod
    @abstractmethod
    def update_by_id(id, db_connection, data):
        result = None
        try:
            User.query.filter_by(id=id).update(data)
            db_connection.session.commit()
            logger.info('update user. ID: %s' % id)
            params = {"user_id": id}
            success = SuccessUpdate(status=200, message=MessagesKeys.SUCCESS_UPDATE, params=params)
            # raise Exception()
            result = True, success

        except InvalidRequestError as error:
            result = db_error_message(logger)
            db_connection.session.rollback()

        except:
            result = db_error_message(logger)
            db_connection.session.rollback()
        return result

    @staticmethod
    def check_supplier(phone_number):
        result = None
        try:
            supplier_id = Supplier.query.filter(Supplier.phone_number == phone_number).with_entities(
                Supplier.id).first()
            result = True, supplier_id[0]
        except:
            result = db_error_message(logger)
            db.session.rollback()
        return result

    @staticmethod
    def find(limit=1, **kwargs):
        res = None
        try:
            res = True, Supplier.query.filter_by(**kwargs).limit(limit).all()
        except:
            res = db_error_message(logger)
            db.session.rollback()
        return res

    @staticmethod
    def check_id_and_phone_number_match(product_id, phone_number):
        result = None
        try:
            supplier_id = Product.query.filter(Product.id == product_id).with_entities(
                Product.supplier_id).first()
            selected_supplier = Supplier.query. \
                filter(Supplier.phone_number == phone_number). \
                filter(Supplier.id.in_(supplier_id)).with_entities(Supplier.id).first()
            result = True, selected_supplier
        except:
            result = db_error_message(logger)
            db.session.rollback()
        return result

    @staticmethod
    def query_builder(search_parameter):
        query = db.session.query(Product) \
            .join(Company, Product.company_id == Company.id) \
            .join(Brand, Product.brand_id == Brand.id) \
            .join(Supplier, Supplier.id == Product.supplier_id) \
            .join(SubCategory, SubCategory.id == Product.sub_category_id) \
            .join(OrderItem, OrderItem.product_id == Product.id)
        if search_parameter.brand_id is not None:
            query = query.filter(Brand.id == search_parameter.brand_id)
        if search_parameter.company_id is not None:
            query = query.filter(search_parameter.company_id == Company.id)
        if search_parameter.sub_category_id is not None:
            query = query.filter(search_parameter.sub_category_id == SubCategory.id)
        if search_parameter.supplier_id is not None:
            query = query.filter(search_parameter.supplier_id == Supplier.id)
        if len(search_parameter.code) > 0:
            query = query.filter(search_parameter.code == Product.code)
        if search_parameter.max_price is not None:
            query = query.filter(Product.price <= search_parameter.max_price)
        if search_parameter.min_price is not None:
            query = query.filter(search_parameter.min_price <= Product.price)
        # if search_parameter.max_price is not None:
        #     if search_parameter.min_price is not None:
        #         query = query.filter(search_parameter.min_price <= Product.price <= search_parameter.max_price)
        if search_parameter.minimum_order is not None:
            query = query.filter(Product.minimum_order <= search_parameter.minimum_order)
        if search_parameter.requested_number is not None:
            query = query.filter(OrderItem.requested_number == search_parameter.requested_number)
        if search_parameter.accepted_number is not None:
            query = query.filter(OrderItem.accepted_number == search_parameter.accepted_number)
        if search_parameter.supplier_status_id is not None:
            query = query.filter(OrderItem.supplier_status_id == search_parameter.supplier_status_id)

        return query

    @staticmethod
    def search_on_products(search_parameter):
        query = Supplier.query_builder(search_parameter)
        try:
            products = query.all()
            ids = set()
            for product in products:
                ids.add(product.id)
            search_results = Product.query.filter(Product.id.in_(ids)).all()
            result = True, search_results
        except:
            result = db_error_message(logger)

        return result

