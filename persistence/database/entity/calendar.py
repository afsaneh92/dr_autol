import logging

from sqlalchemy import String
from sqlalchemy import cast
from sqlalchemy import or_, and_
from sqlalchemy.exc import InvalidRequestError

from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result.success.success_add_job_calendar import SuccessAddNewJob
from core.result.success.success_delete_job import SuccessDeleteJob
from core.result.success.success_update import SuccessUpdate
from core.validation.helpers import db_error_message
from persistence.database.entity.base import BaseMixin, db

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Calendar(BaseMixin, db.Model):
    __tablename__ = 'calendars'
    job_id = db.Column(db.Integer, nullable=True)
    business_owner = db.relationship('AutoServiceBusinessOwner')
    business_owner_id = db.Column(db.Integer, db.ForeignKey('auto_service_business_owners.id'))
    start_time = db.Column(db.DateTime, nullable=False)
    finish_time = db.Column(db.DateTime, nullable=False)
    flag = db.Column(db.JSON, nullable=False, default={Keys.DELETED: 0})

    def __repr__(self):
        return '<Calendar %r>' % self.id

    def add(self, db_connection, calendar):
        result = None
        try:
            db_connection.session.add(self)
            db_connection.session.commit()
            self.business_owner.calendars.extend([calendar])
            logger.info('Add new job. Job id: %s', self.id)
            params = {Keys.CALENDAR_ID: self.id}
            success = SuccessAddNewJob(status=200, message=MessagesKeys.SUCCESS_ADD_NEW_JOB, params=params)
            result = True, success
        except:
            db_connection.session.rollback()
            result = db_error_message(logger)

        return result

    @staticmethod
    def delete_by_id(db_connection, business_owner_id):
        result = None
        db_connection.session.begin(subtransactions=True)
        try:
            Calendar.query.filter_by(id=business_owner_id).update({Keys.FLAG: {Keys.ACTIVATION_STATUS: 1}})

            job = Calendar.find(1, id=business_owner_id)[1][0]
            logger.info('Delete business_owner id: %s', business_owner_id)
            db_connection.session.commit()
            params = {Keys.ID: business_owner_id}
            success = SuccessDeleteJob(status=200, message=MessagesKeys.SUCCESS_DELETE_JOB, params=params)
            result = True, success
            db_connection.session.commit()
        except:
            db_connection.session.rollback()
            result = db_error_message(logger)

        return result

    def update(self, db_connection, data):
        result = None
        try:
            Calendar.query.filter_by(id=self.id).update(data)
            db_connection.session.commit()
            logger.info('update business_owner. ID: %s' % self.id)
            params = {Keys.ID: self.id}
            success = SuccessUpdate(status=200, message=MessagesKeys.SUCCESS_UPDATE, params=params)
            result = True, success
        except InvalidRequestError as error:
            result = db_error_message(logger, message='InvalidRequestError')
            db_connection.session.rollback()

        except:
            result = db_error_message(logger)
            db_connection.session.rollback()
        return result

    @staticmethod
    def find(limit=1, **kwargs):
        res = None
        try:
            res = True, Calendar.query.filter_by(**kwargs).limit(limit).all()
        except:
            res = db_error_message(logger, message='InvalidRequestError')
        return res

    @staticmethod
    def count_conflict(start_time, finish_time, business_owner_id):
        res = None
        try:
            # q = Calendar.query \
            #     .filter(or_(
            #             and_(Calendar.start_time <= start_time, Calendar.finish_time <= start_time),
            #             and_(Calendar.start_time >= finish_time, Calendar.finish_time <= finish_time))) \
            #     .filter(Calendar.business_owner_id == business_owner_id)

            q = Calendar.query \
                .filter(or_(
                and_(Calendar.start_time < finish_time, Calendar.finish_time >= finish_time),
                and_(Calendar.finish_time > start_time, Calendar.finish_time <= finish_time))) \
                .filter(Calendar.business_owner_id == business_owner_id) \
                .filter(cast(Calendar.flag[Keys.DELETED], String) == cast(0, String))
            res = True, q.count()
        except:
            res = db_error_message(logger, message='InvalidRequestError')
        return res
