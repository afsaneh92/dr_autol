from app import db, global_logger
from core.validation.helpers import db_error_message
from persistence.database.entity.payment_.payment import Payment


class FullPayment(Payment):
    __tablename__ = 'full_payment'
    id = db.Column(db.Integer, db.ForeignKey('payments.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'FullPayment',
    }

    def add(self, db_connection, payment):
        result = None
        try:
            db_connection.session.begin(subtransactions=True)
            db_connection.session.add(payment)
            db_connection.session.commit()
            global_logger.info('Add new payment. Payment id: %s', payment.id)
            params = {"payment": payment}
            result = True, params
        except:
            db_connection.session.rollback()
            result = db_error_message(global_logger)

        return result
