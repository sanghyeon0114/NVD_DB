import psycopg2
import logging
import traceback

from database.database import Database
from database.create_table import *

from .insert import *
from .select import *

from format.item import Item
import dateutil.parser


class Query(Database):
    # cve table
    insert_cve: str = None
    insert_problemtype_data: str = None
    insert_reference_data: str = None
    insert_description_data: str = None

    # configurations table
    insert_configuration_nodes: str = None
    insert_cpe_match: str = None

    # impact table
    insert_impact: str = None

    # cpe table
    insert_cpe: str = None

    # cpe references table
    insert_cpe_references: str = None

    # select sql
    get_last_cve_id: str = None
    get_last_node_id: str = None
    get_last_cpe_id: str = None

    @staticmethod
    def loadQuery():

        Query.insert_cve = insert_cve
        Query.insert_problemtype_data = insert_problemtype_data
        Query.insert_reference_data = insert_reference_data
        Query.insert_description_data = insert_description_data

        Query.insert_configuration_nodes = insert_configuration_nodes
        Query.insert_cpe_match = insert_cpe_match

        Query.insert_impact = insert_impact

        Query.insert_cpe = insert_cpe
        Query.insert_cpe_references = insert_cpe_references

        Query.get_last_cve_id = get_last_cve_id
        Query.get_last_node_id = get_last_node_id
        Query.get_last_cpe_id = get_last_cpe_id

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
            Query.print(traceback.format_exc())
            logging.error(traceback.format_exc())

    @staticmethod
    def insertCve(item: Item) -> int:
        """Create cve data function"""

        # cve
        Query.execute(Query.insert_cve, [item.cve.get('data_type'), item.cve.get('data_format'), item.cve.get('data_version'), item.cve.get('CVE_data_meta').get('ID'),
                                         item.cve.get('CVE_data_meta').get('ASSIGNER'), item.configurations.get('CVE_data_version'), dateutil.parser.parse(item.publishedDate), dateutil.parser.parse(item.lastModifiedDate)])

        cveId = Query.getLastCveId()

        # problemtypes
        problemtypes: list[dict] = item.cve['problemtype']['problemtype_data'][0]['description']

        for problemtype in problemtypes:
            Query.execute(Query.insert_problemtype_data, [
                cveId, problemtype.get('lang'), problemtype.get('value')])

        # references
        references: list[dict] = item.cve['references']['reference_data']
        for reference in references:
            Query.execute(Query.insert_reference_data, [
                cveId, reference.get('url'), reference.get('name'), reference.get('refsource'), "{"+','.join(reference.get('tags'))+"}"])

        # description
        description: list[dict] = item.cve['description']['description_data'][0]
        Query.execute(Query.insert_description_data, [
            cveId, description.get('lang'), description.get('value')])

        return cveId

    @staticmethod
    def insertConfigurations(item: Item, cveId: int):
        """Create configurations data function"""
        nodes: list[dict] = item.configurations.get('nodes')

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

            # cpe_match [TODO] : 수정사항이 있을 수 있음
            cpe_match: list[dict] = node.get('cpe_match')

            if len(cpe_match) != 0:
                for cpe in cpe_match:

                    cpe23: str = cpe.get('cpe23Uri')
                    cpe23Data = cpe23.split(':')
                    columns = [
                        cveId,
                        nodeId,
                        cpe.get('vulnerable'),
                        cpe23,
                        cpe23Data[2],
                        cpe23Data[3],
                        cpe23Data[4],
                        cpe23Data[5],
                        cpe23Data[6],
                        cpe23Data[7],
                        cpe23Data[8],
                        cpe23Data[9],
                        cpe23Data[10],
                        cpe23Data[11],
                        cpe23Data[12],
                        cpe.get('versionStartIncluding'),
                        cpe.get('versionEndIncluding'),
                        cpe.get('versionStartExcluding'),
                        cpe.get('versionEndExcluding'),
                        "{"+','.join(cpe['cpe_name'])+"}"
                    ]
                    Query.execute(Query.insert_cpe_match, columns)

    @ staticmethod
    def insertNodeChildren(children: list[dict], cveId, nodeId):
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

            # cpe_match [TODO] : 수정사항이 있을 수 있음
            cpe_match: list[dict] = child.get('cpe_match')

            if len(cpe_match) != 0:
                for cpe in cpe_match:
                    cpe23: str = cpe.get('cpe23Uri')
                    cpe23Data = cpe23.split(':')
                    columns = [
                        cveId,
                        nodeId,
                        cpe.get('vulnerable'),
                        cpe23,
                        cpe23Data[2],
                        cpe23Data[3],
                        cpe23Data[4],
                        cpe23Data[5],
                        cpe23Data[6],
                        cpe23Data[7],
                        cpe23Data[8],
                        cpe23Data[9],
                        cpe23Data[10],
                        cpe23Data[11],
                        cpe23Data[12],
                        cpe.get('versionStartIncluding'),
                        cpe.get('versionEndIncluding'),
                        cpe.get('versionStartExcluding'),
                        cpe.get('versionEndExcluding'),
                        "{"+','.join(cpe['cpe_name'])+"}"
                    ]
                    Query.execute(Query.insert_cpe_match, columns)

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
            Query.insertCpeReferences(cpe, cpeId)
            Query.commit()
        except psycopg2.Error:
            Query.print(traceback.format_exc())
            logging.error(traceback.format_exc())

    @ staticmethod
    def insertCpe(cpe: dict):
        """Create cpe data function"""
        cpe22 = cpe.get('@name')
        title = cpe.get('title')
        cpe23: str = cpe.get('cpe-23:cpe23-item').get('@name')
        cpe23Data = cpe23.split(':')

        columns = [
            cpe22,
            title.get('#text'),
            title.get('@xml:lang'),
            cpe23,
            cpe23Data[2],
            cpe23Data[3],
            cpe23Data[4],
            cpe23Data[5],
            cpe23Data[6],
            cpe23Data[7],
            cpe23Data[8],
            cpe23Data[9],
            cpe23Data[10],
            cpe23Data[11],
            cpe23Data[12],
        ]
        Query.execute(Query.insert_cpe, columns)

        cpeId = Query.getLastCpeId()
        return cpeId

    @ staticmethod
    def insertCpeReferences(cpe, cpeId):
        """Create cpe references data function"""
        references = cpe['references']['reference']

        for reference in references:
            columns = [
                cpeId,
                reference.get('#text'),
                reference.get('@href')
            ]
            Query.execute(Query.insert_cpe_references, columns)

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
