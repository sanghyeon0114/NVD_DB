import logging
import traceback
import time

from dotenv import load_dotenv
from database.database import Database

from query.query import Query


def main():
    '''main function'''
    print('CVE Count :', Query.getLastCveId())
    print('-------------------------------------')
    print('CPE Count :', Query.getCpeCount())
    print('CPE Last Id :', Query.getLastCpeId())

    day = "[" + time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(time.time())) + "]"
    logging.info(day + " no error ( get_count )")


if __name__ == "__main__":
    logging.basicConfig(filename='./info.log', level=logging.INFO)
    logging.info(
        "---------------------[get_count.py]--------------------------")
    try:
        load_dotenv()
        Database.connect()
        Database.init()
        Query.loadQuery()
        main()
        Database.close()
    except:
        day = "[" + time.strftime('%Y-%m-%d %H:%M:%S',
                                  time.localtime(time.time())) + "]"
        logging.info(day + traceback.format_exc())
