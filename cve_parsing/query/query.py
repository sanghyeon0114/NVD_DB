import psycopg2
import logging
import traceback
import time

from database.database import Database
from database.create_table import *

from .insert import *
from .select import *

from format.item import Item
import dateutil.parser


class Query(Database):
    # configurations table
    insert_configuration_nodes: str = None
    insert_cpe_match: str = None

    # impact table
    insert_impact: str = None

    # cpe table
    insert_cpe: str = None

    # cpe titles table
    insert_cpe_titles: str = None

    # cpe references table
    insert_cpe_references: str = None

    # nvd cpe match table
    insert_nvd_cpe_match: str = insert_nvd_cpe_match

    # select sql
    get_cve_id: str = None
    get_cpe_id: str = None

    get_last_cve_id: str = None
    get_last_node_id: str = None
    get_last_cpe_id: str = None
    get_last_nvd_cpe_match_id: str = None

    get_cve_count: str = None
    get_cpe_count: str = None
    get_nvd_cpe_match_count: str = None

    @staticmethod
    def loadQuery():

        Query.insert_configuration_nodes = insert_configuration_nodes
        Query.insert_cpe_match = insert_cpe_match

        Query.insert_impact = insert_impact

        Query.insert_cpe = insert_cpe
        Query.insert_cpe_titles = insert_cpe_titles
        Query.insert_cpe_references = insert_cpe_references

        Query.insert_nvd_cpe_match = insert_nvd_cpe_match

        Query.get_cve_id = get_cve_id
        Query.get_cpe_id = get_cpe_id

        Query.get_last_cve_id = get_last_cve_id
        Query.get_last_node_id = get_last_node_id
        Query.get_last_cpe_id = get_last_cpe_id
        Query.get_last_nvd_cpe_match_id = get_last_nvd_cpe_match_id

        Query.get_cve_count = get_cve_count
        Query.get_cpe_count = get_cpe_count
        Query.get_nvd_cpe_match_count = get_nvd_cpe_match_count

    # Overriding
    @staticmethod
    def print(message: str) -> None:
        """print 'query class' message function"""
        print("[Query]", message)

    @staticmethod
    def insertAllCVEData(item: Item):
        '''
            if you want to handle error, plz to handle in this function
        '''
        try:
            cveId = Query.insertCve(item)
            Query.insertConfigurations(item, cveId)
            Query.insertImpact(item, cveId)
            Query.commit()
        except psycopg2.Error:
            day = "[" + time.strftime('%Y-%m-%d %H:%M:%S',
                                      time.localtime(time.time())) + "]"
            logging.info(day + traceback.format_exc())
            quit()

    @staticmethod
    def insertCve(item: Item) -> int:
        """Create cve data function"""

        # cve
        sql = """
            INSERT INTO cve (
                data_type,
                data_format,
                data_version,
                CVE_data_meta_ID,
                CVE_data_meta_ASSIGNER,
                configurations_CVE_data_version,
                publishedDate,
                lastModifiedDate
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
        Query.execute(sql, [item.cve.get('data_type'), item.cve.get('data_format'), item.cve.get('data_version'), item.cve.get('CVE_data_meta').get('ID'),
                                         item.cve.get('CVE_data_meta').get('ASSIGNER'), item.configurations.get('CVE_data_version'), dateutil.parser.parse(item.publishedDate), dateutil.parser.parse(item.lastModifiedDate)])

        cveId = Query.getCveId(item.cve.get('CVE_data_meta').get('ID'))

        # problemtypes
        problemtypes: list = item.cve['problemtype']['problemtype_data'][0]['description']
        problemtype_columns = []
        sql = """
            INSERT INTO problemtype_data (cveId, lang, value) VALUES 
            """
        
        for problemtype in problemtypes:
            sql += "(%s, %s, %s),"
            problemtype_columns.append(cveId)
            problemtype_columns.append(problemtype.get('lang'))
            problemtype_columns.append(problemtype.get('value'))
        
        if len(problemtype_columns) != 0:
            Query.execute(sql[:-1], problemtype_columns)

        # references
        references: list = item.cve['references']['reference_data']

        references_columns = []
        sql = """
            INSERT INTO reference_data (cveId, url, name, refsource, tag) VALUES 
            """
        
        for reference in references:
            sql += "(%s, %s, %s, %s, %s),"
            problemtype_columns.append(cveId)
            problemtype_columns.append(reference.get('url'))
            problemtype_columns.append(reference.get('name'))
            problemtype_columns.append(reference.get('refsource'))
            problemtype_columns.append("{"+','.join(reference.get('tags'))+"}")
        
        if len(references_columns) != 0:
            Query.execute(sql[:-1], references_columns)


        # description
        description: list = item.cve['description']['description_data'][0]
        sql = """
            INSERT INTO description_data (cveId, lang, value) VALUES (%s, %s, %s)
            """
        Query.execute(sql, [
            cveId, description.get('lang'), description.get('value')])

        return cveId

    @staticmethod
    def insertConfigurations(item: Item, cveId: int):
        """Create configurations data function"""
        nodes: list = item.configurations.get('nodes')

        for node in nodes:
            columns = [
                cveId,
                node.get('operator'),
                None
            ]
            Query.execute(Query.insert_configuration_nodes, columns)

            nodeId = Query.getLastNodeId()
            if len(node.get('children')) != 0:
                Query.insertNodeChildren(node.get('children'), cveId, nodeId)

            cpe_match: list = node.get('cpe_match')
            sql = """
                INSERT INTO cpe_match (
                    cveId,
                    nodeId,
                    vulnerable,
                    cpe23Uri,
                    versionStartIncluding,
                    versionEndIncluding,
                    versionStartExcluding,
                    versionEndExcluding,
                    cpe_name
                ) VALUES 
                """
            
            if len(cpe_match) != 0:
                cpe_match_columns = []
                for cpe in cpe_match:
                    cpe23: str = cpe.get('cpe23Uri')
                    sql += "(%s, %s, %s, %s, %s, %s, %s, %s, %s),"
                    cpe_match_columns.append(cveId)
                    cpe_match_columns.append(nodeId)
                    cpe_match_columns.append(cpe.get('vulnerable'))
                    cpe_match_columns.append(cpe23)
                    cpe_match_columns.append(cpe.get('versionStartIncluding'))
                    cpe_match_columns.append(cpe.get('versionEndIncluding'))
                    cpe_match_columns.append(cpe.get('versionStartExcluding'))
                    cpe_match_columns.append(cpe.get('versionEndExcluding'))
                    cpe_match_columns.append("{"+','.join(cpe['cpe_name'])+"}")
                Query.execute(sql, cpe_match_columns)

    @ staticmethod
    def insertNodeChildren(children: list, cveId, nodeId):
        """Create children data in configurations function"""
        for child in children:
            columns = [
                cveId,
                child.get('operator'),
                nodeId
            ]
            Query.execute(Query.insert_configuration_nodes, columns)

            parentId = Query.getLastNodeId()
            if len(child.get('children')) != 0:
                Query.insertNodeChildren(
                    child.get('children'), cveId, parentId)

            cpe_match: list = child.get('cpe_match')
            sql = """
                INSERT INTO cpe_match (
                    cveId,
                    nodeId,
                    vulnerable,
                    cpe23Uri,
                    versionStartIncluding,
                    versionEndIncluding,
                    versionStartExcluding,
                    versionEndExcluding,
                    cpe_name
                ) VALUES 
                """
            
            if len(cpe_match) != 0:
                cpe_match_columns = []
                for cpe in cpe_match:
                    cpe23: str = cpe.get('cpe23Uri')
                    sql += "(%s, %s, %s, %s, %s, %s, %s, %s, %s),"
                    cpe_match_columns.append(cveId)
                    cpe_match_columns.append(nodeId)
                    cpe_match_columns.append(cpe.get('vulnerable'))
                    cpe_match_columns.append(cpe23)
                    cpe_match_columns.append(cpe.get('versionStartIncluding'))
                    cpe_match_columns.append(cpe.get('versionEndIncluding'))
                    cpe_match_columns.append(cpe.get('versionStartExcluding'))
                    cpe_match_columns.append(cpe.get('versionEndExcluding'))
                    cpe_match_columns.append("{"+','.join(cpe['cpe_name'])+"}")
                Query.execute(sql, cpe_match_columns)

    @ staticmethod
    def insertImpact(item: Item, cveId: int):
        """Create impact data function"""
        impact = item.impact

        if impact == None:
            return

        columns = [
            cveId,
            impact.get('baseMetricV3.cvssV3.version'),
            impact.get('baseMetricV3.cvssV3.vectorString'),
            impact.get('baseMetricV3.cvssV3.baseScore'),
            impact.get('baseMetricV3_cvssV3_baseSeverity'),
            impact.get('baseMetricV3.exploitabilityScore'),
            impact.get('baseMetricV3.impactScore'),
            impact.get('baseMetricV2.cvssV2.version'),
            impact.get('baseMetricV2.cvssV2.vectorString'),
            impact.get('baseMetricV2.cvssV2.baseScore'),
            impact.get('baseMetricV2.severity'),
            impact.get('baseMetricV2.exploitabilityScore'),
            impact.get('baseMetricV2.impactScore'),
            impact.get('baseMetricV2.acInsufInfo'),
            impact.get('baseMetricV2.obtainAllPrivilege'),
            impact.get('baseMetricV2.obtainUserPrivilege'),
            impact.get('baseMetricV2.obtainOtherPrivilege'),
            impact.get('baseMetricV2.userInteractionRequired')
        ]

        Query.execute(Query.insert_impact, columns)

    @ staticmethod
    def insertAllCPEData(cpe):
        '''
            if you want to handle error, plz to handle in this function
        '''
        try:
            cpeId = Query.insertCpe(cpe)
            Query.insertCpeTitles(cpe, cpeId)
            Query.insertCpeReferences(cpe, cpeId)
            Query.commit()
        except psycopg2.Error:
            day = "[" + time.strftime('%Y-%m-%d %H:%M:%S',
                                      time.localtime(time.time())) + "]"
            logging.info(day + traceback.format_exc())
            quit()

    @ staticmethod
    def insertCpe(cpe: dict):
        """Create cpe data function"""
        cpe22 = cpe.get('@name')
        cpe23: str = cpe.get('cpe-23:cpe23-item').get('@name')

        columns = [
            cpe22,
            cpe23
        ]
        Query.execute(Query.insert_cpe, columns)

        cpeId = Query.getCpeId(cpe23)
        return cpeId

    @staticmethod
    def insertCpeTitles(cpe, cpeId):
        titles = cpe.get('title')
        if titles == None:
            return

        if isinstance(titles, list):
            for title in titles:
                columns = [
                    cpeId,
                    title.get('#text'),
                    title.get('@xml:lang')
                ]
                Query.execute(Query.insert_cpe_titles, columns)
        else:
            columns = [
                cpeId,
                titles.get('#text'),
                titles.get('@xml:lang')
            ]
            Query.execute(Query.insert_cpe_titles, columns)

    @staticmethod
    def insertCpeReferences(cpe, cpeId):
        """Create cpe references data function"""
        references = cpe.get('references')
        if references == None:
            return

        references = references.get('reference')

        if isinstance(references, list):
            for reference in references:
                columns = [
                    cpeId,
                    reference.get('#text'),
                    reference.get('@href')
                ]
                Query.execute(Query.insert_cpe_references, columns)
        else:
            columns = [
                cpeId,
                references.get('#text'),
                references.get('@href')
            ]
            Query.execute(Query.insert_cpe_references, columns)

    @staticmethod
    def insertCpeMatch(item: dict):
        cpe_name = "{"
        for i in item.get('cpe_name'):
            cpe_name += i.get('cpe23Uri')
        cpe_name += "}"

        columns = [
            item.get('cpe23Uri'),
            item.get('versionStartIncluding'),
            item.get('versionEndIncluding'),
            item.get('versionStartExcluding'),
            item.get('versionEndExcluding'),
            cpe_name
        ]

        Query.execute(Query.insert_nvd_cpe_match, columns)
        Query.commit()

    @staticmethod
    def getCveId(metaId: str):
        Query.execute(Query.get_cve_id, [metaId])
        return Query.cursor.fetchone()[0]

    @staticmethod
    def getCpeId(cpe23: str):
        Query.execute(Query.get_cpe_id, [cpe23])
        return Query.cursor.fetchone()[0]

    @ staticmethod
    def getLastCveId():
        Query.execute(Query.get_last_cve_id)
        return Query.cursor.fetchone()[0]

    @ staticmethod
    def getLastNodeId():
        Query.execute(Query.get_last_node_id)
        return Query.cursor.fetchone()[0]

    @ staticmethod
    def getLastCpeId():
        Query.execute(Query.get_last_cpe_id)
        return Query.cursor.fetchone()[0]

    @staticmethod
    def getLastNvdCpeMatchId():
        Query.execute(Query.get_last_nvd_cpe_match_id)
        return Query.cursor.fetchone()[0]

    @staticmethod
    def getCveCount():
        Query.execute(Query.get_cve_count)
        return Query.cursor.fetchone()[0]

    @staticmethod
    def getCpeCount():
        Query.execute(Query.get_cpe_count)
        return Query.cursor.fetchone()[0]

    @staticmethod
    def getNvdCpeMatchCount():
        Query.execute(Query.get_nvd_cpe_match_count)
        return Query.cursor.fetchone()[0]
