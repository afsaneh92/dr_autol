class DataBaseConfig(object):
    DB_DIALECT = 'postgresql+psycopg2://'
    USER_NAME = 'postgres'
    PASSWORD = 'postgres'
    SERVER_ADDRESS = 'localhost'
    PORT = '5432'
    DATABASE_NAME = 'dr-autol-test'

    @staticmethod
    def generate_database_uri():
        return DataBaseConfig.DB_DIALECT + DataBaseConfig.USER_NAME + ':' + DataBaseConfig.PASSWORD + '@' \
               + DataBaseConfig.SERVER_ADDRESS + ':' + DataBaseConfig.PORT + '/' + DataBaseConfig.DATABASE_NAME


    @staticmethod
    def generate_engine_uri():
        return DataBaseConfig.DB_DIALECT + DataBaseConfig.USER_NAME + ':' + DataBaseConfig.PASSWORD + '@' \
               + DataBaseConfig.SERVER_ADDRESS + ':' + DataBaseConfig.PORT
