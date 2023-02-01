import logging
import traceback
import time

from dotenv import load_dotenv
from database.database import Database
from format.cve import CVE

from query.query import Query


def main():
    '''main function'''

    for year in range(2002, 2024):
        cveData = CVE(year)
        for item in range(5):
            Query.insertAllCVEData(cveData.getItem(item))
        day = "[" + time.strftime('%Y-%m-%d %H:%M:%S',
                                  time.localtime(time.time())) + "]"
        logging.info(
            day + " success to upload {} cve data ( insert_cve )".format(year))

    print('inserting cve data is finished.')

    day = "[" + time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(time.time())) + "]"
    logging.info(day + " no error ( insert_cve )")


if __name__ == "__main__":
    logging.basicConfig(filename='./info.log', level=logging.INFO)
    logging.info(
        "---------------------[insert_cve.py]--------------------------")
    try:
        load_dotenv()
        Database.connect()
        Query.loadQuery()
        main()
        Database.close()
    except:
        day = "[" + time.strftime('%Y-%m-%d %H:%M:%S',
                                  time.localtime(time.time())) + "]"
        logging.info(day + traceback.format_exc())
