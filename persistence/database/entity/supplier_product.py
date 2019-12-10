from app import global_logger
from persistence.database.entity.base import db
from persistence.database.entity.product import Product
from persistence.database.entity.user.supplier import Supplier

logger = global_logger


# TODO DELETE
class SupplierToProduct(db.Model):
    __tablename__ = 'supplier_to_product'
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), primary_key=True)
    product = db.relationship(Product, backref="product")
    supplier = db.relationship(Supplier, backref="supplier")

    def __init__(self, supplier=None, product=None):
        self.product = product
        self.supplier = supplier

    def __repr__(self):
        return '<SupplierToProduct %r>' % self.product
