#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy.ext.associationproxy import association_proxy

from app import db, global_logger
from core.validation.helpers import db_error_message
from persistence.database.entity.base import BaseMixin

logger = global_logger


class Company(BaseMixin, db.Model):
    __tablename__ = 'companies'
    name = db.Column(db.String(50), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    brands = association_proxy('companies', 'brands')
    products = db.relationship('Product')

    # name = db.Column(db.String(20), nullable=False)
    # phone_number = db.Column(db.String(11), unique=True, nullable=False)
    # validate = db.Column(db.Boolean, default=False)
    # password = db.Column(db.String(300), nullable=False)
    # code = db.Column(db.String(4), nullable=True)
    # reg_id = db.Column(db.String(200), nullable=True)

    type = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'Company',
        'polymorphic_on': type
    }

    def __repr__(self):
        return '<Company %r>' % self.id

    @staticmethod
    def find(limit=1, **kwargs):
        res = None
        try:
            res = True, Company.query.filter_by(**kwargs).limit(limit).all()
        except:
            res = db_error_message(logger, message='InvalidRequestError')
        return res
