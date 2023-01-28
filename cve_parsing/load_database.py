import logging
import traceback

from dotenv import load_dotenv
from database.database import Database

from query.query import Query

if __name__ == "__main__":
    logging.basicConfig(filename='./error.log', level=logging.ERROR)
    try:
        load_dotenv()
        Database.connect()
        Database.init()
        Query.loadQuery()
        Database.close()
        print("success to load database.")
    except:
        logging.error(traceback.format_exc())