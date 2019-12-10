from geoalchemy2 import Geometry
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy.exc import InvalidRequestError

from app import db, global_logger
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result.success.success_add_new_user import SuccessAddNewUser
from core.result.success.success_update import SuccessUpdate
from core.validation.helpers import db_error_message
from persistence.database.entity.base import BaseMixin
from persistence.database.entity.business_owner_task import BusinessOwnerTask
from persistence.database.entity.calendar import Calendar
from persistence.database.entity.services import ServiceGradeType

logger = global_logger


class BusinessOwners(BaseMixin, db.Model):
    __tablename__ = 'business_ownerss'
    name = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(11), nullable=False)
    phone_number_workspace = db.Column(db.String(11), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    workspace_name = db.Column(db.String(20), nullable=True)
    validate = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(300), nullable=False)
    code = db.Column(db.String(4), nullable=True)
    # task = db.relationship("BusinessOwnerTask", backref="business_owner_backref",
    #                        primaryjoin=lambda: BusinessOwner.id == BusinessOwnerTask.business_owner_id)
    reg_id = db.Column(db.String(200), nullable=True)
    # calendars = db.relationship("Calendar", backref="business_owner_calendar_backref", lazy='dynamic',
    #                             primaryjoin=lambda: BusinessOwner.id == Calendar.business_owner_id)
    lat = db.Column(DOUBLE_PRECISION())
    lng = db.Column(DOUBLE_PRECISION())
    geom = db.Column(Geometry('POINT', srid=Keys.SRID_VALUE))
    flags = db.Column(db.JSON, default={Keys.ACTIVATION_STATUS: True})

    def __repr__(self):
        return '<BusinessOwner %r>' % self.name

    def add(self, db_connection):
        result = None
        try:
            hashed = BusinessOwners.generate_hash_password(self.password)
            self.password = hashed
            db_connection.session.add(self)
            db_connection.session.commit()
            logger.info('Add new business owner. User id: %s', self.id)
            params = {Keys.USER_ID: self.id}
            success = SuccessAddNewUser(status=200, message=MessagesKeys.SUCCESS_ADD_NEW_USER, params=params)
            result = True, success
        except:
            db_connection.session.rollback()
            result = db_error_message(logger)
        return result

    def is_registered(self):
        count = BusinessOwners.query.filter_by(phone_number=self.phone_number).count()
        if not count == 0:
            return True
        return False

    def is_valid(self):
        count = BusinessOwners.query.filter_by(phone_number=self.phone_number, validate=True).count()
        if count == 0:
            return False
        return True

    def is_invalid(self):
        count = BusinessOwners.query.filter_by(phone_number=self.phone_number, validate=False).count()
        if count == 0:
            return False
        return True

    def update(self, db_connection, data):
        result = None
        try:
            BusinessOwners.query.filter_by(phone_number=self.phone_number).update(data)
            iws = BusinessOwners.query.filter_by(phone_number=self.phone_number).first()
            self.id = iws.id
            db_connection.session.commit()
            logger.info('update user. ID: %s' % self.id)
            params = {Keys.USER_ID: self.id}
            success = SuccessUpdate(status=200, message=MessagesKeys.SUCCESS_UPDATE, params=params)
            result = True, success
        except InvalidRequestError as error:
            result = db_error_message(logger)
            db_connection.session.rollback()

        except:
            result = db_error_message(logger)
            db_connection.session.rollback()
        return result

    def is_valid_business_owner_id(self):
        count = BusinessOwners.query.filter_by(id=self).count()
        if count == 0:
            return False
        return True

    #TODO delete
    @staticmethod
    def find(limit=1, **kwargs):
        res = None
        try:
            res = True, BusinessOwners.query.filter_by(**kwargs).limit(limit).all()
        except:
            res = db_error_message(logger)
        return res

    def find_user_by_phone_number(self):
        pass

    @staticmethod
    def generate_hash_password(password):
        return pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)

    #TODO delete
    @staticmethod
    def query_iws(search_parameter):
        query = BusinessOwners.query_builder(search_parameter)
        try:
            business_owners = query.all()
            ids = set()
            for business_owner in business_owners:
                ids.add(business_owner[1].id)

            matched_business_owners = BusinessOwners.query.filter(BusinessOwners.id.in_(ids)).all()

            return True, matched_business_owners
        except:
            return db_error_message(logger)

    #TODO delete
    @staticmethod
    def query_builder(search_parameter):
        query = db.session.query(BusinessOwnerTask, BusinessOwners, ServiceGradeType) \
            .join(ServiceGradeType, BusinessOwnerTask.services_id == ServiceGradeType.id) \
            .join(BusinessOwners, BusinessOwners.id == BusinessOwnerTask.business_owner_id) \
            .filter(ServiceGradeType.service_grade_id == search_parameter.service_grade)

        if len(search_parameter.name) > 0:
            query = query.filter(BusinessOwners.name == search_parameter.name)
        if len(search_parameter.service_types) > 0:
            query = query.filter(ServiceGradeType.service_type_id.in_(search_parameter.service_types))
        if len(search_parameter.region) > 0:
            polygon = BusinessOwners.polygon_maker(search_parameter.region)
            query = query.filter(
                func.ST_Contains(
                    func.ST_GeomFromText(
                        polygon,
                        Keys.SRID_VALUE), BusinessOwners.geom))
        return query

    #TODO delete
    @staticmethod
    def load_business_owner(business_owner_id):
        return BusinessOwners.query. \
            add_columns(BusinessOwners.name, BusinessOwners.reg_id). \
            filter(BusinessOwners.id == business_owner_id). \
            first()

    @staticmethod
    def query_builder2(search_parameter):
        """
        polygon( lng  lat)
        :param search_parameter:
        :return:
        """
        polygon = BusinessOwners.polygon_maker(search_parameter.region)
        query = db.session.query(BusinessOwners).filter(
            func.ST_Contains(
                func.ST_GeomFromText(
                    polygon,
                    Keys.SRID_VALUE), BusinessOwners.geom))

        return query


    # TODO delete
    @staticmethod
    def polygon_maker(polygons):
        polygs = []
        for polygon in polygons:
            polyg = ""
            for point in polygon:
                polyg += str(point[Keys.LONGITUDE]) + " " + str(point[Keys.LATITUDE]) + " , "
            last_comma = polyg.rfind(',')
            polyg = polyg[:last_comma]
            polygs.append(polyg)

        pol_str = ""
        for pol in polygs:
            pol_str += "( " + pol + " ) ,"

        last_comma = pol_str.rfind(',')
        pol_str = pol_str[:last_comma]

        pol_str = 'MULTIPOLYGON((' + pol_str + '))',

        return pol_str

    #TODO delete
    @staticmethod
    def update_by_id(id, db_connection, data):
        result = None
        try:
            BusinessOwners.query.filter_by(id=id).update(data)
            db_connection.session.commit()
            logger.info('update user. ID: %s' % id)
            params = {Keys.USER_ID: id}
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

    #TODO delete
    @staticmethod
    def update_lng_lat(id, lng, lat, db_connection):
        geom = 'SRID=' + str(Keys.SRID_VALUE) + ';POINT(' + str(lng) + " " + str(lat) + ')'
        data = {Keys.LAT: lat, Keys.LNG: lng, Keys.GEOM: geom}
        return BusinessOwners.update_by_id(id, db_connection, data)

    @staticmethod
    def update_reg_id(phone_number, reg_id, db_connection):
        business_owner = BusinessOwners(phone_number=phone_number)
        data = {Keys.REG_ID: reg_id}
        update_result = business_owner.update(db_connection, data)
        return update_result
