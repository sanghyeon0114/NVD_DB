import logging
import traceback

from util.print_log import printLog

from dotenv import load_dotenv
from database.database import Database

from query.query import Query

if __name__ == "__main__":
    logging.basicConfig(filename='./info.log', level=logging.INFO)
    printLog("create_database.py", "run")
    try:
        load_dotenv()
        Database.connect()
        Database.init()
        Query.loadQuery()
        Database.close()
        print("success to load database.")
    except:
        printLog("create_database.py", traceback.format_exc())
