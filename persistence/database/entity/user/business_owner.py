#!/usr/bin/env python
# -*- coding: utf-8 -*-
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy.exc import InvalidRequestError

from app import db, global_logger
from core.messages.keys import Keys

from core.messages.translator.messages_keys import MessagesKeys
from core.result.success.success_update import SuccessUpdate
from core.validation.helpers import db_error_message
from persistence.database.entity.user.user import User

logger = global_logger


class BusinessOwner(User):
    __tablename__ = 'business_owners'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    phone_number_workspace = db.Column(db.String(11), nullable=True)
    # order_items = db.relationship("OrderItem")
    address = db.Column(db.String(100), nullable=True)
    workspace_name = db.Column(db.String(20), nullable=True)
    lat = db.Column(DOUBLE_PRECISION(), nullable=True)
    lng = db.Column(DOUBLE_PRECISION(), nullable=True)
    geom = db.Column(Geometry('POINT', srid=Keys.SRID_VALUE), nullable=True)
    flags = db.Column(db.JSON, default={Keys.ACTIVATION_STATUS: True})
    uuid = db.Column(db.String(300), nullable=True, default='75106e9e-a9eb-11e8-a66e-34f39aa7f24b')

    __mapper_args__ = {
        'polymorphic_identity': 'BusinessOwners',
    }

    def __repr__(self):
        return '<BusinessOwners %r>' % self.id

    @staticmethod
    def find(limit=1, **kwargs):
        res = None
        try:
            res = True, BusinessOwner.query.filter_by(**kwargs).limit(limit).all()
        except:
            res = db_error_message(logger)
        return res

    @staticmethod
    def update_lng_lat(id, lng, lat, db_connection):
        geom = 'SRID=' + str(Keys.SRID_VALUE) + ';POINT(' + str(lng) + " " + str(lat) + ')'
        data = {Keys.LAT: lat, Keys.LNG: lng, Keys.GEOM: geom}
        return BusinessOwner.update_by_id(id, db_connection, data)

    @staticmethod
    def update_by_id(id, db_connection, data):
        result = None
        try:
            BusinessOwner.query.filter_by(id=id).update(data)
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

