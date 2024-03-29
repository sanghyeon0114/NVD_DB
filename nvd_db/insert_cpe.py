import logging
import traceback

from util.print_log import printLog

import json
import xmltodict

from dotenv import load_dotenv
from database.database import Database

from query.query import Query


def main():
    '''main function'''
    with open("cpe/official-cpe-dictionary_v2.3.xml", 'rt', encoding="UTF-8") as f:
        doc = xmltodict.parse(f.read())
        data = json.loads(json.dumps(doc))
        cpe_list = data['cpe-list']['cpe-item']
        printLog("insert_cpe.py", "success to load cpe data")
        for cpe in cpe_list:
            Query.insertCPEData(cpe)

    printLog("insert_cpe.py", "finished")


if __name__ == "__main__":
    logging.basicConfig(filename='./info.log', level=logging.INFO)
    printLog("insert_cpe.py", "run")
    try:
        load_dotenv()
        Database.connect()
        Query.loadQuery()
        main()
        Database.close()
    except:
        printLog("insert_cpe.py", traceback.format_exc())
