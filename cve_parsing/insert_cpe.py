import logging
import traceback

from dotenv import load_dotenv
from database.database import Database

from query.query import Query

## global variables ##
# CPE_DATA = pd.read_csv('cpe/official-cpe-dictionary_v2.3.xml')


# [TODO] xmltodict 사용해서 CPE 데이터 뽑기

def main():
    '''main function'''

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
