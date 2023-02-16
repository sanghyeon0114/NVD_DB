import logging
import traceback
import pandas as pd

from util.print_log import printLog

from dotenv import load_dotenv
from database.database import Database

from query.query import Query


def manufac_day(data):
    return (data[0], data[1], data[1].split("-")[1])


def main():
    '''main function'''
    keyword = input("input keyword : ")
    find_keyword = '%' + keyword + '%'

    print("Finding cpe match with keyword...")
    # 1단계 : cpe dictionary에서 "keyword"가 들어간 cpe23Uri를 모두 검색.
    # TABLES : cpe (cpe23), cpe_titles(cpeid, value, lang), cpe_references(cpeid, type, uri)
    # 2단계 : cpe match에서 cpe23Uri가 들어간 객체 모두 검색.

    sql = """
        SELECT
            m.cpe23uri, m.versionStartIncluding, m.versionEndIncluding, m.versionStartExcluding, m.versionEndExcluding
        FROM (SELECT c.cpe23 FROM cpe AS c JOIN cpe_titles AS t ON c.id = t.cpeid JOIN cpe_references AS r ON c.id = r.cpeid WHERE c.cpe23 LIKE %s OR t.value LIKE %s OR r.uri LIKE %s) AS c
        JOIN nvd_cpe_match AS m ON (cpe23 = any(m.cpe_name)) OR (m.cpe23uri = cpe23)
    """
    Query.execute(sql, [find_keyword, find_keyword,
                  find_keyword, find_keyword])

    cpe_match_data = set(Query.cursor.fetchall())

    print("Finding cve with cpe match...")
    # 3단계 : cve에서 cpe_match 객체와 매치되는 것 모두 검색.
    # (cpe23Uri, SI, EI, SE, EE)
    cve_data = set([])
    for cpe_match in cpe_match_data:
        sql = """
            SELECT
                c.id, c.CVE_data_meta_ID
            FROM cve AS c
            JOIN cpe_match AS m ON c.id = m.cveid
            WHERE m.cpe23Uri = %s"""

        columns = [cpe_match[0]]

        if cpe_match[1] != None:
            sql += " AND versionStartIncluding = %s"
            columns.append(cpe_match[1])
        if cpe_match[2] != None:
            sql += " AND versionEndIncluding = %s"
            columns.append(cpe_match[2])
        if cpe_match[3] != None:
            sql += " AND versionStartExcluding = %s"
            columns.append(cpe_match[3])
        if cpe_match[4] != None:
            sql += " AND versionEndExcluding = %s"
            columns.append(cpe_match[4])

        Query.execute(sql, columns)
        for cve in Query.cursor.fetchall():
            cve_data.add(cve)

    print("Searching for cve by keyword")
    # 4단계 : cve에서 keyword 를 포함하는 것 모두 검색.
    # cve : CVE_data_meta_ASSIGNER
    # reference_data : url
    # description_data : value
    sql = """
        SELECT
            c.id, c.CVE_data_meta_ID
        FROM cve AS c
        JOIN reference_data AS r ON c.id = r.cveid
        JOIN description_data AS d ON c.id = d.cveid
        WHERE c.CVE_data_meta_ASSIGNER LIKE %s OR r.url LIKE %s OR d.value LIKE %s
    """

    find_keyword = '%' + keyword + '%'
    Query.execute(sql, [find_keyword, find_keyword, find_keyword])

    for cve in Query.cursor.fetchall():
        cve_data.add(cve)

    cve_count = len(cve_data)
    print("------------------------------")
    print("cve_count :", cve_count)
    print("------------------------------")
    df = pd.DataFrame(map(manufac_day, cve_data), columns=[
                      'id', 'metaID', 'year'])

    data_for_year = []
    for year in range(1999, 2024):
        data = len(df[df['year'] == str(year)])
        print("{0} : {1}".format(year, data))
        data_for_year.append((year, data))

    print("------------------------------")
    print("= row data =")
    print(data_for_year)
    print("------------------------------")
    print("= row data 2 =")
    print(df)
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
