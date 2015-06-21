#!/usr/bin/python3
# pylint: disable=invalid-name
"""Creates Module"""
__author__ = 'sfblackl'

from flask import Flask
application = Flask(__name__)

import flaskApp.routes
