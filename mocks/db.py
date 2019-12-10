class Session:
    name = ""

    def add(self, obj):
        self.name = ""
        print("added function to database")

    def commit(self):
        print("commit function to database")

    def rollback(self):
        print("rollback function to database")

    def update(self):
        print("updated function to database")

    def __init__(self):
        print("")


class DBMock:
    session = Session()

    def __init__(self):
        # self.session = Session()
        pass


class MyClass:

    def method(self):
        return 'instance method called', self

    @classmethod
    def classmethod(cls):
        return 'class method called', cls

    @staticmethod
    def staticmethod():
        return 'static method called'
