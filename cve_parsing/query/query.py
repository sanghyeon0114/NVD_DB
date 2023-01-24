import psycopg2

from database.database import Database
from database.create_table import *

from .insert import *
from .select import *

from format.item import Item
import dateutil.parser


class Query(Database):
    insert_cve: str = None
    insert_problemtype_data: str = None
    insert_reference_data: str = None
    insert_description_data: str = None

    get_last_cve_id: str = None

    @staticmethod
    def loadQuery():

        Query.insert_cve = insert_cve
        Query.insert_problemtype_data = insert_problemtype_data
        Query.insert_reference_data = insert_reference_data
        Query.insert_description_data = insert_description_data

        Query.get_last_cve_id = get_last_cve_id

    @staticmethod
    def insertCve(item: Item):
        """Create database cursor and table function"""
        if Query.db is None:
            Query.print("Database is not connected")
        try:
            Query.execute(Query.insert_cve, [item.cve['data_type'], item.cve['data_format'], item.cve['data_version'], item.cve['CVE_data_meta']['ID'],
                                             item.cve['CVE_data_meta']['ASSIGNER'], item.configurations['CVE_data_version'], dateutil.parser.parse(item.publishedDate), dateutil.parser.parse(item.lastModifiedDate)])

            Query.commit()
            ##################################################################################
            cveId = Query.getLastCveId()
            ##################################################################################
            problemtypes = item.cve['problemtype']['problemtype_data'][0]['description']

            for problemtype in problemtypes:
                Query.execute(Query.insert_problemtype_data, [
                    cveId, problemtype['lang'], problemtype['value']])
            ##################################################################################
            references = item.cve['references']['reference_data']
            for reference in references:
                Query.execute(Query.insert_reference_data, [
                    cveId, reference['url'], reference['name'], reference['refsource'], "{"+','.join(reference['tags'])+"}"])
            ##################################################################################
            description = item.cve['description']['description_data'][0]
            Query.execute(Query.insert_description_data, [
                          cveId, description['lang'], description['value']])

            Query.commit()
        except psycopg2.Error as err:
            Query.print("execute sql error : ")
            for msg in err.args:
                Query.print(msg)

    @staticmethod
    def getLastCveId():
        Query.execute(Query.get_last_cve_id)
        return Query.cursor.fetchone()[0]
