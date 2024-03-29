import time
import logging


def printLog(title: str, content: str):
    day = time.strftime('%Y-%m-%d %H:%M:%S',
                        time.localtime(time.time()))
    logging.info("[{}.py][{}] {}".format(title, day, content))
