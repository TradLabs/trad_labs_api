#!/usr/bin/python3
"""health check functions"""
__author__ = 'sfblackl'

import logging

from flask import request, jsonify

import flaskApp.config

# Create Logger
LOGGER = logging.getLogger('tradlabs.api.health')
LOGGER.setLevel(flaskApp.config.LOG_LEVEL_HEALTH)

def health_check():
    """Performs health check functions"""
    # I. Determine detail level
    # Any value but sla should use default of app_pool
    detail_level = request.args.get('detail_level', 'app_pool')
    if detail_level != 'sla':
        detail_level = 'app_pool'

    # X. Return Items
    json_message = jsonify(currentSetting=flaskApp.config.ENV,
                           detail=detail_level,
                           isHealth=True)

    return json_message
