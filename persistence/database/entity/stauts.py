from app import global_logger
from core.messages.keys import Keys
from core.validation.helpers import db_error_message
from persistence.database.entity.base import BaseMixin, db

logger = global_logger


class Status(BaseMixin, db.Model):
    __tablename__ = 'statuses'
    name = db.Column(db.String(200), nullable=False)
    jobs = db.relationship("Job", backref="job_backref", lazy='dynamic',
                           primaryjoin="Status.id == Job.status_id")

    def __repr__(self):
        return '<Status %r>' % self.id

    @staticmethod
    def find_status(status_name):
        result = True,
        try:
            status = Status.query.filter(Status.name == status_name).first()
            result = True, status
        except:
            result = False, db_error_message(global_logger)
        return result

    @staticmethod
    def load_not_payable_statues_ids():
        try:
            names = [Keys.STATUS_PENDING, Keys.STATUS_CANCELLED_BY_BUSINESS_OWNER, Keys.STATUS_DENIED_BY_BUSINESS_OWNER,
                     Keys.STATUS_CANCELLED_BY_CAR_OWNER, Keys.STATUS_TIMEOUT]
            tuple_ids = Status.query.filter(Status.name.in_(names)).with_entities(Status.id).all()
            ids = [r for (r,) in tuple_ids]
            return True, ids
        except:
            return False, db_error_message(logger)

    @staticmethod
    def load_status(status_name):
        return Status.find_status(status_name)
