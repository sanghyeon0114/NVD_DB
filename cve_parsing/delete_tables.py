import logging
import traceback

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
        logging.error(traceback.format_exc())