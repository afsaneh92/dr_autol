import logging
from sqlalchemy.ext.associationproxy import association_proxy
from persistence.database.entity.base import BaseMixin, db

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class QuestionSet(BaseMixin, db.Model):
    __tablename__ = 'question_sets'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(64))
    questions = association_proxy('question_to_question_set', 'question')
    # questionservice_grade_type = db.relationship("ServiceGradeType")

    def __repr__(self):
        return '<QuestionSet %r>' % self.id

    def __init__(self, label):
        self.label = label
