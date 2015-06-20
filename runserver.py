#!/usr/bin/python3
"""Used to launch flask application from outside module"""
__author__ = 'sfblackl'

import log_setup
log_setup.start_log()

################################################################################
# Start Our Application
################################################################################
from flaskApp import application

application.run()
