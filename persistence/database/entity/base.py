import datetime
import jwt
from sqlalchemy.ext.declarative import declared_attr
from app import db, app


class BaseMixin(object):

    @declared_attr
    def id(self):
        return db.Column(db.Integer, primary_key=True, autoincrement=True)

    @declared_attr
    def date_created(self):
        return db.Column(db.DateTime, default=db.func.current_timestamp())

    @declared_attr
    def date_modified(self):
        return db.Column(db.DateTime, default=db.func.current_timestamp(),
                         onupdate=db.func.current_timestamp())


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
