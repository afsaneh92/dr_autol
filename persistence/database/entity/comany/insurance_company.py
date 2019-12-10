#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db, global_logger
from persistence.database.entity.base import BaseMixin
from persistence.database.entity.comany.comapny import Company

logger = global_logger


class InsuranceCompany(Company):
    __tablename__ = 'insurance_companies'
    id = db.Column(db.Integer, db.ForeignKey('companies.id'), primary_key=True)
    branches_count = db.Column(db.String(2), nullable=False)

    # payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'))
    # payment = db.relationship("Payment", backref="payment_backref", uselist=False)


    def __repr__(self):
        return '<InsuranceCompany %r>' % self.id