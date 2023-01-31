import logging
import traceback
import time

from dotenv import load_dotenv
from database.database import Database

if __name__ == "__main__":
    logging.basicConfig(filename='./error.log', level=logging.ERROR)
    try:
        load_dotenv()
        Database.connect()
        Database.delete_tables()
        Database.close()
        print("success to delete database.")
    except:
        day = "[" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "]"
        logging.error(day + traceback.format_exc())
