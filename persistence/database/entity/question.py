import logging
from persistence.database.entity.base import BaseMixin, db
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Question(db.Model, BaseMixin):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    factor = db.Column(db.Integer, nullable=True)

    def __init__(self, question):
        self.question = question

    def __repr__(self):
        return '<Question %r>' % self.id
