import logging
from sqlalchemy.orm import relationship
from core.validation.helpers import db_error_message
from persistence.database.entity.base import BaseMixin, db

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Payments(BaseMixin, db.Model):
    __tablename__ = 'paymentss'
    payment_type_id = db.Column(db.Integer, db.ForeignKey('payment_types.id'), nullable=False)
    amount = db.Column(db.Numeric, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    transaction_number = db.Column(db.String(30), nullable=True)
    # job = relationship("Jobs", uselist=False, back_populates="payment")

    def __repr__(self):
        return '<Payment %r>' % self.id

    #TODO delete
    def add(self, db_connection, payment):
        result = None
        try:
            db_connection.session.begin(subtransactions=True)
            db_connection.session.add(payment)
            db_connection.session.commit()
            logger.info('Add new payment. Payment id: %s', payment.id)
            params = {"payment": payment}
            result = True, params
        except:
            db_connection.session.rollback()
            result = db_error_message(logger)

        return result

