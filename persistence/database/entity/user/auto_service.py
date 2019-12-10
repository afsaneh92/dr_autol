from abc import abstractmethod
from datetime import timedelta, datetime, date

import xlrd
from sqlalchemy import func
from sqlalchemy.exc import InvalidRequestError

from app import db, global_logger
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result.failure.list_is_empty import EmptyList
from core.result.failure.more_than_allowed_credit import MoreThanAllowed
from core.result.failure.sheet_is_empty import EmptySheet
from core.result.success.list_of_allowed_and_rest_credit import ListOfAllowedAndUsedCredit
from core.result.success.success_update import SuccessUpdate
from core.validation.helpers import db_error_message, read_data_from_excel_file, special_time
from persistence.database.entity.business_owner_task import BusinessOwnerTask
from persistence.database.entity.calendar import Calendar
from persistence.database.entity.service_definition import ServicesDefinition
from persistence.database.entity.supplier_status import SupplierStatus
from persistence.database.entity.user.business_owner import BusinessOwner
from persistence.database.entity.user.user import User
from persistence.database.entity.order_items import OrderItem

logger = global_logger


class AutoServiceBusinessOwner(BusinessOwner):
    __tablename__ = 'auto_service_business_owners'
    id = db.Column(db.Integer, db.ForeignKey('business_owners.id'), primary_key=True)
    task = db.relationship("BusinessOwnerTask", backref="auto_service_task",
                           primaryjoin=lambda: AutoServiceBusinessOwner.id == BusinessOwnerTask.business_owner_id)
    calendars = db.relationship("Calendar", backref="auto_service_calendar", lazy='dynamic',
                                primaryjoin=lambda: AutoServiceBusinessOwner.id == Calendar.business_owner_id)
    order_items = db.relationship("OrderItem")

    __mapper_args__ = {
        'polymorphic_identity': 'AutoServiceBusinessOwner',
    }

    def __repr__(self):
        return '<AutoServiceBusinessOwner %r>' % self.id

    @staticmethod
    @abstractmethod
    def update_by_id(id, db_connection, data):
        result = None
        try:
            db.session.query(BusinessOwner). \
                filter(AutoServiceBusinessOwner.id == BusinessOwner.id). \
                filter(AutoServiceBusinessOwner.id == User.id). \
                filter(AutoServiceBusinessOwner.id == id). \
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
        query = AutoServiceBusinessOwner.query_builder(search_parameter)
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
        query = db.session.query(BusinessOwnerTask, AutoServiceBusinessOwner, ServicesDefinition) \
            .join(ServicesDefinition, BusinessOwnerTask.service_definition_id == ServicesDefinition.id) \
            .join(AutoServiceBusinessOwner, AutoServiceBusinessOwner.id == BusinessOwnerTask.business_owner_id) \
            .filter(ServicesDefinition.service_grade == search_parameter.service_grade) \
            .filter(ServicesDefinition.service_category == 'AutoService')
        # TODO add activation to search
        # .filter(cast(BusinessOwners.flags['activation'], String) == cast('true', String))

        if len(search_parameter.name) > 0:
            query = query.filter(User.name == search_parameter.name)
        if len(search_parameter.service_types) > 0:
            query = query.filter(ServicesDefinition.service_type_id.in_(search_parameter.service_types))
        if len(search_parameter.region) > 0:
            polygon = AutoServiceBusinessOwner.polygon_maker(search_parameter.region)
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

    @staticmethod
    def order_items_modified_and_done_in_special_time(business_owner_id, before, after):
        try:
            orders_in_special_time = []
            done_status_id = SupplierStatus.query.filter(SupplierStatus.name == Keys.BUY_DONE). \
                with_entities(SupplierStatus.id).first()
            done_order_items = OrderItem.query.filter(OrderItem.supplier_status_id.in_(done_status_id)). \
                filter(OrderItem.business_owner_id == business_owner_id).all()
            for order_item in done_order_items:
                if before <= order_item.orders.date_modified <= after:
                    orders_in_special_time.append(order_item)
            res = True, orders_in_special_time
        except:
            res = db_error_message(logger)
            db.session.rollback()
        return res

    @staticmethod
    def read_allow_credit_from_excel(sheet, business_owner_phone_number):
        allow_credit_in_special_time = []
        fail_list = []
        if sheet.nrows == 0 or sheet.ncols == 0:
            return False, EmptySheet(status=404, message=MessagesKeys.SHEET_IS_EMPTY, params=None)
        number_of_cols = sheet.ncols
        cols = (number_of_cols + 2)
        for value in range(1,cols ):
            row_value = sheet.row_values(value)
            if business_owner_phone_number == row_value[0]:
                allow_credit_in_special_time.append(row_value[1])
            else:
                fail_list.append(row_value)
        if len(allow_credit_in_special_time) <= 0:
            return False, EmptyList(status=404, message=MessagesKeys.FAIL_LIST, params=None)
        return True, allow_credit_in_special_time
