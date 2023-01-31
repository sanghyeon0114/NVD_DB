import logging
import traceback
import time

from dotenv import load_dotenv
from database.database import Database
from format.cve import CVE

from query.query import Query

# TODO : db에 cve 잘 저장됐는지 select 로 뽑아서 확인


def main():
    '''main function'''
    cve2002 = CVE(2002)
    for i in range(100):
        Query.insertAllCVEData(cve2002.getItem(i))

    print("cve2002.length :", cve2002.length)
    print("Query.getLastCveId() :", Query.getLastCveId())

    print('inserting cve data is finished.')
    
    day = "[" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "]"
    logging.error(day + " no error ( insert_cve )")


if __name__ == "__main__":
    logging.basicConfig(filename='./error.log', level=logging.ERROR)

    try:
        load_dotenv()
        Database.connect()
        Query.loadQuery()
        main()
        Database.close()
    except:
        day = "[" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "]"
        logging.error(day + traceback.format_exc())
