import time
import traceback
import logging
import os


def main():
    '''main function'''
    for i in range(2002, 2024):
        os.remove('./cve/nvdcve-1.1-{}.json.zip'.format(i))

    os.remove('./cve/nvdcpematch-1.0.json.zip')
    os.remove('./cpe/official-cpe-dictionary_v2.3.xml.zip')


if __name__ == "__main__":
    logging.basicConfig(filename='./info.log', level=logging.INFO)
    logging.info(
        "---------------------[rm_zipfile.py]--------------------------")
    try:
        main()
    except:
        day = "[" + time.strftime('%Y-%m-%d %H:%M:%S',
                                  time.localtime(time.time())) + "]"
        logging.info(day + traceback.format_exc())
