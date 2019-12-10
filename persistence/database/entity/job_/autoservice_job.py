#!/usr/bin/env python
# -*- coding: utf-8 -*-
from persistence.database.entity.user.user import User
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result.success.scuucess_start_a_job import SuccessStartJob
from core.result.success.success_accept_job import SuccessAcceptJob, SuccessDenyJob
from core.result.success.success_car_owner_order import SuccessCarOwnerOrder
from core.validation.helpers import db_error_message
from persistence.database.entity.car_problem import CarProblem
from persistence.database.entity.user.business_owner import BusinessOwner
from persistence.database.entity.car import Car
from persistence.database.entity.job_.job import Job
from persistence.database.entity.stauts import Status
from persistence.database.helpers import update_record_from_dictionary
from app import db, global_logger

logger = global_logger


class AutoServiceJob(Job):
    __tablename__ = 'auto_service_job'
    id = db.Column(db.Integer, db.ForeignKey('jobs.id'), primary_key=True)
    start_time = db.Column(db.DateTime, nullable=True)
    finish_time = db.Column(db.DateTime, nullable=True)
    start_schedule = db.Column(db.DateTime, nullable=False)
    finish_schedule = db.Column(db.DateTime, nullable=False)
    car_problems = db.relationship(CarProblem, backref="car_problem_backref", lazy='dynamic',
                                   primaryjoin="AutoServiceJob.id == CarProblem.job_id")
    second_type= db.Column(db.String(20), default='AutoService', nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'AutoService',
    }

    @staticmethod
    def find(limit=1, **kwargs):
        res = None
        try:
            res = True, AutoServiceJob.query.filter_by(**kwargs).limit(limit).all()
        except:
            res = db_error_message(logger, message='InvalidRequestError')
        return res

    @staticmethod
    def accept_deny_job(job, data, db_connection, where_clause=None, message=MessagesKeys.SUCCESS_ACCEPT_JOB):
        result = True,
        try:
            query = Job.query.filter_by(id=job.id)
            # if where_clause is not None:
            #     query = query.filter_by(where_clause)
            query.update(data)
            db_connection.session.commit()
            if message == MessagesKeys.SUCCESS_ACCEPT_JOB:
                result = True, SuccessAcceptJob(status=200, message=MessagesKeys.SUCCESS_ACCEPT_JOB, params=None)
            else:
                result = True, SuccessDenyJob(status=200, message=MessagesKeys.SUCCESS_DENY_JOB, params=None)

        except:
            result = db_error_message(global_logger)
        return result

    @staticmethod
    def has_overlap_jobs(job):
        try:
            stat_id = Status.query. \
                filter(Status.name == Keys.STATUS_START). \
                with_entities(Status.id). \
                first().id
            count = Job.query. \
                filter(Job.status_id == stat_id). \
                filter(Job.business_owner_id == job.business_owner_id). \
                count()
            return True, count

        except:
            return db_error_message(global_logger)

    @staticmethod
    def find_order_list(car_owner_id):
        try:
            status_ids = Status.query. \
                filter((Status.name == Keys.STATUS_PENDING) |
                       (Status.name == Keys.STATUS_ACCEPTED_BY_BUSINESS_OWNER)). \
                with_entities(Status.id)
            lis = AutoServiceJob.query. \
                join(BusinessOwner, AutoServiceJob.business_owner_id == BusinessOwner.id). \
                join(Car, Job.car_id == Car.id). \
                join(Status, AutoServiceJob.status_id == Status.id). \
                add_columns(AutoServiceJob.id, AutoServiceJob.start_schedule, BusinessOwner.name, Car.plate_number,
                            Status.name.label("status"), BusinessOwner.workspace_name). \
                filter(AutoServiceJob.car_owner_id == car_owner_id). \
                filter(AutoServiceJob.status_id.in_(status_ids)). \
                all()
            return True, SuccessCarOwnerOrder(status=200, message=MessagesKeys.SUCCESS_REGISTER_PROBLEM, params=lis)
        except:
            return db_error_message(global_logger)

    def update_status(self, data, db_connection):
        try:
            job = Job.query.filter(Job.id == self.id).first()
            free_error, updated_job = update_record_from_dictionary(job, data)
            if not free_error:
                return free_error, updated_job
            db_connection.session.merge(updated_job)
            return True, SuccessStartJob(status=200, message=MessagesKeys.SUCCESS_IN_QUEUE_JOBS, params=None)
        except:
            result = db_error_message(global_logger)
        return result

    @staticmethod
    def unfinished(wanted_list):
        try:
            result = db.session.query(Job). \
                join(User, User.id == Job.business_owner_id). \
                join(Car, Job.car_id == Car.id). \
                filter(Job.business_owner_id.in_(wanted_list)). \
                with_entities(User.name, User.phone_number, Car.plate_number, User.id). \
                all()

            return True, result

        except:
            return db_error_message(logger)
