#!/usr/bin/python3
"""Maps all incoming paths to correct functions to handle"""
__author__ = 'sfblackl'

import logging
import time
import uuid
import traceback
import sys

from flask import g, request, render_template, url_for

from flaskApp import application
import flaskApp.health
import flaskApp.config
import flaskApp.custom_errors
import flaskApp.google
import flaskApp.db



# Create Logger
LOGGER = logging.getLogger('tradlabs.api.routes')
LOGGER.setLevel(flaskApp.config.LOG_LEVEL_ROUTE)


################################################################################
# WWW
################################################################################
@application.route('/tradlabs/home')
def home():
    """Main Home Page"""
    login_uri = url_for('google_login', _external=True)
    page = render_template('home.html', login_uri=login_uri)
    return page


################################################################################
# Identity
################################################################################
@application.route('/tradlabs/login')
def google_login():
    """Build redirect request to identity provider"""
    return flaskApp.google.google_login()


@application.route('/tradlabs/v1/google_callback')
def google_callback():
    """Handle redirection back from identity provider via user's browser"""
    LOGGER.debug('Root: %s', application.root_path)
    return flaskApp.google.google_callback()


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
    return flaskApp.custom_errors.error_formatter(code='403')


@application.route('/tradlabs/v1/test/db', methods=['GET', 'POST', 'PUT', 'DELETE'])
def test_db():
    """Test of various DB Functions"""
    LOGGER.debug('Routing to DB Test')

    return flaskApp.db.db_tests()


################################################################################
# LOG HTTP REQUESTS
################################################################################
def http_log_entry(response=None, exception=None):
    """Logs Entry at close"""

    # Calculate Request Duration
    start = getattr(g, 'start', None)
    diff = 0
    if start is not None:
        diff = int((time.time() - g.start) * 1000)  # Gets time in MS

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
        LOGGER.info('HTTP|%s|%d|%s|%s|%s|', http_status, status_code, request.method,
                    request.path, '{0:0,}'.format(diff))
    else:
        LOGGER.info('HTTP|%s|%d|%s|%s|%s|%s', http_status, status_code, request.method,
                    request.path, '{0:0,}'.format(diff),
                    traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))


@application.before_request
def before_request():
    """Sets up actions before request starts.  Used for Logging"""
    g.start = time.time()
    g.env = flaskApp.config.ENV

    # Use incoming Request ID if provided
    request_id = str(request.headers.get('X_Request_ID', uuid.uuid1()))
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
