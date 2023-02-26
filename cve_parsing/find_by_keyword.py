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
    col = ''
    keyword: str = input("input keyword : ")
    col += keyword

    while True:
        keyword: str = input("input keyword : ")
        if keyword == '':
            break
        col += ' | '
        col += keyword

    print("find keyword :", col)

    Query.execute("""
        SELECT DISTINCT
            t2.id
        FROM (SELECT
            cveId
        FROM (SELECT
            cpe, versionStartIncluding, versionEndIncluding, versionStartExcluding, versionEndExcluding
        FROM (SELECT cpe23 FROM cpe as c WHERE (cpe23_tsv @@ to_tsquery('english', '{}')) OR (titles_tsv @@ to_tsquery('english', '{}')) OR (references_tsv @@ to_tsquery('english', '{}'))) t1
        JOIN nvd_cpe23 AS t2 ON t1.cpe23 = t2.cpe23) t1
        JOIN cpe_match AS t2 ON (t1.cpe = t2.cpe AND t1.versionStartIncluding = t2.versionStartIncluding AND t1.versionEndIncluding = t2.versionEndIncluding AND t1.versionStartExcluding = t2.versionStartExcluding AND t1.versionEndExcluding = t2.versionEndExcluding)) t1
        JOIN cve AS t2 ON t2.id = t1.cveId
        """.format(col, col, col))

    print(len(Query.cursor.fetchall()))
    cve = set(Query.cursor.fetchall())

    Query.execute("""
        SELECT DISTINCT
            id
        FROM cve WHERE (references_tsv @@ to_tsquery('english', '{}')) OR (description_tsv @@ to_tsquery('english', '{}'))
        """, format(col, col))

    for i in Query.cursor.fetchall():
        cve.add(i)

    print(len(cve))

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
