#!/usr/bin/python3
"""health check functions"""
__author__ = 'sfblackl'

import logging
import sys
import traceback
import socket

from flask import request, jsonify, g

import flaskApp.config
import flaskApp.db



# Create Logger
LOGGER = logging.getLogger('tradlabs.api.health')
LOGGER.setLevel(flaskApp.config.LOG_LEVEL_HEALTH)


def health_check():
    """ Performs health check based on HTTP arguments

    :return: json structure of results of check
    """

    is_healthy = True
    host_name = socket.gethostname().lower()

    # ###############################################################################################################
    # I. Determine detail level
    # Any value but sla should use default of app_pool
    detail_level = request.args.get('detail_level', 'app_pool')
    if detail_level != 'sla':
        detail_level = 'app_pool'
    item_dict = {}

    # ###############################################################################################################
    if detail_level == 'sla' or detail_level == 'reg':
        try:
            db_last_check = flaskApp.db.db_stored_procedure('health_check',
                                                            ('tradlabs api', host_name))['results'][0][0][0]
            item_dict['DB Read/Write'] = 'OK - Last call was from %s was %s seconds ago' % (host_name, db_last_check)
        except Exception:
            item_dict['DB Read/Write'] = 'DOWN - Exception: %s' % \
                                         traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1])
            is_healthy = False
    # End of SLA/REG

    # ###############################################################################################################
    # X. Return Items
    json_message = jsonify(currentSetting=flaskApp.config.ENV,
                           detail=detail_level,
                           isHealth=is_healthy,
                           request_id=g.request_id,
                           host=host_name,
                           items=item_dict)

    return json_message
