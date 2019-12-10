from flask import session


class SessionManager(object):

    @staticmethod
    def is_key_exist(key):
        if key not in session:
            result = False
        else:
            result = True

        return result

    @staticmethod
    def add_new_key(key, value):
        session[key] = value

    @staticmethod
    def update_key(key, new_value):
        session[key] = new_value

    @staticmethod
    def retrieve_session_value_by_key(key):
        return session[key]

    @staticmethod
    def pop_all():
        for key in session.keys():
            session.pop(key)

    @staticmethod
    def pop(key):
        session.pop(key)

    @staticmethod
    def get_all_session():
        return session