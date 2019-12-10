from abc import abstractmethod
from sqlite3 import IntegrityError

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.associationproxy import association_proxy
from werkzeug.routing import ValidationError

from app import db
from core.controller.admin_registration import logger
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result.failure.product_deleted import SuccessDeleteProduct
from core.result.success.add_new_product import SuccessAddNewProduct
from core.result.success.success_update import SuccessUpdate
from core.validation.helpers import db_error_message
from persistence.database.entity.base import BaseMixin


class Product(BaseMixin, db.Model):
    __tablename__ = 'products'
    company_id = db.Column(db.Integer,db.ForeignKey('companies.id'), nullable=False)
    company = db.relationship('Company')
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=False)
    brands = db.relationship('Brand')
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    code = db.Column(db.String(300), nullable=False)
    price = db.Column(db.NUMERIC, nullable=False)
    sub_category_id = db.Column(db.Integer, db.ForeignKey('sub_categories.id'))
    sub_categories = db.relationship('SubCategory')
    minimum_order = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(300), nullable=True)
    deleted = db.Column(db.Boolean, default=False)


    # company description nadare
    def __repr__(self):
        return '<Product %r>' % self.id

    @staticmethod
    def is_added_before(code, supplier_id):
        result = None
        try:
            result = Product.query.filter(Product.code == code).filter(Product.supplier_id == supplier_id).first()
        except:
            result = db_error_message(logger, message='InvalidRequestError')
        return result

    @staticmethod
    @abstractmethod
    def update_by_id(id, db_connection, data):
        result = None
        try:
            Product.query.filter_by(id=id).update(data)
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

    def add(self, db_connection):
        result = None
        try:
            print(self)
            db_connection.session.add(self)
            db_connection.session.commit()
            params = {Keys.SUB_CATEGORY_ID: self.sub_category_id,
                      Keys.CODE: self.code,
                      Keys.BRAND_ID: self.brand_id,
                      Keys.COMPANY_ID: self.company_id
                , Keys.SUPPLIER_ID: self.supplier_id
                      }
            success = SuccessAddNewProduct(status=200, message=MessagesKeys.SUCCESS_ADD_NEW_PRODUCT,
                                           params=params)
            result = True, success

        except IntegrityError as e:
            ValidationError('Integrity error: {}'.format(e.args[0]))
        except:
            db_connection.session.rollback()
            result = db_error_message(logger)

        return result

    @staticmethod
    def find(limit=1, **kwargs):
        res = None
        try:
            res = True, Product.query.filter_by(**kwargs).limit(limit).all()
        except:
            res = db_error_message(logger, message='InvalidRequestError')
        return res

    @staticmethod
    def delete_by_id(db_connection, product_id):
        result = None
        db_connection.session.begin(subtransactions=True)
        try:
            Product.query.filter_by(id=product_id).update({"deleted": True})

            product = Product.find(1, id=product_id)[1][0]
            logger.info('Delete product. Product id: %s', product_id)
            db_connection.session.commit()
            params = {"product_id": product.id, "supplier_id": product.supplier_id}
            success = SuccessDeleteProduct(status=200, message=MessagesKeys.SUCCESS_DELETE_PRODUCT, params=params)
            result = True, success
            db_connection.session.commit()
        except:
            db_connection.session.rollback()
            result = db_error_message(logger)

        return result

    @staticmethod
    def find_all_product_one_supplier_add(supplier_id):
        try:
            return Product.query.filter(Product.supplier_id == supplier_id) \
                .all()
        except:
            return db_error_message(logger)
