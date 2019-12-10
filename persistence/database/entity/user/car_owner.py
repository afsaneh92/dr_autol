from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import InvalidRequestError

from app import db, global_logger
from core.messages.translator.messages_keys import MessagesKeys
from core.result.success.success_update import SuccessUpdate
from core.validation.helpers import db_error_message
from persistence.database.entity.user.user import User

logger = global_logger


class CarOwner(User):
    __tablename__ = 'car_owners'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    cars = db.relationship("Car", backref="car_owner_backref", lazy='dynamic',
                           primaryjoin="CarOwner.id == Car.car_owner_id")
    __mapper_args__ = {
        'polymorphic_identity': 'CarOwner',
    }

    def __repr__(self):
        return '<CarOwner %r>' % self.name

    # #TODO delete
    # def add(self, db_connection):
    #     result = None
    #     try:
    #         hashed = CarOwners.generate_hash_password(self.password)
    #         self.password = hashed
    #         db_connection.session.add(self)
    #         db_connection.session.commit()
    #         logger.info('Add new user. User id: %s', self.id)
    #         params = {"user_id": self.id}
    #         success = SuccessAddNewUser(status=200, message=MessagesKeys.SUCCESS_ADD_NEW_USER, params=params)
    #         result = True, success
    #     except:
    #         db_connection.session.rollback()
    #         result = db_error_message(logger)

        return result

    def update(self, db_connection, data):
        result = None
        try:
            User.query.filter_by(phone_number=self.phone_number).update(data)
            user = CarOwner.query.filter_by(phone_number=self.phone_number).first()
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
    def find(limit=1, **kwargs):
        res = None
        try:
            res = True, CarOwner.query.filter_by(**kwargs).limit(limit).all()
        except:
            res = db_error_message(logger, message='InvalidRequestError')
        return res

    def find_user_by_phone_number(self):
        pass

    @staticmethod
    def load_car_owner(car_owner_id):
        return CarOwner.query. \
            filter(CarOwner.id == car_owner_id).first()

    @staticmethod
    def load_car_owner2(car_owner_id):
        return User.query. \
            filter(User.id == car_owner_id).first()


    @staticmethod
    def update_by_id(id, db_connection, data):
        pass
