from sqlalchemy import Column, String

from app import db, global_logger
from persistence.database.entity.base import BaseMixin

logger = global_logger


class CarColor(BaseMixin, db.Model):
    __tablename__ = 'colors'
    name = Column(String(11), nullable=False)

    def __repr__(self):
        return '<AutoType %r>' % self.name
