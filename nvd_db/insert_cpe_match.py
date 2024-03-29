import logging
import traceback
import time

from util.print_log import printLog

import pandas as pd

from dotenv import load_dotenv
from database.database import Database

from query.query import Query


def main():
    '''main function'''
    Database.reload_nvd_cpe_match()

    cpe_match = pd.read_json('cve/nvdcpematch-1.0.json').get("matches")

    for item in cpe_match:
        Query.insertCpeMatch(item)
    printLog("insert_cpe_match.py", "finished")


if __name__ == "__main__":
    logging.basicConfig(filename='./info.log', level=logging.INFO)
    printLog("insert_cpe_match.py", "run")
    try:
        load_dotenv()
        Database.connect()
        Query.loadQuery()
        main()
        Database.close()
    except:
        printLog("insert_cpe_match.py", traceback.format_exc())
