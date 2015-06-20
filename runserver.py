#!/usr/bin/python3
"""Used to launch flask application from outside module"""
__author__ = 'sfblackl'

################################################################################
# SetUp Logging
################################################################################
import logging
import logging.handlers
import logging.config

import loggy_class

LOGGER = logging.getLogger('tradlabs')
LOGGER.setLevel(logging.INFO)

# File Handler
H_FILE = logging.handlers.TimedRotatingFileHandler('C:\\TEMP\\api.log',
                                                   when='midnight', backupCount=5)
H_CONSOLE = logging.StreamHandler()

FORMATTER = logging.Formatter('%(asctime)s - %(lineno)3d:%(module)-10s-'
                              ' %(levelname)-8s- %(message)s')
H_FILE.setFormatter(FORMATTER)
H_CONSOLE.setFormatter(FORMATTER)

FORMATTER = logging.Formatter('"loggerName":"%(name)s", '
                              '"asciTime":"%(asctime)s", '
                              '"fileName":"%(filename)s", '
                              '"logRecordCreationTime":"%(created)f", '
                              '"functionName":"%(funcName)s", '
                              '"levelNo":"%(levelno)s", '
                              '"lineNo":"%(lineno)d", '
                              '"time":"%(msecs)d", '
                              '"levelName":"%(levelname)s", '
                              '"message":"%(message)s"')
H_LOGGY = loggy_class.HTTPSHandler('https://logs-01.loggly.com/inputs/9c825040-1874-4ede-8950-d16d10f76399/tag/python')
H_LOGGY.setFormatter(FORMATTER)

LOGGER.addHandler(H_FILE)
LOGGER.addHandler(H_CONSOLE)
LOGGER.addHandler(H_LOGGY)


################################################################################
# Start Our Application
################################################################################
from flaskApp import application
application.run()
