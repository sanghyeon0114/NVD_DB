import logging
import traceback

from util.print_log import printLog

from dotenv import load_dotenv
from database.database import Database
from format.cve import CVE

from query.query import Query


def main():
    '''main function'''
    Database.reload_cve()

    for year in range(2002, 2024):
        cveData = CVE(year)
        for item in range(cveData.length):
            Query.insertAllCVEData(cveData.getItem(item))
            Query.commit()
        printLog("insert_cve.py", "success to upload {} cve data".format(year))
    printLog("insert_cve.py", "finished")


if __name__ == "__main__":
    logging.basicConfig(filename='./info.log', level=logging.INFO)
    printLog("insert_cve.py", "run")
    try:
        load_dotenv()
        Database.connect()
        Query.loadQuery()
        main()
        Database.close()
    except:
        printLog("insert_cve.py", traceback.format_exc())
