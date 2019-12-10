from app import db, global_logger
from core.messages.translator.messages_keys import MessagesKeys
from core.result.success.success_add_service_grade import SuccessAddServiceGrade
from core.result.success.success_list_service_grades import SuccessListServiceGrades
from core.result.success.success_list_service_type import SuccessListServiceTypes
from core.result.success.success_service_type_registration import SuccessServiceTypeRegistration
from core.validation.helpers import db_error_message
from persistence.database.entity.base import BaseMixin

logger = global_logger


class ServiceGrade(BaseMixin, db.Model):
    __tablename__ = 'service_grades'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    service_types = db.relationship("ServiceGradeType")

    def __repr__(self):
        return '<ServiceGrade %r>' % self.name

    @staticmethod
    def list_service_grades():
        result = None
        try:

            grades_list = ServiceGrade.query. \
                add_columns(ServiceGrade.id, ServiceGrade.name). \
                all()
            success = SuccessListServiceGrades(status=200, message=MessagesKeys.SUCCESS_LIST, params=grades_list)
            result = True, success
        except:
            result = db_error_message(logger)

        return result

    @staticmethod
    def list_service_types(service_grade_id):
        result = None
        try:
            types_list = ServiceGrade.query. \
                filter_by(id=service_grade_id). \
                all()
            result = True, SuccessListServiceTypes(status=200, message=MessagesKeys.SUCCESS_LIST, params=types_list)
        except:
            result = db_error_message(logger)

        return result

    def add_service_grade(self, db_connection):
        db_connection.session.begin(subtransactions=True)
        result = None
        try:
            db_connection.session.add(self)
            db_connection.session.commit()
            logger.info('Add new service grade. Service grade id: %s', self.id)
            params = {"id": self.id, "service_grade_name": self.name}
            success = SuccessAddServiceGrade(status=200, message=MessagesKeys.SUCCESS_ADD_SERVICE_GRADE, params=params)
            result = True, success
        except:
            db_connection.session.rollback()
            result = db_error_message(logger)

        return result

    @staticmethod
    def register_service_type(service_grade, service_type, db_):
        try:
            service_grade.service_types.append(service_type)
            db_.session.commit()
            return True, SuccessServiceTypeRegistration(status=200, message=MessagesKeys.SUCCESS_ADD_SERVICE_TYPE,
                                                        params=None)
        except:
            db_.session.rollback()
            return db_error_message(logger)

    @staticmethod
    def load_service_grade(grade_id):
        try:
            return ServiceGrade.query.filter_by(id=grade_id).first()
        except:
            pass
