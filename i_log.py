# coding: utf-8

import sys
import logging
reload(sys)
sys.setdefaultencoding('utf-8')


def log(filename, msg, mode):
    open(filename, 'a')
    logger = logging.getLogger('log')
    logger.setLevel('DEBUG')

    flog_format = logging.Formatter("%(levelname)s\n[%(filename)s: %(lineno)d]\n%(asctime)s\n%(message)s\n")
    slog_format = logging.Formatter("%(levelname)s\n%(asctime)s\n%(message)s\n")
    filelog = logging.FileHandler(filename)
    filelog.setFormatter(flog_format)
    streamlog = logging.StreamHandler()
    streamlog.setFormatter(slog_format)
    logger.addHandler(filelog)
    logger.addHandler(streamlog)
    if mode == 'DEBUG':
        logger.debug(msg)
    elif mode == 'INFO':
        logger.info(msg)
    elif mode == 'WARNING':
        logger.warning(msg)
    elif mode == 'ERROR':
        logger.error(msg)
    elif mode == 'CRITICAL':
        logger.critical(msg)
    else:
        print "MODE WRONG"
    logger.removeHandler(filelog)
    logger.removeHandler(streamlog)
