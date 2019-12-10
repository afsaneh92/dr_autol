"""
Many to many of service_grades and service_types
"""
# from aenum import enum
import enum
from sqlalchemy import String, Numeric
from sqlalchemy.ext.associationproxy import association_proxy

from app import db, global_logger
from core.validation.helpers import db_error_message
from persistence.database.entity.base import BaseMixin

logger = global_logger


class ServiceCategoryEnum(enum.Enum):
    AutoService = "AutoService"
    Insurance = "Insurance"
    CarWash = "CarWash"


class ServiceGradeEnum(enum.Enum):
    Common = "Common"
    Plus = "Plus"
    Premium = "Premium"
    InCarWash = "InCarWash"
    InPlaceWash = "InPlaceWash"

    # @classmethod
    # def has_value(cls, value):
    #     return any(value == item.value for item in cls)


class ServicesDefinition(BaseMixin, db.Model):
    __tablename__ = 'services_definition'

    service_grade = db.Column(String(50), nullable=False)
    # TODO pay attention to name="cat" db.Enum('M', 'F', name='gender_types') https://stackoverflow.com/questions/24254775/error-when-running-migrations-sqlalchemy-exc-compileerror-postgresql-enum-type
    service_category = db.Column(db.Enum("AutoService", "Insurance", "CarWash", name="service_category"), nullable= False)
    pay = db.Column(Numeric, nullable=False)
    question_set_id = db.Column(db.Integer, db.ForeignKey('question_sets.id'))
    question_set = db.relationship("QuestionSet", backref=db.backref("services_definition", uselist=False))

    service_type_id = db.Column(db.Integer, db.ForeignKey('service_types.id'))
    service_type = db.relationship("ServiceType", back_populates="service_definitions")

    __table_args__ = (db.UniqueConstraint('service_grade', 'service_type_id', name='unique_services'),)

    @staticmethod
    def load_service_by_id(service_definition_id=None, service_type_id=None):
        try:
            query = ServicesDefinition.load_service_query_builder(service_definition_id, service_type_id)
            return True, query.first()
        except:
            return db_error_message(logger)

    @staticmethod
    def load_service_query_builder(service_definition_id, service_type_id):
        query = db.session.query(ServicesDefinition)
        if service_definition_id is not None:
            query = query.filter(ServicesDefinition.id == service_definition_id)
        if service_type_id is not None:
            query = query.filter(ServicesDefinition.service_type_id == service_type_id)
        return query
