import traceback
import logging
import os

from util.print_log import printLog


def main():
    '''main function'''
    for i in range(2002, 2024):
        os.remove('./cve/nvdcve-1.1-{}.json.zip'.format(i))

    os.remove('./cve/nvdcpematch-1.0.json.zip')
    os.remove('./cpe/official-cpe-dictionary_v2.3.xml.zip')


if __name__ == "__main__":
    logging.basicConfig(filename='./info.log', level=logging.INFO)
    try:
        main()
    except:
        printLog("remove_zipfile.py", traceback.format_exc())