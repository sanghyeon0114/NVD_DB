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
        if keyword == '.':
            break
        col += ' | '
        col += keyword
    
    print(col)

    #Query.execute("""
    #SELECT DISTINCT
    #    t2.cpe_info
    #FROM (SELECT cpe23 FROM cpe as c WHERE (titles_tsv @@ to_tsquery('english', %s)) OR (references_tsv @@ to_tsquery('english', %s))) t1
    #JOIN nvd_cpe_match AS t2 ON t1.cpe23 = ANY(t2.cpe_name)
    #""", [keyword, keyword])

    Query.execute("""
        SELECT DISTINCT
            t2.cveId
        FROM (SELECT DISTINCT
                t2.cpe_info
                FROM (SELECT cpe23 FROM cpe as c WHERE (titles_tsv @@ to_tsquery('english', %s)) OR (references_tsv @@ to_tsquery('english', %s))) t1
                JOIN nvd_cpe_match AS t2 ON t1.cpe23 = ANY(t2.cpe_name)) t1
        JOIN cpe_match AS t2 ON (t2.cpe_info @> t1.cpe_info)
        """, [col, col])
    
    cveList = set([])

    for cve in Query.cursor.fetchall():
        cveList.add(cve[0])

    Query.execute("""
        SELECT DISTINCT
            id
        FROM
            cve
        WHERE
            (references_tsv @@ to_tsquery('english', %s)) OR (description_tsv @@ to_tsquery('english', %s))
        """, [col, col])
    for cve in Query.cursor.fetchall():
        cveList.add(cve[0])

    print(cveList)
    print(len(cveList))

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
