#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta

from sqlalchemy import text
from sqlalchemy.exc import InvalidRequestError

from app import db, global_logger
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result.failure.not_finished_job import NotFinishedJob
from core.result.failure.not_found_user import UserNotFound
from core.result.failure.rated_before import RatedBefore
from core.result.failure.todo_list_is_not_empty import TodoListNotEmpty
from core.result.success.success_accept_job import SuccessAcceptJob, SuccessDenyJob
from core.result.success.success_cancel_job import SuccessCancelJob
from core.result.success.success_car_owner_order import SuccessCarOwnerOrder
from core.result.success.success_in_qeue_jobs import SuccessInQueueJobs
from core.result.success.success_list_of_unfinished_job import SuccessListOfUnfinishedJob
from core.result.success.success_register_problem import SuccessRegisterProblem
from core.result.success.success_update import SuccessUpdate
from core.validation.helpers import db_error_message, expected_time_for_each_job, calculate_real_time_to_finish_job
from persistence.database.entity.base import BaseMixin
from persistence.database.entity.business_owner import BusinessOwners
from persistence.database.entity.user.car_owner import CarOwner
from persistence.database.entity.car import Car
from persistence.database.entity.job_.job import Job
from persistence.database.entity.question_to_question_set import QuestionToQuestionSet
from persistence.database.entity.stauts import Status

logger = global_logger


class Jobs(BaseMixin, db.Model):
    __tablename__ = 'jobss'
    car_owner_id = db.Column(db.Integer, nullable=False)
    # car_owners = db.relationship("CarOwner", backref="car_owners")

    car_id = db.Column(db.Integer, nullable=False)
    business_owner_id = db.Column(db.Integer, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'), nullable=False)
    status_ = db.relationship('Status')
    start_time = db.Column(db.DateTime, nullable=True)
    finish_time = db.Column(db.DateTime, nullable=True)
    start_schedule = db.Column(db.DateTime, nullable=True)
    finish_schedule = db.Column(db.DateTime, nullable=True)

    # car_problems = db.relationship("CarProblem", backref="car_problem_backref", lazy='dynamic',
    #                                primaryjoin="Job.id == CarProblem.job_id")
    # ranking_question_id = db.Column(db.Integer, db.ForeignKey('ranking_questions.id'), nullable=True)
    # car_problems = db.relationship("CarProblem", backref="car_problem_backref", lazy='dynamic',
    #                                primaryjoin="Job.id == CarProblem.job_id")


    # payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'))
    # payment = db.relationship("Payment", backref="payment_backref", uselist=False)

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __repr__(self):
        return '<Job %r>' % self.id

    # TODO delete
    @staticmethod
    def register_problem(db, job, problems):
        result = True,
        try:
            for problem in problems:
                job.car_problems.append(problem)

            pending_status = Status.load_status(Keys.STATUS_PENDING)
            if not pending_status[0]:
                raise Exception()
            job.status_id = pending_status[1].id
            db.session.add(job)
            db.session.commit()
            result = True, SuccessRegisterProblem(status=200, message=MessagesKeys.SUCCESS_REGISTER_PROBLEM,
                                                  params={Keys.ID: job.id})
        except:
            db.session.rollback()
            result = db_error_message(logger)

        return result

    # TODO delete
    @staticmethod
    def find_order_list(car_owner_id):
        try:
            status_ids = Status.query. \
                filter((Status.name == Keys.STATUS_PENDING) |
                       (Status.name == Keys.STATUS_ACCEPTED_BY_BUSINESS_OWNER)). \
                with_entities(Status.id)
            lis = Jobs.query. \
                join(BusinessOwners, Jobs.business_owner_id == BusinessOwners.id). \
                join(Car, Jobs.car_id == Car.id). \
                join(Status, Jobs.status_id == Status.id). \
                add_columns(Jobs.id, Jobs.start_schedule, BusinessOwners.name, Car.plate_number,
                            Status.name.label("status"), BusinessOwners.workspace_name). \
                filter(Jobs.car_owner_id == car_owner_id). \
                filter(Jobs.status_id.in_(status_ids)). \
                all()
            return True, SuccessCarOwnerOrder(status=200, message=MessagesKeys.SUCCESS_REGISTER_PROBLEM, params=lis)
        except:
            return db_error_message(logger)

    # TODO delete
        list
    # TODO delete
    @staticmethod
    def cancel_job(job, data, db_connection):
        result = True,
        try:
            Jobs.query.filter_by(id=job.id).update(data)
            db_connection.session.commit()
            result = True, SuccessCancelJob(status=200, message=MessagesKeys.SUCCESS_CANCEL_JOB, params=None)
        except:
            result = db_error_message(logger)
        return result

    # TODO delete
    @staticmethod
    def load_status(status_name):
        return Status.find_status(status_name)

    # TODO delete
    @staticmethod
    def accept_deny_job(job, data, db_connection, message=MessagesKeys.SUCCESS_ACCEPT_JOB):
        result = True,
        try:
            Jobs.query.filter_by(id=job.id).update(data)
            db_connection.session.commit()
            if message == MessagesKeys.SUCCESS_ACCEPT_JOB:
                result = True, SuccessAcceptJob(status=200, message=MessagesKeys.SUCCESS_ACCEPT_JOB, params=None)
            else:
                result = True, SuccessDenyJob(status=200, message=MessagesKeys.SUCCESS_DENY_JOB, params=None)

        except:
            result = db_error_message(logger)
        return result

    # TODO delete
    @staticmethod
    def load_all_jobs():
        pass

    # TODO delete
    @staticmethod
    def load_in_queue_jobs(business_owner, service_grade, statuses = []):
        """
        :param statuses:
        :param business_owner:
        :return:
        """
        try:
            names = [Keys.STATUS_ACCEPTED_BY_BUSINESS_OWNER]
            tuple_ids = Status.query.filter(Status.name.in_(names)).with_entities(Status.id).all()

            results = db.session.query(Jobs, Car) \
                .join(Car, Car.id == Jobs.car_id) \
                .filter(Jobs.business_owner_id == business_owner.id) \
                .filter(Jobs.status_id.in_(tuple_ids)) \
                .all()
            params = {}
            for result in results:
                service_types = []
                for car_problem in result[0].car_problems:
                    service_types.append(car_problem.services_definition.service_type.name)
                rest = {Keys.AUTO_TYPE: result[1].auto_type_.name, Keys.SERVICE_TYPES: service_types,
                        Keys.JOB_ID: result[0].id}
                params = {result[1].vin_number: rest}

            return True, SuccessInQueueJobs(status=200, message=MessagesKeys.SUCCESS_IN_QUEUE_JOBS, params=params)

        except:
            return db_error_message(logger)

    @staticmethod
    def find(limit=1, **kwargs):
        res = None
        try:
            res = True, Jobs.query.filter_by(**kwargs).limit(limit).all()
        except:
            res = db_error_message(logger, message='InvalidRequestError')
        return res

    @staticmethod
    def is_job_finished(job_id):
        done_job_status_id = Status.query.filter(Status.name == Keys.STATUS_DONE).with_entities(Status.id).all()
        result = Jobs.query \
            .filter(Jobs.id == job_id) \
            .filter(Jobs.status_id.in_(done_job_status_id)).with_entities(Jobs.id).first()
        if result is None:
            return False, NotFinishedJob(status=404, message=MessagesKeys.JOB_IS_NOT_FINISHED, params=None)
        if len(result) == 0:
            return False, NotFinishedJob(status=404, message=MessagesKeys.JOB_IS_NOT_FINISHED, params=None)
        else:
            return True, result[0]

    #TODO delete
    @staticmethod
    def find_all_not_finished_job():
        try:
            time_delta = timedelta(hours=12)
            limited_time_to_follow_up_work = Jobs.start_schedule + time_delta
            expected_time = expected_time_for_each_job(Jobs.start_schedule, Jobs.finish_schedule)
            calculate_real_time = calculate_real_time_to_finish_job(Jobs.start_time, expected_time)

            status_ids = Status.query. \
                filter((Status.name == Keys.STATUS_ACCEPTED_BY_BUSINESS_OWNER) |
                       (Status.name == Keys.STATUS_START)). \
                with_entities(Status.id). \
                all()

            not_start_status = Status.query. \
                filter(Status.name == Keys.STATUS_ACCEPTED_BY_BUSINESS_OWNER). \
                with_entities(Status.id). \
                all()

            list_unfinished1 = Jobs.query. \
                filter(Jobs.status_id.in_(status_ids)). \
                filter(Jobs.start_time is not None). \
                filter(db.func.current_timestamp() > calculate_real_time). \
                with_entities(Jobs.business_owner_id). \
                all()

            list_unfinished2 = Jobs.query. \
                filter(Jobs.status_id.in_(not_start_status)). \
                filter(limited_time_to_follow_up_work < db.func.current_timestamp()). \
                with_entities(Jobs.business_owner_id). \
                all()

            list_unfinished_condition = Jobs.query. \
                filter((Jobs.business_owner_id.in_(list_unfinished2)) | (Jobs.business_owner_id.in_(list_unfinished1))). \
                with_entities(Jobs.business_owner_id). \
                all()

            query = db.session.query(Jobs). \
                join(BusinessOwners, BusinessOwners.id == Jobs.business_owner_id). \
                join(Car, Jobs.car_id == Car.id). \
                filter(Jobs.business_owner_id.in_(list_unfinished_condition)). \
                with_entities(BusinessOwners.name, BusinessOwners.phone_number, Car.plate_number, BusinessOwners.id). \
                all()

            ids = set()
            for result in query:
                ids.add(result)

            return True, SuccessListOfUnfinishedJob(status=200, message=MessagesKeys.SUCCESS_LIST,
                                                    params=ids)
        except:
            return db_error_message(logger)

    @staticmethod
    def is_job_rated_before(job_id):

        # query = db.session.query(Job).join(QuestionToQuestionSet,
        #                                    Job.question_set_id == QuestionToQuestionSet.question_set_id). \
        #     filter(QuestionToQuestionSet.question_id == question_id). \
        #     filter(Job.id == job_id). \
        #     first()
        query = Jobs.query.filter(Jobs.id == job_id). \
            filter(Jobs.rate == []).first()

        result = query
        if result is not None:
            return True, result.id
        else:
            return False, RatedBefore(status=404, message=MessagesKeys.JOB_RATED_BEFORE, params=None)

    @staticmethod
    def update_by_id(id, db_connection, data):
        result = None
        try:
            Jobs.query.filter(Jobs.id == id).update(data)
            db_connection.session.commit()
            logger.info('update question_sets. ID: %s' % id)
            params = {Keys.ID: id}
            success = SuccessUpdate(status=200, message=MessagesKeys.SUCCESS_UPDATE, params=params)
            result = True, success
        except InvalidRequestError as error:
            result = db_error_message(logger)
            db_connection.session.rollback()
        except:
            result = db_error_message(logger)
            db_connection.session.rollback()
        return result

    @staticmethod
    def add_rate(id, db_connection, data):
        result = None
        try:
            res = Jobs.query.filter(Jobs.id == id).first()
            result0 = res.rate.append(data)
            resu1 = res.rate
            re = {Keys.ID: id, Keys.RATE: resu1}
            Jobs.query.filter(Jobs.id == id).update(re)

            db_connection.session.commit()
            logger.info('update question_sets. ID: %s' % id)
            params = {Keys.ID: id}
            success = SuccessUpdate(status=200, message=MessagesKeys.SUCCESS_UPDATE, params=params)
            result = True, success


        except InvalidRequestError as error:
            result = db_error_message(logger)
            db_connection.session.rollback()



    @staticmethod
    def count_questions_in_question_set(question_set_id, rate):

        list_of_questions_in_a_question_set = QuestionToQuestionSet.query. \
            filter(QuestionToQuestionSet.question_set_id == question_set_id).all()
        # list_of_rate_for_one_job = Job.query.filter(Job.question_set_id == question_set_id). \
        #     filter(Job.id == job_id).with_entities(Job.rate).all()

        if len(list_of_questions_in_a_question_set) == len(rate):
            return True, list_of_questions_in_a_question_set
        else:
            return False, RatedBefore(status=404, message=MessagesKeys.JOB_RATED_BEFORE, params=None)

    @staticmethod
    def is_car_owner_and_his_job_matched(job_id, phone_number):
        query = db.session.query(Jobs).join(CarOwner,
                                           Job.car_owner_id == CarOwner.id). \
            filter(Job.id == job_id). \
        query = db.session.query(Jobs).join(CarOwner,
                                            Jobs.car_owner_id == CarOwner.id). \
            filter(Jobs.id == job_id). \
            with_entities(CarOwner.phone_number). \
            first()
        if query[0].encode("utf-8") == phone_number:
            return True, job_id
        else:
            return False, UserNotFound(status=404, message=MessagesKeys.ID_IS_NOT_IN_DB, params=None)

    @staticmethod
    def is_business_owner_jobs_list_is_empty(business_owner_id):
        todo_list__status = Status.query. \
            filter((Status.name == Keys.STATUS_ACCEPTED_BY_BUSINESS_OWNER) |
                   (Status.name == Keys.STATUS_START) |
                   (Status.name == Keys.STATUS_PENDING)). \
            with_entities(Status.id). \
            all()
        query = Jobs.query.filter(Jobs.business_owner_id == business_owner_id). \
            filter(Jobs.status_id.in_(todo_list__status)).all()

        if query == []:
            return True, business_owner_id

        else:
            return False, TodoListNotEmpty(status=404, message=MessagesKeys.TODO_LIST_IS_NOT_EMPTY, params=None)
