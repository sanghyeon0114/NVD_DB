import logging
import traceback
import os
import shutil
import zipfile
import pandas as pd
from requests import get

from util.print_log import printLog

from dotenv import load_dotenv
from database.database import Database

from query.query import Query
from format.item import Item


def download(url, link):
    file_name = url.split('/')[-1]
    with open(link+file_name, "wb") as file:
        response = get(url)
        file.write(response.content)


def change_file():
    download(
        'https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-modified.json.zip', './recent/')
    download(
        'https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-recent.json.zip', './recent/')

    os.chdir('./recent')
    zipfile.ZipFile(
        'nvdcve-1.1-modified.json.zip').extract('nvdcve-1.1-modified.json')
    zipfile.ZipFile(
        'nvdcve-1.1-recent.json.zip').extract('nvdcve-1.1-recent.json')

    os.remove('./nvdcve-1.1-modified.json.zip')
    os.remove('./nvdcve-1.1-recent.json.zip')


def main():
    '''main function'''
    if os.path.exists("./recent"):
        shutil.rmtree('./recent')
    os.makedirs("./recent", exist_ok=True)

    change_file()

    try:
        modified = pd.read_json('nvdcve-1.1-modified.json').get('CVE_Items')
        for i in range(len(modified)):
            Query.insertAllCVEData(Item(modified[i]))
    except:
        printLog("upload_recent_file.py", traceback.format_exc())

    try:
        recent = pd.read_json('nvdcve-1.1-recent.json').get('CVE_Items')

        for i in range(len(recent)):
            Query.insertAllCVEData(Item(recent[i]))
    except:
        printLog("upload_recent_file.py", traceback.format_exc())

    printLog("upload_recent_file.py", "finished")


if __name__ == "__main__":
    logging.basicConfig(filename='./info.log', level=logging.INFO)
    printLog("upload_recent_file.py", "run")
    try:
        load_dotenv()
        Database.connect()
        Query.loadQuery()
        main()
        Database.close()
    except:
        printLog("upload_recent_file.py", traceback.format_exc())
