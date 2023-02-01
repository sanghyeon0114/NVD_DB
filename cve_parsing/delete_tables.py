import logging
import traceback
import time

from dotenv import load_dotenv
from database.database import Database

if __name__ == "__main__":
    logging.basicConfig(filename='./info.log', level=logging.INFO)
    logging.info(
        "---------------------[delete_tables.py]--------------------------")
    try:
        load_dotenv()
        Database.connect()
        Database.delete_tables()
        Database.close()
        print("success to delete database.")
    except:
        day = "[" + time.strftime('%Y-%m-%d %H:%M:%S',
                                  time.localtime(time.time())) + "]"
        logging.info(day + traceback.format_exc())
