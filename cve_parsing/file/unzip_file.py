import logging
import traceback
import time
import os
import zipfile


def main():
    '''main function'''

    os.chdir('./cve')
    for i in range(2002, 2024):
        zipfile.ZipFile('nvdcve-1.1-{}.json.zip'.format(i)
                        ).extract('nvdcve-1.1-{}.json'.format(i))
    zipfile.ZipFile(
        'nvdcpematch-1.0.json.zip').extract('nvdcpematch-1.0.json')

    os.chdir('../cpe')
    zipfile.ZipFile(
        'official-cpe-dictionary_v2.3.xml.zip').extract('official-cpe-dictionary_v2.3.xml')


if __name__ == "__main__":
    logging.basicConfig(filename='./info.log', level=logging.INFO)
    logging.info(
        "---------------------[unzip_file.py]--------------------------")
    try:
        main()
    except:
        day = "[" + time.strftime('%Y-%m-%d %H:%M:%S',
                                  time.localtime(time.time())) + "]"
        logging.info(day + traceback.format_exc())
