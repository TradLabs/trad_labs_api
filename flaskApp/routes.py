#!/usr/bin/python3
"""Maps all incoming paths to correct functions to handle"""
__author__ = 'sfblackl'

import logging
import time
import uuid

from flask import g, request

from flaskApp import application
import flaskApp.health
import flaskApp.config
import flaskApp.custom_errors



# Create Logger
LOGGER = logging.getLogger('tradlabs.api.routes')
LOGGER.setLevel(flaskApp.config.LOG_LEVEL_ROUTE)


################################################################################
# OTHER
################################################################################
@application.route('/tradlabs/v1/health')
def health():
    """Health Check Function used by ELB and SLA Monitoring"""
    LOGGER.debug('Routing to health')
    return flaskApp.health.health_check()

################################################################################
# TESTING
################################################################################
@application.route('/tradlabs/v1/500', methods=['GET', 'POST', 'PUT', 'DELETE'])
def test_500():
    """Forces error to validate error message is correct"""
    LOGGER.debug('Routing to HTTP 500 Error')
    print(1/0)

@application.route('/tradlabs/v1/403', methods=['GET', 'POST', 'PUT', 'DELETE'])
def test_403():
    """Generates 403 Error.  ToDo: Replace this with valid test"""
    LOGGER.debug('Routing to HTTP 403 Error')
    return flaskApp.custom_errors.error_formatter(code=40301)

################################################################################
# LOG HTTP REQUESTS
################################################################################
def http_log_entry(response=None, exception=None):
    """Logs Entry at close"""

    # Calculate Request Duration
    start = getattr(g, 'start', None)
    diff = 0
    if start is not None:
        diff = int((time.time() - g.start) * 1000) # Gets time in MS

    # Determine HTTP Status, Code
    # If we come without a response object, default to HTTP 520
    http_status = 'ERROR'
    status_code = 520
    if response is not None:
        status_code = response.status_code
        if status_code == 200 or status_code == 201:
            http_status = 'SUCCESS'

    # Log Entry
    if exception is None:
        LOGGER.info('HTTP|%s|%d|%s|%s|%s|%s', http_status, status_code, request.method,
                    request.path, '{0:0,}'.format(diff), str(exception))
    else:
        LOGGER.info('HTTP|%s|%d|%s|%s|%s|%s', http_status, status_code, request.method,
                    request.path, '{0:0,}'.format(diff), str(exception))


@application.before_request
def before_request():
    """Sets up actions before request starts.  Used for Logging"""
    g.start = time.time()
    g.env = flaskApp.config.ENV

    # Use incoming Request ID if provided
    request_id = request.headers.get('X_Request_ID', uuid.uuid1())
    g.request_id = request_id

@application.after_request
def after_request(response):
    """Logs a non-exception request"""
    http_log_entry(response=response)
    return response

@application.teardown_request
def teardown_request(exception=None):
    """Still Log request even if exception"""
    # Only Care about items that come with exceptions
    if exception is not None:
        http_log_entry(exception=exception)
