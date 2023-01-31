import logging
import traceback
import time

import json
import xmltodict

from dotenv import load_dotenv
from database.database import Database

from query.query import Query

# TODO : 시간 체크 기능. ( log 하나 더 만들기 )

def main():
    '''main function'''
    # ""
    with open("cpe/official-cpe-dictionary_v2.3.xml", 'rt', encoding="UTF-8") as f:
        doc = xmltodict.parse(f.read())
        data = json.loads(json.dumps(doc))
        cpe_list = data['cpe-list']['cpe-item']

        print('success to load cpe data')
        print('count :', len(cpe_list))
        for cpe in cpe_list:
            Query.insertAllCPEData(cpe)

    print('inserting cpe data is finished.')
    print('total :', Query.getLastCpeId())

    day = "[" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "]"
    logging.error(day + " no error ( insert_cpe )")


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
        day = "[" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "]"
        logging.error(day + traceback.format_exc())
