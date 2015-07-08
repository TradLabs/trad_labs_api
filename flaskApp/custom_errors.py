#!/usr/bin/python3
"""Allows for default errors to be formatted correctly according to our specification"""
__author__ = 'sfblackl'

import logging

from flask import jsonify, request, g, render_template

from flaskApp import application
import flaskApp.config


# Create Logger
LOGGER = logging.getLogger('tradlabs.api.custom_errors')
LOGGER.setLevel(flaskApp.config.LOG_LEVEL)

################################################################################
# ERROR MESSAGES
################################################################################
ERROR_MESSAGES = {'400_unknown': 'Bad Request: There was an unspecified error with the request provided.',
                  '401_missing': 'Unauthorized: This resource requires authorization '
                                 'and the Authorization header is blank',
                  '401_invalid': 'Unauthorized: This resource requires authorization '
                                 'and credentials are invalid or expired',
                  '403': 'Forbidden: Your credentials do not have access to the resource.',
                  '403_opt_out': 'Forbidden: You did not permit access to profile',
                  '404': 'Not Found: The resource (%s) you requested could not be found.',
                  '500_01': 'Internal server error (1)',    # General
                  '500_02': 'Internal server error (2)',    # Service
                  '500_03': 'Internal server error (3)'}    # DB


def error_formatter(code, details=None, parm1=None, parm2=None, display_format='json'):
    """Takes Error Code and various parameters to build JSON error structure
       If display_format='html' the message is formatted for human readability"""
    code = str(code)

    if details is not None:
        details = str(details)

    # Determine Status Code based on first 3 letters of code
    status_code = int(code[:3])

    # Build Message based on parameters
    try:
        if parm2 is not None:
            message = str(ERROR_MESSAGES[code] % (parm1, parm2))
        elif parm1 is not None:
            message = str(ERROR_MESSAGES[code] % parm1)
        else:
            message = str(ERROR_MESSAGES[code])
    except Exception:
        message = str('No Message Exists')

    # Build JSON - Include Detail if exists
    if display_format == 'html':
        # Return message and HTTP status code
        error_page = render_template('error.html', code=code, message=message, request_id=g.request_id, details=details)
        return error_page, status_code
    else:
        if details is None:
            json_message = jsonify(code=code,
                                   message=message,
                                   request_id=g.request_id)
        else:
            json_message = jsonify(code=code,
                                   message=message,
                                   request_id=g.request_id,
                                   details=details)
        # Return message and HTTP status code
        return json_message, status_code


################################################################################
# ERROR ROUTES
################################################################################
@application.errorhandler(404)
def page_not_found(err):
    """Error Handler for Page Not Found"""
    return error_formatter(code='404', details=err, parm1=request.path)


@application.errorhandler(500)
def internal_server_error(err):
    """Error Handler for Internal Server Error"""
    return error_formatter(code='500_01', details=err)
