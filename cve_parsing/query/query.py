import psycopg2
import logging
import traceback
import time
import json

from database.database import Database
from database.create_table import *

from .insert import *
from .select import *

from format.item import Item
import dateutil.parser


class Query(Database):
    # impact table
    insert_impact: str = None

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
        Query.insert_impact = insert_impact

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
                CVE_data_meta,
                problemtype_data,
                references_data,
                description_data,
                references_tsv,
                description_tsv,
                configurations_CVE_data_version,
                publishedDate,
                lastModifiedDate
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, to_tsvector('english', %s), to_tsvector('english', %s), %s, %s, %s) RETURNING id
            """
        Query.execute(sql, [item.cve.get('data_type'), 
                            item.cve.get('data_format'), 
                            item.cve.get('data_version'), 
                            json.dumps(item.cve.get('CVE_data_meta')),
                            json.dumps(item.cve['problemtype']['problemtype_data'][0]['description']),
                            json.dumps(item.cve['references']['reference_data']),
                            json.dumps(item.cve['description']['description_data']),
                            json.dumps(item.cve['references']['reference_data']),
                            json.dumps(item.cve['description']['description_data']),
                            item.configurations.get('CVE_data_version'),
                            dateutil.parser.parse(item.publishedDate), dateutil.parser.parse(item.lastModifiedDate)
                        ])
        
        cveId = Query.cursor.fetchone()[0]
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

            sql = """
                INSERT INTO configuration_nodes (cveId, operator, parentId) VALUES (%s, %s, %s) RETURNING id
                """
            Query.execute(sql, columns)

            nodeId = Query.cursor.fetchone()[0]
            if len(node.get('children')) != 0:
                Query.insertNodeChildren(node.get('children'), cveId, nodeId)

            cpe_match: list = node.get('cpe_match')

            if len(cpe_match) != 0:
                sql = """
                INSERT INTO cpe_match (cveId, nodeId, cpe_info) VALUES 
                """
                
                cpe_match_columns = []

                for cpe in cpe_match:
                    sql += "(%s, %s, %s),"
                    cpe_match_columns.append(cveId)
                    cpe_match_columns.append(nodeId)
                    cpe_match_columns.append(json.dumps(cpe))
                    
                Query.execute(sql[:-1], cpe_match_columns)

    @ staticmethod
    def insertNodeChildren(children: list, cveId, nodeId):
        """Create children data in configurations function"""
        for child in children:
            columns = [
                cveId,
                child.get('operator'),
                nodeId
            ]
            sql = """
                INSERT INTO configuration_nodes (cveId, operator, parentId) VALUES (%s, %s, %s) RETURNING id
                """
            Query.execute(sql, columns)

            parentId = Query.cursor.fetchone()[0]
            if len(child.get('children')) != 0:
                Query.insertNodeChildren(
                    child.get('children'), cveId, parentId)

            cpe_match: list = child.get('cpe_match')
            
            if len(cpe_match) != 0:
                sql = """
                INSERT INTO cpe_match (cveId, nodeId, cpe_info) VALUES 
                """
                
                cpe_match_columns = []

                for cpe in cpe_match:
                    sql += "(%s, %s, %s),"
                    cpe_match_columns.append(cveId)
                    cpe_match_columns.append(nodeId)
                    cpe_match_columns.append(json.dumps(cpe))
                    
                Query.execute(sql[:-1], cpe_match_columns)

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
    def insertCPEData(cpe):
        '''
            if you want to handle error, plz to handle in this function
        '''
        try:
            Query.insertCpe(cpe)
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

        sql = """
            INSERT INTO cpe (
                cpe22,
                cpe23,
                titles,
                titles_tsv,
                references_data,
                references_tsv
            ) VALUES (%s, %s, %s, to_tsvector('english', %s), %s, to_tsvector('english', %s))
            """
        columns = [
            cpe22,
            cpe23,
            json.dumps(cpe.get('title')),
            json.dumps(cpe.get('title')),
            json.dumps(cpe.get('references')),
            json.dumps(cpe.get('references'))
        ]
        Query.execute(sql, columns)
    
    @staticmethod
    def insertCpeMatch(item: dict):
        cpe_name = "{"
        for i in item.get('cpe_name'):
            cpe_name += i.get('cpe23Uri')
        cpe_name += "}"

        cpe_info = item
        cpe_info.pop("cpe_name")

        columns = [
            json.dumps(cpe_info),
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

    @staticmethod
    def getNvdCpeMatch(cpe23Uri, versionStartIncluding, versionEndIncluding, versionStartExcluding, versionEndExcluding):
        sql = "SELECT id FROM nvd_cpe_match WHERE cpe23Uri = %s AND versionStartIncluding {} AND versionEndIncluding {} AND versionStartExcluding {} AND versionEndExcluding {};"
        sql = sql.format('is NULL' if versionStartIncluding is None else ("= '{}'".format(versionStartIncluding)), 'is NULL' if versionEndIncluding is None else ("= '{}'".format(versionEndIncluding)),
                         'is NULL' if versionStartExcluding is None else ("= '{}'".format(versionStartExcluding)), 'is NULL' if versionEndExcluding is None else ("= '{}'".format(versionEndExcluding)))
        Query.execute(sql, [cpe23Uri])

        result = Query.cursor.fetchone()
        result = result[0] if result is not None else None
        return result