from sqlalchemy import func

from app import db, global_logger
from core.messages.keys import Keys
from core.validation.helpers import db_error_message
from persistence.database.entity.business_owner_task import BusinessOwnerTaskCarWash, BusinessOwnerTask
from persistence.database.entity.service_definition import ServicesDefinition
from persistence.database.entity.user.auto_service import AutoServiceBusinessOwner
from persistence.database.entity.user.business_owner import BusinessOwner
from persistence.database.entity.user.car_wash import CarWashBusinessOwner
from persistence.database.entity.user.user import User

logger = global_logger


class SearchBusinessOwner:

    @staticmethod
    def query_iws(search_parameter):
        query = SearchBusinessOwner.query_builder(search_parameter)
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
        if search_parameter.service_category == 'AutoService':
            classTask = BusinessOwnerTask
            ownerType = AutoServiceBusinessOwner
        else:
            classTask = BusinessOwnerTaskCarWash
            ownerType = CarWashBusinessOwner

        query = db.session.query(classTask, ownerType, ServicesDefinition) \
            .join(ServicesDefinition, classTask.service_definition_id == ServicesDefinition.id) \
            .join(ownerType, ownerType.id == classTask.business_owner_id) \
            .filter(ServicesDefinition.service_grade == search_parameter.service_grade) \
            .filter(
            ServicesDefinition.service_category == search_parameter.service_category)  # TODO search_parameter.service_category
        # TODO add activation to search  # search_parameter.service_grade
        # .filter(cast(BusinessOwners.flags['activation'], String) == cast('true', String))
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
