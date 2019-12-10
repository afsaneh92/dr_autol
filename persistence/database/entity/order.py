from app import db
from persistence.database.entity.base import BaseMixin


class Order(BaseMixin, db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, nullable=True)
    pre_invoice_id = db.Column(db.Integer, nullable=False)
    order_items = db.relationship("OrderItem")

    def __repr__(self):
        return '<Order %r>' % self.id
