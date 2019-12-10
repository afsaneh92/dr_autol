from sqlalchemy import Column, String

from app import db, global_logger
from persistence.database.entity.base import BaseMixin

logger = global_logger


class AutoModel(BaseMixin, db.Model):
    __tablename__ = 'auto_models'
    name = Column(String(70), nullable=False)
    auto_types_id = Column(db.Integer, db.ForeignKey('auto_types.id'))

    def __repr__(self):
        return '<AutoModel %r>' % self.name
