#!/usr/bin/env python
# -*- coding: utf-8 -*-
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy.exc import InvalidRequestError

from app import db, global_logger
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result.success.success_add_new_user import SuccessAddNewUser
from core.result.failure.not_found_user import UserNotFound
from core.result.success.success_update import SuccessUpdate
from core.validation.helpers import db_error_message
from persistence.database.entity.base import BaseMixin
from abc import abstractmethod

logger = global_logger


class User(BaseMixin, db.Model):
    __tablename__ = 'users'
    name = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(11), unique=True, nullable=False)
    validate = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(300), nullable=False)
    code = db.Column(db.String(4), nullable=True)
    reg_id = db.Column(db.String(500), nullable=True)

    type = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'User',
        # TODO with_polymorphic??????
        # 'with_polymorphic': '*',
        'polymorphic_on': type
    }

    def __repr__(self):
        return '<User %r>' % self.id

    @staticmethod
    def generate_hash_password(password):
        return pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)

    @staticmethod
    @abstractmethod
    def update_by_id(id, db_connection, data):
        result = None
        try:
            User.query.filter_by(id=id).update(data)
            db_connection.session.commit()
            logger.info('update user. ID: %s' % id)
            params = {"user_id": id}
            success = SuccessUpdate(status=200, message=MessagesKeys.SUCCESS_UPDATE, params=params)
            # raise Exception()
            result = True, success

        except InvalidRequestError as error:
            result = db_error_message(logger)
            db_connection.session.rollback()

        except:
            result = db_error_message(logger)
            db_connection.session.rollback()
        return result

    def update(self, db_connection, data):
        result = None
        try:
            User.query.filter_by(phone_number=self.phone_number).update(data)
            user = User.query.filter_by(phone_number=self.phone_number).first()
            self.id = user.id
            db_connection.session.commit()
            logger.info('update user. ID: %s' % self.id)
            params = {"user_id": self.id}
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
    def update_reg_id(phone_number, reg_id, db_connection):
        user = User(phone_number=phone_number)
        data = {Keys.REG_ID: reg_id}
        update_result = user.update(db_connection, data)
        return update_result

    @staticmethod
    def find(limit=1, **kwargs):
        res = None
        try:
            res = True, User.query.filter_by(**kwargs).limit(limit).all()
        except:
            res = db_error_message(logger)
        return res

    @staticmethod
    def find_login(phone_number):
        res = None
        try:
            res = True, User.query.filter(User.phone_number == phone_number).first()
        except:
            res = db_error_message(logger)
        return res

    def is_registered(self):
        count = User.query.filter_by(phone_number=self.phone_number).count()
        if not count == 0:
            return True
        return False

    def is_valid(self):
        count = User.query.filter_by(phone_number=self.phone_number, validate=True).count()
        if count == 0:
            return False
        return True

    def is_invalid(self):
        count = User.query.filter_by(phone_number=self.phone_number, validate=False).count()
        if count == 0:
            return False
        return True

    def add(self, db_connection):
        result = None
        try:
            hashed = User.generate_hash_password(self.password)
            self.password = hashed
            db_connection.session.add(self)
            db_connection.session.commit()
            logger.info('Add new user. User id: %s', self.id)
            params = {"user_id": self.id}
            success = SuccessAddNewUser(status=200, message=MessagesKeys.SUCCESS_ADD_NEW_USER, params=params)
            result = True, success
        except:
            db_connection.session.rollback()
            result = db_error_message(logger)
        return result

    @staticmethod
    def load_user_reg_id(user_id):
        return User.query. \
            add_columns(User.name, User.reg_id). \
            filter(User.id == user_id). \
            first()
