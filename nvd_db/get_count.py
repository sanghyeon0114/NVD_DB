import logging
import traceback

from util.print_log import printLog

from dotenv import load_dotenv
from database.database import Database

from query.query import Query


def main():
    '''main function'''

    print('-------------------------------------')
    print('CVE Count :', Query.getCveCount())
    print('CVE Last Id :', Query.getLastCveId())
    print('-------------------------------------')
    print('CPE Count :', Query.getCpeCount())
    print('-------------------------------------')
    print('NVD_CPE_MATCH Count :', Query.getNvdCpeMatchCount())
    print('NVD_CPE_MATCH Last Id :', Query.getLastNvdCpeMatchId())
    print('-------------------------------------')


if __name__ == "__main__":
    logging.basicConfig(filename='./info.log', level=logging.INFO)
    try:
        load_dotenv()
        Database.connect()
        Query.loadQuery()
        main()
        Database.close()
    except:
        printLog("get_count.py", traceback.format_exc())
