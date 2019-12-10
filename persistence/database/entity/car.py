from sqlalchemy.exc import InvalidRequestError, IntegrityError

from app import db, global_logger
from core.messages.translator.messages_keys import MessagesKeys
from core.result.success.success_add_new_car import SuccessAddNewCar
from core.result.success.success_delete_car import SuccessDeleteNewCar
from core.result.success.success_list_cars import SuccessListCars
from core.result.success.success_update import SuccessUpdate
from core.validation.helpers import db_error_message
from persistence.database.entity.auto_model import AutoModel
from persistence.database.entity.auto_type import AutoType
from persistence.database.entity.base import BaseMixin
from persistence.database.entity.car_color import CarColor
from persistence.database.entity.user.car_owner import CarOwner
from core.result import Result

logger = global_logger


class Car(BaseMixin, db.Model):
    __tablename__ = 'cars'
    current_kilometer = db.Column(db.Integer, nullable=False)
    vin_number = db.Column(db.String(17), unique=True, nullable=True)  # shomare shasi
    plate_number = db.Column(db.String(11), unique=True ,nullable=False)  # shomare pelak
    deleted = db.Column(db.Boolean, default=False)
    car_owner_id = db.Column(db.Integer, db.ForeignKey('car_owners.id'))
    car_owner_ = db.relationship(CarOwner)

    color_id = db.Column(db.Integer, db.ForeignKey('colors.id'), nullable=True)
    colors = db.relationship(CarColor)

    auto_model_id = db.Column(db.Integer, db.ForeignKey('auto_models.id'))
    auto_models = db.relationship("AutoModel", backref=db.backref("cars"))

    auto_type_id = db.Column(db.Integer, db.ForeignKey('auto_types.id'))
    auto_type_ = db.relationship('AutoType')

    def __repr__(self):
        return '<Car %r>' % self.plate_number

    def add(self, db_connection, car_owner_id):
        db_connection.session.begin(subtransactions=True)
        result = None
        try:
            user = CarOwner.find(1, id=car_owner_id)
            auto_type = AutoType.query.filter_by(id=self.auto_type_id).limit(1).all()
            auto_model = AutoModel.query.filter_by(id=self.auto_model_id).limit(1).all()
            auto_model[0].cars.extend([self])
            auto_type[0].cars.extend([self])
            user[1][0].cars.extend([self])
            db_connection.session.add(self)
            db_connection.session.commit()
            logger.info('Add new car. Car id: %s', self.id)
            params = {"vin_number": self.vin_number, "plate_number": self.plate_number,
                      "current_kilometer": self.current_kilometer, "color": self.color_id,
                      "auto_type_id": auto_type[0].id, "auto_model_id": auto_model[0].id, "id": self.id}
            success = SuccessAddNewCar(status=200, message=MessagesKeys.SUCCESS_ADD_NEW_CAR, params=params)
            result = True, success
        except:
            db_connection.session.rollback()
            result = db_error_message(logger)

        return result

    @staticmethod
    def find(limit=1, **kwargs):
        res = None
        try:
            res = True, Car.query.filter_by(**kwargs).limit(limit).all()
        except:
            res = db_error_message(logger)
        return res

    @staticmethod
    def delete_by_id(db_connection, car_id):
        result = None
        db_connection.session.begin(subtransactions=True)
        try:
            Car.query.filter_by(id=car_id).update({"deleted": True})

            car = Car.find(1, id=car_id)[1][0]
            logger.info('Delete car. Car id: %s', car_id)
            params = {"vin_number": car.vin_number, "plate_number": car.plate_number}
            success = SuccessDeleteNewCar(status=200, message=MessagesKeys.SUCCESS_DELETE_CAR, params=params)
            result = True, success
            db_connection.session.commit()
        except:
            db_connection.session.rollback()
            result = db_error_message(logger)

        return result

    def update(self, db_connection, data):
        result = None
        try:
            Car.query.filter_by(id=self.id).update(data)
            db_connection.session.commit()
            logger.info('update car. ID: %s' % self.id)
            params = {"id": self.id}
            success = SuccessUpdate(status=200, message=MessagesKeys.SUCCESS_UPDATE, params=params)
            result = True, success
        except InvalidRequestError as error:
            result = db_error_message(logger, message='InvalidRequestError')
            db_connection.session.rollback()

        except IntegrityError as error:
            result = db_error_message(logger, message= Result.language.DUPLICATED_CAR)
            db_connection.session.rollback()
        except:
            result = db_error_message(logger)
            db_connection.session.rollback()
        return result

    @staticmethod
    def find_all(user_id, deleted=False):
        res = None
        try:
            list = Car.query. \
                join(AutoType, Car.auto_type_id == AutoType.id). \
                add_columns(Car.vin_number, Car.plate_number, Car.id, AutoType.name, AutoType.id). \
                filter(Car.car_owner_id == user_id). \
                filter(Car.deleted == deleted). \
                all()

            success = SuccessListCars(status=200, message=MessagesKeys.SUCCESS_LIST, params=list)
            res = True, success
        except:
            res = db_error_message(logger, message='InvalidRequestError')
        return res

    @staticmethod
    def load_car(car_id):
        return Car.query. \
            join(AutoType, AutoType.id == Car.auto_type_id). \
            add_columns(AutoType.name). \
            filter(Car.id == car_id).first()
