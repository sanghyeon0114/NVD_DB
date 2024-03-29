import psycopg2
import os
import logging
import traceback

from .create_table import *
from .delete_table import *


class Database:
    """Database setting class"""

    db = None
    cursor = None

    @staticmethod
    def print(message: str) -> None:
        """print 'database class' message function"""
        logging.info("[database]", message)

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

            except psycopg2.Error:
                Database.print(traceback.format_exc())
        else:
            Database.print("Already connected database")

    @staticmethod
    def close():
        """Close to database function"""
        try:
            Database.db.close()
            Database.cursor.close()
        except psycopg2.Error:
            Database.print(traceback.format_exc())

    @staticmethod
    def execute(sql: str, columns: list = None):
        '''
        query execute function.
        '''
        Database.cursor.execute(sql, columns)

    @staticmethod
    def commit():
        Database.db.commit()

    @staticmethod
    def init():
        """Create database cursor and table function"""
        if Database.db is None:
            Database.print("Database is not connected")
        try:
            ######################## table ########################
            Database.execute(create_cpe)
            Database.execute(create_nvd_cpe_match)
            Database.execute(create_nvd_cpe23)
            Database.execute(create_cve)
            Database.execute(create_configuration_nodes)
            Database.execute(create_cpe_match)
            Database.execute(create_impact)

            Database.commit()

            ######################## index ########################
            Database.execute("""
            CREATE INDEX cve_references_idx ON cve USING gin(references_tsv)
            """)
            Database.execute("""
            CREATE INDEX cve_description_idx ON cve USING gin(description_tsv)
            """)

            Database.execute("""
            CREATE INDEX cpe_references_idx ON cpe USING gin(titles_tsv)
            """)
            Database.execute("""
            CREATE INDEX cpe_description_idx ON cpe USING gin(references_tsv)
            """)

            Database.commit()
        except psycopg2.Error:
            Database.print(traceback.format_exc())

    @staticmethod
    def delete_tables():
        """Create database cursor and table function"""
        if Database.db is None:
            Database.print("Database is not connected")
        try:
            ######################## index ########################
            Database.execute("""DROP INDEX IF EXISTS cve_references_idx;""")
            Database.execute("""DROP INDEX IF EXISTS cve_description_idx;""")

            Database.execute("""DROP INDEX IF EXISTS cpe_references_idx;""")
            Database.execute("""DROP INDEX IF EXISTS cpe_description_idx;""")

            Database.commit()

            ######################## table ########################
            Database.execute(delete_impact)
            Database.execute(delete_cpe_match)
            Database.execute(delete_configuration_nodes)
            Database.execute(delete_cve)
            Database.execute(delete_nvd_cpe23)
            Database.execute(delete_nvd_cpe_match)
            Database.execute(delete_cpe)

            Database.commit()

        except psycopg2.Error:
            Database.print(traceback.format_exc())

    @staticmethod
    def reload_cve():
        """reload cve table function"""
        if Database.db is None:
            Database.print("Database is not connected")
        try:
            Database.execute(delete_impact)
            Database.execute(delete_cpe_match)
            Database.execute(delete_configuration_nodes)
            Database.execute(delete_cve)

            Database.execute(create_cve)
            Database.execute(create_configuration_nodes)
            Database.execute(create_cpe_match)
            Database.execute(create_impact)

            Database.commit()
        except psycopg2.Error:
            Database.print(traceback.format_exc())

    @staticmethod
    def reload_cpe():
        """reload cve table function"""
        if Database.db is None:
            Database.print("Database is not connected")
        try:
            Database.execute(delete_cpe)
            Database.execute(create_cpe)

            Database.commit()
        except psycopg2.Error:
            Database.print(traceback.format_exc())

    @staticmethod
    def reload_nvd_cpe_match():
        """reload cve table function"""
        if Database.db is None:
            Database.print("Database is not connected")
        try:
            Database.execute(delete_cpe_match)
            Database.execute(delete_nvd_cpe23)
            Database.execute(delete_nvd_cpe_match)

            Database.execute(create_nvd_cpe_match)
            Database.execute(create_nvd_cpe23)
            Database.execute(create_cpe_match)
            Database.commit()
        except psycopg2.Error:
            Database.print(traceback.format_exc())
