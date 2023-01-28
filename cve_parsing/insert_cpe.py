import logging
import traceback

import json
import xmltodict

from dotenv import load_dotenv
from database.database import Database

from query.query import Query


def main():
    '''main function'''
    # "cpe/official-cpe-dictionary_v2.3.xml"
    with open("cpe/test.xml", 'rt', encoding="UTF-8") as f:
        doc = xmltodict.parse(f.read())
        data = json.loads(json.dumps(doc))
        cpe_list = data['cpe-list']['cpe-item']

        for cpe in cpe_list:
            Query.insertAllCPEData(cpe)

    print('inserting cpe data is finished.')


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
