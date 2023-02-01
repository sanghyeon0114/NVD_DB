import logging
import traceback
import time

from dotenv import load_dotenv
from database.database import Database

from query.query import Query

if __name__ == "__main__":
    logging.basicConfig(filename='./info.log', level=logging.INFO)
    try:
        load_dotenv()
        Database.connect()
        Database.init()
        Query.loadQuery()
        Database.close()
        print("success to load database.")
    except:
        day = "[" + time.strftime('%Y-%m-%d %H:%M:%S',
                                  time.localtime(time.time())) + "]"
        logging.info(day + traceback.format_exc())
