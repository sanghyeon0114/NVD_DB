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

    insert_configuration_nodes: str = None
    insert_cpe_match: str = None

    insert_impact: str = None

    get_last_cve_id: str = None
    get_last_node_id: str = None

    @staticmethod
    def loadQuery():

        Query.insert_cve = insert_cve
        Query.insert_problemtype_data = insert_problemtype_data
        Query.insert_reference_data = insert_reference_data
        Query.insert_description_data = insert_description_data

        Query.insert_configuration_nodes = insert_configuration_nodes
        Query.insert_cpe_match = insert_cpe_match

        Query.insert_impact = insert_impact

        Query.get_last_cve_id = get_last_cve_id
        Query.get_last_node_id = get_last_node_id

    @staticmethod
    def insertAllData(item: Item):
        cveId = Query.insertCve(item)
        Query.insertConfigurations(item, cveId)
        Query.insertImpact(item, cveId)
        Query.commit()

    @staticmethod
    def insertCve(item: Item) -> int:
        """Create database cursor and table function"""
        try:
            Query.execute(Query.insert_cve, [item.cve['data_type'], item.cve['data_format'], item.cve['data_version'], item.cve['CVE_data_meta']['ID'],
                                             item.cve['CVE_data_meta']['ASSIGNER'], item.configurations['CVE_data_version'], dateutil.parser.parse(item.publishedDate), dateutil.parser.parse(item.lastModifiedDate)])

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

            return cveId
        except psycopg2.Error as err:
            Query.print("execute sql error : ")
            for msg in err.args:
                Query.print(msg)

    @staticmethod
    def insertConfigurations(item: Item, cveId: int):
        nodes: list = item.configurations.get('nodes')

        for node in nodes:
            columns = [
                cveId,
                node['operator'],
                None
            ]
            Query.execute(Query.insert_configuration_nodes, columns)

            nodeId = Query.getLastNodeId()
            if len(node['children']) != 0:
                Query.insertNodeChildren(node['children'], cveId, nodeId)

            # cpe_match [TODO] : 수정사항이 있을 수 있음
            cpe_match: list[dict] = node.get('cpe_match')

            if len(cpe_match) != 0:
                for cpe in cpe_match:
                    columns = [
                        cveId,
                        nodeId,
                        cpe.get('vulnerable'),
                        cpe.get('cpe23Uri'),
                        cpe.get('versionStartIncluding'),
                        cpe.get('versionEndIncluding'),
                        cpe.get('versionStartExcluding'),
                        cpe.get('versionEndExcluding'),
                        "{"+','.join(cpe['cpe_name'])+"}"
                    ]
                    Query.execute(Query.insert_cpe_match, columns)

    @staticmethod
    def insertNodeChildren(children: dict, cveId, nodeId):
        for child in children:
            columns = [
                cveId,
                child['operator'],
                nodeId
            ]
            Query.execute(Query.insert_configuration_nodes, columns)

            parentId = Query.getLastNodeId()
            if len(child['children']) != 0:
                Query.insertNodeChildren(child['children'], cveId, parentId)

            # cpe_match [TODO] : 수정사항이 있을 수 있음
            cpe_match: list[dict] = child.get('cpe_match')

            if len(cpe_match) != 0:
                for cpe in cpe_match:
                    columns = [
                        cveId,
                        nodeId,
                        cpe.get('vulnerable'),
                        cpe.get('cpe23Uri'),
                        cpe.get('versionStartIncluding'),
                        cpe.get('versionEndIncluding'),
                        cpe.get('versionStartExcluding'),
                        cpe.get('versionEndExcluding'),
                        "{"+','.join(cpe['cpe_name'])+"}"
                    ]
                    Query.execute(Query.insert_cpe_match, columns)

    @staticmethod
    def insertImpact(item: Item, cveId: int):
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

    @staticmethod
    def getLastCveId():
        Query.execute(Query.get_last_cve_id)
        return Query.cursor.fetchone()[0]

    @staticmethod
    def getLastNodeId():
        Query.execute(Query.get_last_node_id)
        return Query.cursor.fetchone()[0]
