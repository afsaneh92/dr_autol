from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import InvalidRequestError

from app import db, global_logger
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result.success.success_add_new_user import SuccessAddNewUser
from core.result.success.success_update import SuccessUpdate
from core.validation.helpers import db_error_message

logger = global_logger


class CarOwners(db.Model):
    __tablename__ = 'car_ownerss'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(11), unique=True, nullable=False)
    code = db.Column(db.String(4), nullable=True)
    validate = db.Column(db.Boolean, default=False)
    user_type = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    # cars = db.relationship("Car", backref="car_owner_backref", lazy='dynamic',
    #                        primaryjoin="CarOwner.id == Car.car_owner_id")
    cars = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    reg_id = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return '<CarOwner %r>' % self.name

    def add(self, db_connection):
        result = None
        try:
            hashed = CarOwners.generate_hash_password(self.password)
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

    def is_registered(self):
        count = CarOwners.query.filter_by(phone_number=self.phone_number).count()
        if not count == 0:
            return True
        return False

    def is_valid(self):
        count = CarOwners.query.filter_by(phone_number=self.phone_number, validate=True).count()
        if count == 0:
            return False
        return True

    def is_invalid(self):
        count = CarOwners.query.filter_by(phone_number=self.phone_number, validate=False).count()
        if count == 0:
            return False
        return True

    def update(self, db_connection, data):
        result = None
        try:
            CarOwners.query.filter_by(phone_number=self.phone_number).update(data)
            user = CarOwners.query.filter_by(phone_number=self.phone_number).first()
            self.id = user.id
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

    @staticmethod
    def find(limit=1, **kwargs):
        res = None
        try:
            res = True, CarOwners.query.filter_by(**kwargs).limit(limit).all()
        except:
            res = db_error_message(logger, message='InvalidRequestError')
        return res

    def find_user_by_phone_number(self):
        pass

    @staticmethod
    def generate_hash_password(password):
        return pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)

    @staticmethod
    def load_car_owner(car_owner_id):
        return CarOwners.query. \
            filter(CarOwners.id == car_owner_id).first()

    @staticmethod
    def update_reg_id(phone_number, reg_id, db_connection):
        carOwner = CarOwners(phone_number=phone_number)
        data = {Keys.REG_ID: reg_id}
        update_result = carOwner.update(db_connection, data)
        return update_result
