import logging
import traceback

import json
import xmltodict

from dotenv import load_dotenv
from database.database import Database

from query.query import Query


def main():
    '''main function'''
    print('CVE Count :', Query.getLastCveId())
    print('-------------------------------------')
    print('CPE Count :', Query.getCpeCount())
    print('CPE Last Id :', Query.getLastCpeId())


if __name__ == "__main__":
    logging.basicConfig(filename='./error.log', level=logging.ERROR)

    try:
        load_dotenv()
        Database.connect()
        Database.init()
        Query.loadQuery()
        main()
        Database.close()
    except:
        logging.error(traceback.format_exc())
