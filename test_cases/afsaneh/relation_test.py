from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    type = Column(String(50))

    def __init__(self, id=None, name=None, type=None):
        self.id = id
        self.name = name
        self.type = type

    __mapper_args__ = {
        'polymorphic_identity': 'employee',
        'polymorphic_on': type
    }


class Engineer(Employee):
    __tablename__ = 'engineer'
    id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
    engineer_name = Column(String(30))

    __mapper_args__ = {
        'polymorphic_identity': 'engineer',
    }


class Manager(Employee):
    __tablename__ = 'manager'
    id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
    manager_name = Column(String(30))

    def __init__(self, id=None, manager_name=None):
        self.id = id
        self.manager_name = manager_name

    __mapper_args__ = {
        'polymorphic_identity': 'manager',
    }

manager1 = Manager(id=22, manager_name='sdssd', name='hashse', type='manager')
manager2 = Manager(id=28, manager_name='sdkkssd', name='hasehs', type='manager')
manager3 = Manager(id=27, manager_name='sjjssd', name='hashs', type='manager')

class User(Base):

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))

    # association proxy of "user_keywords" collection
    # to "keyword" attribute
    keywords = association_proxy('user_keywords', 'keyword')

    def __init__(self, name):
        self.name = name


class Keyword(Base):
    __tablename__ = 'keyword'
    id = Column(Integer, primary_key=True)
    keyword = Column(String(64))

    users = association_proxy('keyword_users', 'user', creator=lambda user: UserKeyword(user=user))

    def __init__(self, keyword):
        self.keyword = keyword

    def __repr__(self):
        return 'Keyword(%s)' % repr(self.keyword)


class UserKeyword(Base):
    __tablename__ = 'user_keyword'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    keyword_id = Column(Integer, ForeignKey('keyword.id'), primary_key=True)
    special_key = Column(String(50))

    # bidirectional attribute/collection of "user"/"user_keywords"
    user = relationship(User, backref=backref("user_keywords"))

    # reference to the "Keyword" object
    keyword = relationship(Keyword, backref=backref("keyword_users"))

    def __init__(self, keyword=None, user=None, special_key=None):
        self.user = user
        self.keyword = keyword
        self.special_key = special_key


if __name__ == "__main__":
    engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/proxydb')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    user = User('log')
    kermit = User('kermit')
    piggy = User('piggy')
    keyword = Keyword('new_from_blammo')
    UserKeyword(keyword, kermit, "there is a place over the rainbow")
    UserKeyword(keyword, piggy, "there is a place over the rainbow")
    for kw in (keyword, Keyword('its_big')):
        UserKeyword(kw, user, special_key="Hello there")

    UserKeyword(Keyword('its_wood'), piggy, special_key='the special key')
    session.add(kermit)
    session.add(user)
    session.add(keyword)
    session.commit()

    for user in keyword.users:
        print user.keywords
