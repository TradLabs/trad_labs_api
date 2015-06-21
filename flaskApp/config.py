#!/usr/bin/python3
"""Configuration of Applications - All Environments"""
__author__ = 'sfblackl'
import os
import traceback
import sys
import logging

from flaskApp.env import START_ENV

if START_ENV == 'tbd':
    ENV = START_ENV
    try:
        ENV = os.environ['trad_labs_api_env']
    except Exception:
        print("Error getting environment variable: %s" %
              traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))


# Default items
# Log Levels
LOG_LEVEL_TOP = logging.INFO
LOG_LEVEL_DB = logging.DEBUG
LOG_LEVEL_ROUTE = logging.DEBUG
LOG_LEVEL_HEALTH = logging.DEBUG

# Loggy Location
LOGGY_URI = 'https://logs-01.loggly.com/inputs/9c825040-1874-4ede-8950-d16d10f76399/tag/python'
