"""
Many to many of service_grades and service_types
"""

from app import db
from persistence.database.entity.base import BaseMixin


class ServiceGradeType(BaseMixin, db.Model):
    __tablename__ = 'service_grade_type'
    service_grade_id = db.Column(db.Integer, db.ForeignKey('service_grades.id'))
    service_type_id = db.Column(db.Integer, db.ForeignKey('service_types.id'))
    price = db.Column(db.Numeric, nullable=True)
    service_type = db.relationship("ServiceType")
    # question_set_id = db.Column(db.Integer, db.ForeignKey('question_sets.id'))

    @staticmethod
    def load_service_price(service_grade_id, service_type_id):
        price_result = None
        try:
            price_result = True, ServiceGradeType.query. \
                filter(ServiceGradeType.service_grade_id == service_grade_id). \
                filter(ServiceGradeType.service_type_id == service_type_id). \
                with_entities(ServiceGradeType.price). \
                one().price
        except:
            pass
        return price_result
