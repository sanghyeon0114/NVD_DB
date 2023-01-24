import psycopg2
import os

from format.item import Item
import dateutil.parser

from query.create import *
from query.insert import *

from query.query import Query


class Database:
    """Database setting class"""

    connect = None
    cursor = None

    @staticmethod
    def print(message: str) -> None:
        """print 'database class' message function"""
        print("[database]", message)

    @staticmethod
    def connect_database():
        """Connect to database function"""
        if Database.connect is None:
            try:
                Database.connect = psycopg2.connect(
                    host=os.environ.get('DB_HOST'),
                    dbname=os.environ.get('DB_NAME'),
                    user=os.environ.get('DB_USER'),
                    port=int(os.environ.get('DB_PORT')),
                    password=os.environ.get('DB_PASSWORD')
                )

                Database.cursor = Database.connect.cursor()

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
            Database.connect.close()
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
        Database.connect.commit()

    @ staticmethod
    def init():
        """Create database cursor and table function"""
        if Database.connect is None:
            Database.print("Database is not connected")
        try:

            Database.execute(Query.create_cve)
            Database.execute(Query.create_problemtypes)
            Database.execute(Query.create_references)
            Database.execute(Query.create_descriptions)
            Database.execute(Query.create_configuration_nodes)
            Database.execute(Query.create_cpe_match)
            Database.execute(Query.create_cpe_metadata)
            Database.execute(Query.create_cpe_name)
            Database.execute(Query.create_impact)

            Database.commit()
        except psycopg2.Error as err:
            Database.print("create Table error : ")
            for msg in err.args:
                Database.print(msg)

    @staticmethod
    def insert_cve(item: Item):
        """Create database cursor and table function"""
        if Database.connect is None:
            Database.print("Database is not connected")
        try:
            Database.execute(Query.insert_cve, [item.cve['data_type'], item.cve['data_format'], item.cve['data_version'], item.cve['CVE_data_meta']['ID'],
                                                item.cve['CVE_data_meta']['ASSIGNER'], item.configurations['CVE_data_version'], dateutil.parser.parse(item.publishedDate), dateutil.parser.parse(item.lastModifiedDate)])

            Database.commit()

            ##################################################################################
            cveId = Database.getLastCveId()
            ##################################################################################
            problemtypes = item.cve['problemtype']['problemtype_data'][0]['description']

            for problemtype in problemtypes:
                Database.execute(Query.insert_problemtypes, [
                    cveId, problemtype['lang'], problemtype['value']])

            Database.commit()
            ##################################################################################
            references = item.cve['references']['reference_data']
            for reference in references:
                pass
        except psycopg2.Error as err:
            Database.print("execute sql error : ")
            for msg in err.args:
                Database.print(msg)

    @staticmethod
    def getLastCveId():
        return Database.execute(Query.get_last_cve_id)
