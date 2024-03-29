import logging
import traceback
import os
import zipfile

from print_log import printLog


def main():
    '''main function'''

    os.chdir('./cve_data')
    for i in range(2002, 2024):
        zipfile.ZipFile('nvdcve-1.1-{}.json.zip'.format(i)
                        ).extract('nvdcve-1.1-{}.json'.format(i))
    zipfile.ZipFile(
        'nvdcpematch-1.0.json.zip').extract('nvdcpematch-1.0.json')

    os.chdir('../cpe_data')
    zipfile.ZipFile(
        'official-cpe-dictionary_v2.3.xml.zip').extract('official-cpe-dictionary_v2.3.xml')


if __name__ == "__main__":
    logging.basicConfig(filename='./info.log', level=logging.INFO)
    try:
        main()
    except:
        printLog("unzip_file.py", traceback.format_exc())
