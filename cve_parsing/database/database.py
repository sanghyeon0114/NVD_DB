import psycopg2
import os

from .create_table import *


class Database:
    """Database setting class"""

    db = None
    cursor = None

    @staticmethod
    def print(message: str) -> None:
        """print 'database class' message function"""
        print("[database]", message)

    @staticmethod
    def connect():
        """Connect to database function"""
        if Database.db is None:
            try:
                Database.db = psycopg2.connect(
                    host=os.environ.get('DB_HOST'),
                    dbname=os.environ.get('DB_NAME'),
                    user=os.environ.get('DB_USER'),
                    port=int(os.environ.get('DB_PORT')),
                    password=os.environ.get('DB_PASSWORD')
                )

                Database.cursor = Database.db.cursor()

            except psycopg2.Error as err:
                Database.print("Database connect error : ")
                for msg in err.args:
                    Database.print(msg)
        else:
            Database.print("Already connected database")

    @staticmethod
    def close():
        """Close to database function"""
        try:
            Database.db.close()
            Database.cursor.close()
        except psycopg2.Error as err:
            Database.print("Database close error : ")
            for msg in err.args:
                Database.print(msg)

    @staticmethod
    def execute(sql: str, columns: list = None):
        '''
        query execute function.
        '''
        Database.cursor.execute(sql, columns)

    @staticmethod
    def commit():
        Database.db.commit()

    @ staticmethod
    def init():
        """Create database cursor and table function"""
        if Database.db is None:
            Database.print("Database is not connected")
        try:

            Database.execute(create_cve)
            Database.execute(create_problemtypes)
            Database.execute(create_references)
            Database.execute(create_descriptions)
            Database.execute(create_configuration_nodes)
            Database.execute(create_cpe_match)
            Database.execute(create_impact)

            Database.commit()
        except psycopg2.Error as err:
            Database.print("create Table error : ")
            for msg in err.args:
                Database.print(msg)
