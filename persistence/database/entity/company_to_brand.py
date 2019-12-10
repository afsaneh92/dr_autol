from app import db
from core.controller.admin_registration import logger
from core.validation.helpers import db_error_message
from persistence.database.entity.base import BaseMixin
from persistence.database.entity.brand import Brand
from persistence.database.entity.comany.comapny import Company


class CompanyToBrand(BaseMixin, db.Model):
    __tablename__ = 'company_to_brand'
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), primary_key=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), primary_key=True)
    company = db.relationship(Company, backref='company_to_brand')
    brand = db.relationship(Brand)

    @staticmethod
    def find(limit=1, **kwargs):
        res = None
        try:
            res = True, CompanyToBrand.query.filter_by(**kwargs).limit(limit).all()
        except:
            res = db_error_message(logger, message='InvalidRequestError')
        return res

    @staticmethod
    def is_brand_and_company_match(company_id, brand_id):
        result = None
        try:
            result = True, CompanyToBrand.query.filter(CompanyToBrand.company_id == company_id). \
                filter(CompanyToBrand.brand_id == brand_id).first()
        except:
            result = db_error_message(logger, message='InvalidRequestError')
        return result
