#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db, global_logger
from core.validation.helpers import db_error_message
from persistence.database.entity.base import BaseMixin
from sqlalchemy.orm import relationship

logger = global_logger


class Payment(BaseMixin, db.Model):
    __tablename__ = 'payments'
    payment_type_id = db.Column(db.Integer, db.ForeignKey('payment_types.id'), nullable=False)
    amount = db.Column(db.Numeric, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    transaction_number = db.Column(db.String(30), nullable=True)
    job = relationship("Job", uselist=False, back_populates="payment")

    type = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'Payment',
        'polymorphic_on': type
    }

    def __repr__(self):
        return '<Payments %r>' % self.id

    @staticmethod
    def find_status(status_name):
        result = True,
        try:
            status = Payment.query.filter(Payment.name == status_name).first()
            result = True, status
        except:
            db.session.rollback()
            result = db_error_message(logger)
        return result
