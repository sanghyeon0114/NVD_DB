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
    keyword: str = input("input keyword : ")
    Query.execute("""
    SELECT
        COUNT(cpe23)
    FROM
        cpe
    WHERE
        (titles_tsv @@ to_tsquery('english', %s)) OR (references_tsv @@ to_tsquery('english', %s))
    """, [keyword, keyword])
    total = Query.cursor.fetchone()[0]
    order = 0

    Query.execute("""
    SELECT
        cpe23
    FROM
        cpe
    WHERE
        (titles_tsv @@ to_tsquery('english', %s)) OR (references_tsv @@ to_tsquery('english', %s))
    """, [keyword, keyword])

    for cpe in Query.cursor.fetchall():
        order+=1

        Query.execute("""
        SELECT
            COUNT(*)
        FROM
            nvd_cpe_match
        WHERE
            cpe_name_tsv @@ plainto_tsquery('simple', %s)
        """, [cpe[0]])
        count = Query.cursor.fetchone()[0]
        print(count)
        if count != 0:
            print(total, " / ", order, " => ", count)

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
