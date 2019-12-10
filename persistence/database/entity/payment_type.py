import logging

from core.validation.helpers import db_error_message
from persistence.database.entity.base import BaseMixin, db
from persistence.database.entity.payment_.payment import Payment

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class PaymentType(BaseMixin, db.Model):
    __tablename__ = 'payment_types'
    name = db.Column(db.String(200), nullable=False)
    payments = db.relationship("Payment", backref="payments_list", lazy='dynamic',
                               primaryjoin=lambda: PaymentType.id == Payment.payment_type_id)

    def __repr__(self):
        return '<PaymentType %r>' % self.id

    @staticmethod
    def find_payment_type_by_id(type_id):
        try:
            result = True, PaymentType.query.filter(PaymentType.id == type_id).first()
        except:
            result = db_error_message(logger)
        return result
