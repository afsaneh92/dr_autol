from sqlalchemy import create_engine

from config import DataBaseConfig

if __name__ == "__main__":
    engine = create_engine(DataBaseConfig.generate_engine_uri())
    conn = engine.connect()
    conn.execute("commit")
    conn.execute('DROP DATABASE IF EXISTS "' + DataBaseConfig.DATABASE_NAME + '"')
    conn.execute("commit")
    print "Database '" + DataBaseConfig.DATABASE_NAME+ "' dropped ..."
    conn.execute('CREATE DATABASE "' + DataBaseConfig.DATABASE_NAME + '"'
    """
        WITH 
        OWNER = postgres
        ENCODING = 'UTF8'
        CONNECTION LIMIT = -1;
    """)
    conn.close()
    print "New database created ..."

    database = create_engine(DataBaseConfig.generate_database_uri())
    conn = database.connect()
    conn.execute("commit")
    conn.execute("""
        CREATE EXTENSION postgis;
    """)
    conn.close()
    print "extension postgis created."
