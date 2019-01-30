# -*- coding:utf-8 -*-
import logging
log = None


def init_logger():
    global log
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(process)d] [%(thread)d] [%(levelname)s] %(message)s')
    log = logging.getLogger('p2pserver')
    log.info("日志模块初始化完成")
