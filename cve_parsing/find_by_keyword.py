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
        cpe23
    FROM
        cpe
    WHERE
        (titles_tsv @@ to_tsquery('english', 'proxy')) OR (references_tsv @@ to_tsquery('english', 'proxy'))
    """, [keyword, keyword])

    Query.execute("""
    SELECT
        cpe23
    FROM
        nvd_cpe_match
    WHERE
        cpe_name_tsv @@ to_tsquery('english', c.cpe23)
    """, [keyword, keyword])

    Query.execute("""
    SELECT
        cpe23
    FROM
        nvd_cpe_match
    JOIN cpe AS c ON (titles_tsv @@ to_tsquery('english', 'proxy')) OR (references_tsv @@ to_tsquery('english', 'proxy'))
    WHERE
        cpe_name_tsv @@ to_tsquery('english', $$c.cpe23$$)
    """, [keyword, keyword])

    print(Query.cursor.fetchall())
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
