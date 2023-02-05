import logging
import traceback

from util.print_log import printLog

from dotenv import load_dotenv
from database.database import Database

from query.query import Query


def main():
    '''main function'''
    keyword = input("input keyword : ")

    print("Finding keyword in cpe dictionary...")
    # 1단계 : cpe dictionary에서 "keyword"가 들어간 cpe23Uri를 모두 검색.
    # TABLES : cpe (cpe23), cpe_titles(cpeid, value, lang), cpe_references(cpeid, type, uri)
    sql = """
        SELECT
            c.cpe23
        FROM cpe AS c
        JOIN cpe_titles AS t ON c.id = t.cpeid
        JOIN cpe_references AS r ON c.id = r.cpeid
        WHERE c.cpe23 LIKE '%{0}%' OR t.value LIKE '%{0}%' OR r.type LIKE '%{0}%' OR r.uri LIKE '%{0}%'
    """.format(keyword)
    Query.execute(sql)

    cpe23_data = set([])
    for cpe23 in Query.cursor.fetchall():
        cpe23_data.add(cpe23[0])

    if len(cpe23_data) == 0:
        print("No result")
        return

    print("Finding cpe23Uri in nvd cpe match...")
    # 2단계 : cpe match에서 cpe23Uri가 들어간 객체 모두 검색.
    cpe_match_data = set([])
    for cpe23 in cpe23_data:
        sql = """
            SELECT
                m.cpe23uri, m.versionStartIncluding, m.versionEndIncluding, m.versionStartExcluding, m.versionEndExcluding
            FROM nvd_cpe_match AS m
            WHERE ('{0}' = any(m.cpe_name)) OR (m.cpe23uri = '{0}')
        """.format(cpe23)
        Query.execute(sql)
        for match in Query.cursor.fetchall():
            cpe_match_data.add(match)
    cpe_count = len(cpe_match_data)

    print("Finding cve with cpe match...")
    # 3단계 : cve에서 cpe_match 객체와 매치되는 것 모두 검색.
    # (cpe23Uri, SI, EI, SE, EE)
    cve_data = set([])
    for cpe_match in cpe_match_data:
        sql = """
            SELECT
                c.*
            FROM cve AS c
            JOIN cpe_match AS m ON c.id = m.cveid
            WHERE m.cpe23Uri = '{0}'""".format(cpe_match[0])

        if cpe_match[1] != None:
            sql += " AND versionStartIncluding = '{0}'".format(cpe_match[1])
        if cpe_match[2] != None:
            sql += " AND versionEndIncluding = '{0}'".format(cpe_match[2])
        if cpe_match[3] != None:
            sql += " AND versionStartExcluding = '{0}'".format(cpe_match[3])
        if cpe_match[4] != None:
            sql += " AND versionEndExcluding = '{0}'".format(cpe_match[4])

        Query.execute(sql)
        for cve in Query.cursor.fetchall():
            cve_data.add(cve)

    print("Searching for cve by keyword")
    # 4단계 : cve에서 keyword 를 포함하는 것 모두 검색.
    # cve : CVE_data_meta_ASSIGNER
    # reference_data : url
    # description_data : value
    sql = """
        SELECT
            c.*
        FROM cve AS c
        JOIN reference_data AS r ON c.id = r.cveid
        JOIN description_data AS d ON c.id = d.cveid
        WHERE c.CVE_data_meta_ASSIGNER LIKE '%{0}%' OR r.url LIKE '%{0}%' OR d.value LIKE '%{0}%'
    """.format(keyword)

    Query.execute(sql)

    for cve in Query.cursor.fetchall():
        cve_data.add(cve)

    cve_count = len(cve_data)
    print("cve_count :", cve_count)
    print("cpe_count :", cpe_count)
    printLog("insert_cpe_match.py", "finished")


if __name__ == "__main__":
    logging.basicConfig(filename='./info.log', level=logging.INFO)
    printLog("find_by_keyword.py", "run")
    try:
        load_dotenv()
        Database.connect()
        Query.loadQuery()
        main()
        Database.close()
    except:
        printLog("find_by_keyword.py", traceback.format_exc())
