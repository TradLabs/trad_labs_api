#!/usr/bin/python3
"""Configuration of Applications - All Environments"""
__author__ = 'sfblackl'

import logging

from flaskApp.env import ENVIRONMENT

ENV = ENVIRONMENT

# Default items
# Log Levels
LOG_LEVEL_TOP = logging.INFO
LOG_LEVEL_DB = logging.DEBUG
LOG_LEVEL_ROUTE = logging.DEBUG
LOG_LEVEL_HEALTH = logging.DEBUG

# Loggy Location
LOGGY_URI = 'https://logs-01.loggly.com/inputs/9c825040-1874-4ede-8950-d16d10f76399/tag/python'
