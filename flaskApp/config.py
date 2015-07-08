#!/usr/bin/python3
"""Configuration of Applications - All Environments"""
__author__ = 'sfblackl'
import os
import logging

from flaskApp.env import START_ENV


################################################################################
# If CI hasn't changed to specific env, use OS Env Variables to get it
################################################################################
ENV = START_ENV
if ENV == 'tbd':
    ENV = os.getenv('trad_labs_api_env', START_ENV)

# Default items
# Log Levels
LOG_LEVEL = logging.INFO
LOG_LEVEL_DB = logging.DEBUG
LOG_LEVEL_GOOGLE = logging.DEBUG
LOG_LEVEL_HEALTH = logging.DEBUG
LOG_LEVEL_ROUTE = logging.DEBUG

# Log Directory
LOG_PATH = 'C:\\temp\\'
if ENV == 'ci':
    LOG_PATH = ''
elif ENV == 'qa1':
    LOG_PATH = '/var/log/trad_labs/'

# Loggly Location
LOGGLY_URI = 'https://logs-01.loggly.com/inputs/9c825040-1874-4ede-8950-d16d10f76399/tag/python'
