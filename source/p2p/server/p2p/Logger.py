# -*- coding:utf-8 -*-
import logging
logger = None


def init_logger():
    globals logger
    FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
    logging.basicConfig(FORMAT)
    logger = logging.getLogger('p2pserver')
