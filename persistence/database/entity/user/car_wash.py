from abc import abstractmethod

from sqlalchemy.exc import InvalidRequestError

from app import db, global_logger
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result.success.success_update import SuccessUpdate
from core.validation.helpers import db_error_message
from persistence.database.entity.business_owner_task import BusinessOwnerTaskCarWash
# from persistence.database.entity.calendar import Calendar
from persistence.database.entity.service_definition import ServicesDefinition
from persistence.database.entity.user.business_owner import BusinessOwner
from persistence.database.entity.user.user import User
from sqlalchemy import func, String, cast, Boolean

logger = global_logger


class CarWashBusinessOwner(BusinessOwner):
    __tablename__ = 'car_wash_business_owner_owners'
    id = db.Column(db.Integer, db.ForeignKey('business_owners.id'), primary_key=True)
    task = db.relationship("BusinessOwnerTaskCarWash", backref="auto_service_task",
                           primaryjoin=lambda: CarWashBusinessOwner.id == BusinessOwnerTaskCarWash.business_owner_id)
    # calendars = db.relationship("Calendar", backref="auto_service_calendar", lazy='dynamic',
    #                             primaryjoin=lambda: CarWashBusinessOwner.id == Calendar.business_owner_id)

    __mapper_args__ = {
        'polymorphic_identity': 'CarWashBusinessOwner',
    }

    def __repr__(self):
        return '<CarWashBusinessOwner %r>' % self.id

    def print_me(self):
        return "yahoo!"

    @staticmethod
    @abstractmethod
    def update_by_id(id, db_connection, data):
        result = None
        try:
            db.session.query(BusinessOwner). \
                filter(CarWashBusinessOwner.id == BusinessOwner.id). \
                filter(CarWashBusinessOwner.id == User.id). \
                filter(CarWashBusinessOwner.id == id). \
                update(data, synchronize_session='fetch')
            # AutoServiceBusinessOwner.query.filter_by(id=id).update(data)
            # AutoServiceBusinessOwner.query.filter_by(id=id).update(data)
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

    @staticmethod
    def query_iws(search_parameter):
        query = CarWashBusinessOwner.query_builder(search_parameter)
        try:
            business_owners = query.all()
            ids = set()
            for business_owner in business_owners:
                ids.add(business_owner[1].id)

            matched_business_owners = User.query.filter(User.id.in_(ids)).all()

            return True, matched_business_owners
        except:
            return db_error_message(global_logger)

    @staticmethod
    def query_builder(search_parameter):
        query = db.session.query(BusinessOwnerTaskCarWash, CarWashBusinessOwner, ServicesDefinition) \
            .join(ServicesDefinition, BusinessOwnerTaskCarWash.service_definition_id == ServicesDefinition.id) \
            .join(CarWashBusinessOwner, CarWashBusinessOwner.id == BusinessOwnerTaskCarWash.business_owner_id) \
            .filter(ServicesDefinition.service_grade == search_parameter.service_grade) \
            .filter(ServicesDefinition.service_category == search_parameter.service_category) #TODO search_parameter.service_category
            # TODO add activation to search  # search_parameter.service_grade
            #.filter(cast(BusinessOwners.flags['activation'], String) == cast('true', String))
        # return query

        if len(search_parameter.name) > 0:
            query = query.filter(User.name == search_parameter.name)
        if len(search_parameter.service_types) > 0:
            query = query.filter(ServicesDefinition.service_type_id.in_(search_parameter.service_types))
        if len(search_parameter.region) > 0:
            polygon = CarWashBusinessOwner.polygon_maker(search_parameter.region)
            query = query.filter(
                func.ST_Contains(
                    func.ST_GeomFromText(
                        polygon,
                        Keys.SRID_VALUE), BusinessOwner.geom))
        return query

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
