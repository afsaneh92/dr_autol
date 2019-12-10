from app import db, global_logger
from core.messages.translator.messages_keys import MessagesKeys
from core.result.success.success_service_type_registration import SuccessServiceTypeRegistration
from core.validation.helpers import db_error_message
from persistence.database.entity.base import BaseMixin
from persistence.database.entity.consumable_item import ConsumableItem
from persistence.database.entity.services import ServiceGradeType

logger = global_logger


class ServiceType(BaseMixin, db.Model):
    __tablename__ = 'service_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    consumable_items = db.relationship(ConsumableItem)
    service_definitions = db.relationship("ServicesDefinition", back_populates="service_type")

    __table_args__ = (db.UniqueConstraint('name', name='unique_service_type'),)

    def __repr__(self):
        return '<ServiceType %r>' % self.name

    def add_service_type(self, db_connection):
        db_connection.session.begin(subtransactions=True)
        result = None
        try:
            db_connection.session.add(self)
            db_connection.session.commit()
            logger.info('Add new service type. Service type id: %s', self.id)
            params = {"id": self.id, "service_type_name": self.name}
            success = SuccessServiceTypeRegistration(status=200, message=MessagesKeys.SUCCESS_ADD_SERVICE_TYPE,
                                                     params=params)
            result = True, success
        except:
            db_connection.session.rollback()
            result = db_error_message(logger)

        return result

    @staticmethod
    def load_service_types(service_grade, service_type):
        service_types = ServiceType.query. \
            join(ServiceGradeType, ServiceGradeType.service_type_id == ServiceType.id). \
            filter(ServiceGradeType.service_grade_id == service_grade). \
            filter(ServiceType.id.in_(service_type)). \
            all()
        types = []
        for re in service_types:
            types.append(re.name)
        return types

    @staticmethod
    def load_service_by_id(service_id):
        try:
            return True, ServiceType.query.filter(ServiceType.id == service_id).first()
        except:
            return False, db_error_message(logger)
