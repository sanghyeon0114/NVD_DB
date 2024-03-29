import logging
import traceback
import os
import shutil
from requests import get

from print_log import printLog


def download(url, link):
    file_name = url.split('/')[-1]
    with open(link+file_name, "wb") as file:
        response = get(url)
        file.write(response.content)


def main():
    '''main function'''
    if os.path.exists("./cve_data"):
        shutil.rmtree('./cve_data')
    os.makedirs("./cve", exist_ok=True)

    if os.path.exists("./cpe_data"):
        shutil.rmtree('./cpe_data')
    os.makedirs("./cpe", exist_ok=True)

    for i in range(2002, 2024):
        download(
            'https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-{}.json.zip'.format(i), './cve/')

    download(
        'https://nvd.nist.gov/feeds/json/cpematch/1.0/nvdcpematch-1.0.json.zip', './cve/')
    download('https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.zip', './cpe/')


if __name__ == "__main__":
    logging.basicConfig(filename='./info.log', level=logging.INFO)
    try:
        main()
    except:
        printLog("upload_file.py", traceback.format_exc())
