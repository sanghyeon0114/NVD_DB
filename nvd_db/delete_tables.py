import logging
import traceback

from util.print_log import printLog

from dotenv import load_dotenv
from database.database import Database

if __name__ == "__main__":
    logging.basicConfig(filename='./info.log', level=logging.INFO)
    printLog("delete_tables.py", "run")
    try:
        load_dotenv()
        Database.connect()
        Database.delete_tables()
        Database.close()
        print("success to delete database.")
    except:
        printLog("delete_tables.py", traceback.format_exc())
