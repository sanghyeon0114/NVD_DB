import logging
import traceback

from util.print_log import printLog

from dotenv import load_dotenv
from database.database import Database

from query.query import Query


def main():
    '''main function'''

    # 1단계 : cpe dictionary에서 "keyword"가 들어간 cpe23Uri를 모두 검색.

    # 2단계 : cpe match에서 cpe23Uri가 들어간 객체 모두 검색.

    # 3단계 : cve에서 cpe_match 객체와 매치되는 것 모두 검색.

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
