import psycopg2
import logging
import traceback
import time
import json

from database.database import Database
from database.create_table import *

from .select import *

from format.item import Item
import dateutil.parser


class Query(Database):
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
        except:
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
                            json.dumps(
                                item.cve['problemtype']['problemtype_data'][0]['description']),
                            json.dumps(item.cve['references']
                                       ['reference_data']),
                            json.dumps(item.cve['description']
                                       ['description_data']),
                            json.dumps(item.cve['references']
                                       ['reference_data']),
                            json.dumps(item.cve['description']
                                       ['description_data']),
                            item.configurations.get('CVE_data_version'),
                            dateutil.parser.parse(item.publishedDate), dateutil.parser.parse(
                                item.lastModifiedDate)
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
                INSERT INTO cpe_match (cveId, nodeId, cpe, versionStartIncluding, versionEndIncluding, versionStartExcluding, versionEndExcluding, vulnerable) SELECT %s, %s, %s, %s, %s, %s, %s, %s
                WHERE EXISTS (SELECT id FROM nvd_cpe_match WHERE cpe = %s AND versionStartIncluding = %s AND versionEndIncluding = %s AND versionStartExcluding = %s AND versionEndExcluding = %s)
                """

                cpe_match_columns = []

                for cpe in cpe_match:
                    cpe_match_columns = [cveId,
                                         nodeId,
                                         str(cpe.get('cpe23Uri')),
                                         str(cpe.get('versionStartIncluding')),
                                         str(cpe.get('versionEndIncluding')),
                                         str(cpe.get('versionStartExcluding')),
                                         str(cpe.get('versionEndExcluding')),
                                         cpe.get('vulnerable'),
                                         str(cpe.get('cpe23Uri')),
                                         str(cpe.get('versionStartIncluding')),
                                         str(cpe.get('versionEndIncluding')),
                                         str(cpe.get('versionStartExcluding')),
                                         str(cpe.get('versionEndExcluding'))]

                Query.execute(sql, cpe_match_columns)
                Query.commit()

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
                INSERT INTO cpe_match (cveId, nodeId, cpe, versionStartIncluding, versionEndIncluding, versionStartExcluding, versionEndExcluding, vulnerable) SELECT %s, %s, %s, %s, %s, %s, %s, %s
                WHERE EXISTS (SELECT id FROM nvd_cpe_match WHERE cpe = %s AND versionStartIncluding = %s AND versionEndIncluding = %s AND versionStartExcluding = %s AND versionEndExcluding = %s)
                """

                cpe_match_columns = []

                for cpe in cpe_match:
                    cpe_match_columns = [cveId,
                                         nodeId,
                                         str(cpe.get('cpe23Uri')),
                                         str(cpe.get('versionStartIncluding')),
                                         str(cpe.get('versionEndIncluding')),
                                         str(cpe.get('versionStartExcluding')),
                                         str(cpe.get('versionEndExcluding')),
                                         cpe.get('vulnerable'),
                                         str(cpe.get('cpe23Uri')),
                                         str(cpe.get('versionStartIncluding')),
                                         str(cpe.get('versionEndIncluding')),
                                         str(cpe.get('versionStartExcluding')),
                                         str(cpe.get('versionEndExcluding'))]

                Query.execute(sql, cpe_match_columns)
                Query.commit()

    @ staticmethod
    def insertImpact(item: Item, cveId: int):
        """Create impact data function"""

        sql = '''
            INSERT INTO impact (
                cveId,
                baseMetricV3_cvssV3_version,
                baseMetricV3_cvssV3_vectorString,
                baseMetricV3_cvssV3_baseScore,
                baseMetricV3_cvssV3_baseSeverity,
                baseMetricV3_exploitabilityScore,
                baseMetricV3_impactScore,
                baseMetricV2_cvssV2_version,
                baseMetricV2_cvssV2_vectorString,
                baseMetricV2_cvssV2_baseScore,
                baseMetricV2_severity,
                baseMetricV2_exploitabilityScore,
                baseMetricV2_impactScore,
                baseMetricV2_acInsufInfo,
                baseMetricV2_obtainAllPrivilege,
                baseMetricV2_obtainUserPrivilege,
                baseMetricV2_obtainOtherPrivilege,
                baseMetricV2_userInteractionRequired
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
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

        Query.execute(sql, columns)

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
                cpe23,
                cpe23_tsv,
                cpe22,
                titles,
                titles_tsv,
                references_data,
                references_tsv
            ) VALUES (%s, to_tsvector('english', %s), %s, %s, to_tsvector('english', %s), %s, to_tsvector('english', %s))
            """
        columns = [
            cpe23,
            cpe23,
            cpe22,
            json.dumps(cpe.get('title')),
            json.dumps(cpe.get('title')),
            json.dumps(cpe.get('references')),
            json.dumps(cpe.get('references'))
        ]
        Query.execute(sql, columns)

    @staticmethod
    def insertCpeMatch(item: dict):
        sql = """
            INSERT INTO nvd_cpe_match (
                cpe,
                versionStartIncluding,
                versionEndIncluding,
                versionStartExcluding,
                versionEndExcluding
            ) VALUES (%s, %s, %s, %s, %s)
        """
        columns = [
            str(item.get('cpe23Uri')),
            str(item.get('versionStartIncluding')),
            str(item.get('versionEndIncluding')),
            str(item.get('versionStartExcluding')),
            str(item.get('versionEndExcluding'))
        ]
        Query.execute(sql, columns)

        cpe_name: list = item.get('cpe_name')

        if cpe_name == None:
            return

        sql = """
            INSERT INTO nvd_cpe23 (
                cpe,
                versionStartIncluding,
                versionEndIncluding,
                versionStartExcluding,
                versionEndExcluding,
                cpe23
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """

        for i in cpe_name:
            columns = [
                str(item.get('cpe23Uri')),
                str(item.get('versionStartIncluding')),
                str(item.get('versionEndIncluding')),
                str(item.get('versionStartExcluding')),
                str(item.get('versionEndExcluding')),
                i.get('cpe23Uri')
            ]
            Query.execute(sql, columns)

        Query.commit()

    @ staticmethod
    def getCveId(metaId: str):
        Query.execute(Query.get_cve_id, [metaId])
        return Query.cursor.fetchone()[0]

    @ staticmethod
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

    @ staticmethod
    def getLastNvdCpeMatchId():
        Query.execute(Query.get_last_nvd_cpe_match_id)
        return Query.cursor.fetchone()[0]

    @ staticmethod
    def getCveCount():
        Query.execute(Query.get_cve_count)
        return Query.cursor.fetchone()[0]

    @ staticmethod
    def getCpeCount():
        Query.execute(Query.get_cpe_count)
        return Query.cursor.fetchone()[0]

    @ staticmethod
    def getNvdCpeMatchCount():
        Query.execute(Query.get_nvd_cpe_match_count)
        return Query.cursor.fetchone()[0]

    @ staticmethod
    def getNvdCpeMatch(cpe23Uri, versionStartIncluding, versionEndIncluding, versionStartExcluding, versionEndExcluding):
        sql = "SELECT id FROM nvd_cpe_match WHERE cpe23Uri = %s AND versionStartIncluding {} AND versionEndIncluding {} AND versionStartExcluding {} AND versionEndExcluding {};"
        sql = sql.format('is NULL' if versionStartIncluding is None else ("= '{}'".format(versionStartIncluding)), 'is NULL' if versionEndIncluding is None else ("= '{}'".format(versionEndIncluding)),
                         'is NULL' if versionStartExcluding is None else ("= '{}'".format(versionStartExcluding)), 'is NULL' if versionEndExcluding is None else ("= '{}'".format(versionEndExcluding)))
        Query.execute(sql, [cpe23Uri])

        result = Query.cursor.fetchone()
        result = result[0] if result is not None else None
        return result
