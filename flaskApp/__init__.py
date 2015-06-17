#!/usr/bin/env python
# pylint: disable=C0103
# pylint: disable=R0401

"""Creates Module"""
# __author__ = 'sfblackl'

from flask import Flask
application = Flask(__name__)

import flaskApp.routes
