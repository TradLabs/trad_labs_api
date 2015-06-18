#!/usr/bin/python3
"""Used to launch flask application from outside module"""
__author__ = 'sfblackl'

from flaskApp import application

if __name__ == 'main':
    application.run()
