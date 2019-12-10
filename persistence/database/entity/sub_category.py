from app import db, global_logger
from core.validation.helpers import db_error_message
from persistence.database.entity.base import BaseMixin

logger = global_logger


class SubCategory(BaseMixin, db.Model):
    __tablename__ = 'sub_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    products = db.relationship("Product")
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __repr__(self):
        return '<SubCategory %r>' % self.id

    @staticmethod
    def load_by_id(id):
        res = None
        try:
            res = True, SubCategory.query.filter_by(id=id).all()
        except:
            res = db_error_message(logger, message='InvalidRequestError')
        return res
