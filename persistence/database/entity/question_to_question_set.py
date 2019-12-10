from app import global_logger
from core.validation.helpers import db_error_message
from persistence.database.entity.base import db
from persistence.database.entity.question import Question
from persistence.database.entity.question_set import QuestionSet


class QuestionToQuestionSet(db.Model):
    __tablename__ = 'question_to_question_sets'
    question_set_id = db.Column(db.Integer, db.ForeignKey('question_sets.id'), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    question_set = db.relationship(QuestionSet, backref="question_to_question_set")
    question = db.relationship(Question)
    is_key = db.Column(db.Boolean, default=False)

    def __init__(self, question=None, question_set=None, is_key=None):
        self.question_set = question_set
        self.question = question
        self.is_key = is_key

    def __repr__(self):
        return '<QuestionToQuestionSet %r>' % self.question_set_id
