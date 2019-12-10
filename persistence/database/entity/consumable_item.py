"""
Many to many of service_grades and service_types
"""

from sqlalchemy import UniqueConstraint

from app import db
from persistence.database.entity.base import BaseMixin


class ConsumableItem(BaseMixin, db.Model):
    __tablename__ = 'consumable_items'
    brand_name = db.Column(db.String(64), nullable=False)
    product_name = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    service_type_id = db.Column(db.Integer, db.ForeignKey('service_types.id'))
    # product_type_id = db.Column(db.Integer, db.ForeignKey('brand_usages.id'), nullable=False)
    # product_type = db.relationship("BrandUsage")

    __table_args__ = (UniqueConstraint('brand_name', 'product_name', name='unique_brand_with_product'),)

    def __init__(self, brand_name, product_name, price):
        self.brand_name = brand_name
        self.product_name = product_name
        self.price = price

    def __repr__(self):
        return 'ConsumableItem(%s)' % repr(self.brand_name) + " " +  repr(self.product_name)
