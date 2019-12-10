from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import InvalidRequestError

from app import db, global_logger
from core.messages.translator.messages_keys import MessagesKeys
from core.result.success.success_add_new_user import SuccessAddNewUser
from core.result.success.success_update import SuccessUpdate
from core.validation.helpers import db_error_message
from persistence.database.entity.user.user import User

logger = global_logger


class Admin(User):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    last_name = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(11), default="pending")

    __mapper_args__ = {
        'polymorphic_identity':'Admin',
    }