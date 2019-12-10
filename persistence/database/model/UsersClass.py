from core.services.validation_code import *


# db.Model
class Users:
    pass
    id = ""
    name = ""
    email = ""
    password = ""
    user_type = ""
    phone = ""
    code = ""
    is_validate = False

    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(80))
    # email = db.Column(db.String(120), unique=True)
    # password = db.Column(db.String(120))
    # user_type = db.Column(db.String(120))
    # phone = db.Column(db.String(120), unique=True)
    # is_validate = db.Column(db.Boolean)

    def __init__(self, name, phone, password, user_type):
        self.name = name
        self.phone = phone
        self.password = password
        self.user_type = user_type
        self.is_validate = False


# ma.Schema
class UsersSchema:
    class Meta:
        # Fields to expose
        fields = ('username', 'email')


class UsersQuery:

    @staticmethod
    def is_user_exists_and_valid():
        count = db.users.filter(and_(db.users.phone_number == phone_number, db.users.is_validate == True))
        if count == 0:
            return False
        return True

    @staticmethod
    def is_user_exist(phone_number):
        count = db.users.filter(db.users.phone_number == phone_number)
        if count == 0:
            return False
        else:
            return

    @staticmethod
    def is_valid_user_by_phone_number(phone_number):
        """
        search in db to find is this number is registered and has validated.

        :return: Bool
        """
        count = db.users.filter(and_(db.users.phone_number == phone_number, db.users.is_validate == True))
        if count == 1:
            return True

    @staticmethod
    def add_user_to_db(json_details):
        """
        add user to db. User details (name, pass, phone) is in json_details

        :return: Bool
        """
        return True

    def register_user_in_database(self, user, db):
        # user_data = extract_user_info(request)
        # user.name
        # user.password
        # user.user_type
        # user.phone_number
        new_user = Users(user.name, user.phone_number, user.password, user.user_type)
        # new_user = Users(user_data['name'], user_data['phone_number'], user_data['password'], user_data['user_type'])
        try:
            db.session.add(new_user)
            db.session.commit()

        except:
            db.session.rollack()
            return False, "adding new user failed"
        return True, new_user
