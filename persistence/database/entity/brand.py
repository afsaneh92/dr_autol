from app import db
from core.controller.admin_registration import logger
from core.validation.helpers import db_error_message
from persistence.database.entity.base import BaseMixin


class Brand(BaseMixin, db.Model):
    __tablename__ = 'brands'
    name = db.Column(db.String, nullable=False)

    # id = db.Column(db.Integer, db.ForeignKey('company_to_brand'))
    def __repr__(self):
        return '<Brand %r>' % self.id

    @staticmethod
    def find(limit=1, **kwargs):
        res = None
        try:
            res = True, Brand.query.filter_by(**kwargs).limit(limit).all()
        except:
            res = db_error_message(logger)
        return res
