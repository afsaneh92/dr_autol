from app import db, global_logger
from persistence.database.entity.base import BaseMixin

logger = global_logger


class Category(BaseMixin, db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    sub_categories = db.relationship("SubCategory")

    def __repr__(self):
        return '<Category %r>' % self.id
