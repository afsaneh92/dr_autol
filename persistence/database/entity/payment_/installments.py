#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db, global_logger
from persistence.database.entity.base import BaseMixin
from sqlalchemy.orm import relationship

logger = global_logger


class Installment(BaseMixin, db.Model):
    __tablename__ = 'installments'
    installment_id = db.Column(db.Integer, db.ForeignKey('install_payments.id'), nullable=False)
    amount = db.Column(db.Numeric, nullable=False)
    pay_date = db.Column(db.DateTime, nullable= False)


    def __repr__(self):
        return '<Installment %r>' % self.id