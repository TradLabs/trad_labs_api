#!/usr/bin/python3
"""Makes Logging consistent between unit tests and normal run"""
__author__ = 'sfblackl'

################################################################################
# SetUp Logging
################################################################################
import logging

import logging.handlers

import flaskApp.loggly_class
import flaskApp.config


def start_log(loggly=True):
    """Starts Logging to Occur"""
    logger = logging.getLogger('tradlabs')
    logger.setLevel(flaskApp.config.LOG_LEVEL)

    # File Handler
    h_file = logging.handlers.TimedRotatingFileHandler(flaskApp.config.LOG_PATH + 'api.log',
                                                       when='midnight', backupCount=5)
    h_console = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(lineno)3d:%(module)-10s-'
                                  ' %(levelname)-8s- %(message)s')
    h_file.setFormatter(formatter)
    h_console.setFormatter(formatter)
    logger.addHandler(h_file)
    logger.addHandler(h_console)

    if loggly:
        h_loggly = flaskApp.loggly_class.HTTPSHandler(flaskApp.config.LOGGLY_URI)
        logger.addHandler(h_loggly)
