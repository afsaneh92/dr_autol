#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections

from sqlalchemy import desc
from sqlalchemy.exc import InvalidRequestError
from app import db, global_logger
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result.success.success_cancel_job import SuccessCancelJob
from core.result.success.scuucess_start_a_job import SuccessStartJob
from core.result.success.success_list_of_finished_job import SuccessListOfFinishedJob
from core.result.success.success_list_of_payable_job import SuccessListOfPayableJob
from core.result.success.success_list_of_unfinished_job import SuccessListOfUnfinishedJob
from core.result.success.success_register_problem import SuccessRegisterProblem
from core.result.success.success_update import SuccessUpdate
from core.validation.helpers import db_error_message
from core.validation.helpers import db_error_message, calculate_real_time_to_finish_job, expected_time_for_each_job
from persistence.database.entity.auto_type import AutoType
from persistence.database.entity.base import BaseMixin
from persistence.database.entity.car import Car
from persistence.database.entity.car_problem import CarProblem
from persistence.database.entity.payment_.payment import Payment
from persistence.database.entity.question import Question
from persistence.database.entity.question_to_question_set import QuestionToQuestionSet
from persistence.database.entity.service_definition import ServicesDefinition
from persistence.database.entity.user.business_owner import BusinessOwner
from persistence.database.entity.stauts import Status
from persistence.database.entity.user.user import User
from persistence.database.helpers import update_record_from_dictionary
from collections import defaultdict

logger = global_logger


class Job(BaseMixin, db.Model):
    __tablename__ = 'jobs'
    car_owner_id = db.Column(db.Integer, nullable=False)
    car_id = db.Column(db.Integer, nullable=False)
    business_owner_id = db.Column(db.Integer, nullable=True)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'), nullable=True)
    status_ = db.relationship(Status)
    price = db.Column(db.Numeric, nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'), nullable=True)
    payment = db.relationship("Payment", back_populates="job")
    rate = db.Column(db.ARRAY(db.NUMERIC), index=True, default=[])
    question_set_id = db.Column(db.Integer, db.ForeignKey('question_sets.id'), nullable=True)
    question_sets = db.relationship("QuestionSet", backref="question_sets")
    invoice_number = db.Column(db.String(), nullable=True)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'Job',
        'polymorphic_on': type
    }

    def __repr__(self):
        return '<Jobs %r>' % self.id

    @staticmethod
    def find(limit=1, **kwargs):
        res = None
        try:
            res = True, Job.query.filter_by(**kwargs).limit(limit).all()
        except:
            res = db_error_message(logger, message='InvalidRequestError')
        return res

    @staticmethod
    def load_job(job_id):
        try:
            job = Job.query.filter(Job.id == job_id).first()
            return True, job
        except:
            return db_error_message(logger)

    def update(self, db_connection, data):
        result = None
        try:
            db_connection.session.begin(subtransactions=True)
            Job.query.filter_by(id=self.id).update(data)
            db_connection.session.commit()
            logger.info('update job. ID: %s' % self.id)
            params = {"id": self.id}
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
    def register_problem(db, job, problems):
        result = True,
        try:
            job.car_problems.extend(problems)
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

    def update_status(self, data, db_connection):
        try:
            job = Job.query.filter(Job.id == 1).first()
            free_error, updated_job = update_record_from_dictionary(job, data)
            if not free_error:
                return free_error, updated_job
            db_connection.session.merge(updated_job)
            return True, SuccessStartJob(status=200, message=MessagesKeys.SUCCESS_IN_QUEUE_JOBS, params=None)
        except:
            result = db_error_message(global_logger)
        return result

    @staticmethod
    def update_by_id(id, db_connection, data):
        result = None
        try:
            Job.query.filter(Job.id == id).update(data)
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
    def count_questions_in_question_set(job):
        wanted_question_set_id = job.question_set_id
        list_of_questions_in_a_question_set = QuestionToQuestionSet.query. \
            filter(QuestionToQuestionSet.question_set_id == wanted_question_set_id).all()
        return list_of_questions_in_a_question_set

    @staticmethod
    def is_job_finished():
        done_job_status_id = Status.query.filter(Status.name == Keys.STATUS_DONE).with_entities(Status.id).all()
        return done_job_status_id[0].id

    @staticmethod
    def cancel_job(job, data, db_connection):
        result = True,
        try:
            Job.query.filter_by(id=job.id).update(data)
            db_connection.session.commit()
            result = True, SuccessCancelJob(status=200, message=MessagesKeys.SUCCESS_CANCEL_JOB, params=None)
        except:
            result = db_error_message(logger)
        return result

    @staticmethod
    def find_all_finished_job(car_owner_id):
        try:
            finished_status = Status.query.filter(Status.name == Keys.STATUS_DONE). \
                with_entities(Status.id)


            jobsss = db.session.query(Job, BusinessOwner). \
                join(BusinessOwner, BusinessOwner.id == Job.business_owner_id). \
                filter(Job.rate == []). \
                filter(Job.car_owner_id == car_owner_id). \
                filter(Job.status_id.in_(finished_status)). \
                order_by(desc(Job.id)).all()






            car_owner_finished_jobs_question_set_id = Job.query.filter(Job.status_id.in_(finished_status)). \
                filter(Job.rate == []). \
                filter(Job.car_owner_id == car_owner_id). \
                with_entities(Job.question_set_id).all()

            question_ids = QuestionToQuestionSet.query. \
                filter(QuestionToQuestionSet.question_set_id.in_(car_owner_finished_jobs_question_set_id)). \
                with_entities(QuestionToQuestionSet.question_id).all()

            query_results = db.session.query(Job). \
                join(QuestionToQuestionSet, QuestionToQuestionSet.question_set_id == Job.question_set_id). \
                join(Question, QuestionToQuestionSet.question_id == Question.id). \
                join(BusinessOwner, BusinessOwner.id == Job.business_owner_id). \
                filter(Question.id.in_(question_ids)). \
                filter(Job.car_owner_id == car_owner_id). \
                with_entities(Question.question, Job.car_owner_id, BusinessOwner.name, BusinessOwner.uuid, Job.id,
                              Job.type,
                              QuestionToQuestionSet.is_key). \
                order_by(desc(Job.id)). \
                all()

            final_result = defaultdict(list)
            for result in query_results:
                key = result.id
                final_result[key].append(result)

            return True, SuccessListOfFinishedJob(status=200, message=MessagesKeys.SUCCESS_LIST, params=jobsss)

        except:
            return db_error_message(logger)

    @staticmethod
    def find_all_payable_job(car_owner_id):
        try:
            # results = db.session.query(Job). \
            #     join(CarProblem, CarProblem.job_id == Job.id). \
            #     join(ServicesDefinition, CarProblem.services_definition_id == ServicesDefinition.id). \
            #     filter(Job.payment_id.is_(None)). \
            #     filter(Job.car_owner_id == car_owner_id). \
            #     with_entities(Job.id, Job.car_id, Job.price, ServicesDefinition.pay, ServicesDefinition.service_grade,
            #                   ServicesDefinition.service_category).all()

            # job1 = db.session.query(Job) \
            #     .filter(Job.type.in_(['AutoService'])) \
            #     .filter(Job.car_owner_id == car_owner_id) \
            #     .filter(Job.payment_id.is_(None)).all()
            # # print jobs

            list_items = db.session.query(Job, Car, User) \
                .filter(Job.car_owner_id == Car.car_owner_id) \
                .filter(User.id == Job.business_owner_id) \
                .filter(Job.type == 'AutoService') \
                .filter(Job.car_owner_id == car_owner_id) \
                .filter(Job.payment_id.is_(None)).all()

            # items = set()
            # for result in jobs:
            #     items.add(result)
            # print jobs

            result = SuccessListOfPayableJob(status=200, message=MessagesKeys.SUCCESS_LIST, params=list_items)
            return True, result
        except:
            return db_error_message(logger)

    @staticmethod
    def load_jobs_by_statuses_for_business_owner(business_owner, statuses=[]):
        try:
            query = db.session.query(Job, Car) \
                .join(Car, Car.id == Job.car_id) \
                .filter(Job.business_owner_id == business_owner.id)

            if not len(statuses) == 0:
                desired_status_ids = Status.query.filter(Status.name.in_(statuses)).with_entities(Status.id).all()
                query = query.filter(Job.status_id.in_(desired_status_ids))
            results = query.all()
            return True, results

        except:
            return db_error_message(logger)
